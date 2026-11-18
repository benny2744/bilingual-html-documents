"""Render validated bilingual data as offline HTML; never overwrite outputs."""
import argparse
from html import escape
import json
from pathlib import Path
from string import Template
import zipfile
from validate import validate_document

ROOT = Path(__file__).resolve().parents[1]


def bilingual(pair):
    return '\n'.join(f'<span lang="{lang}" data-language="{lang}">{escape(pair[lang])}</span>' for lang in ('zh', 'en'))


def render_block(block):
    kind = block['type']
    if kind == 'paragraph': return '<p>' + bilingual(block['text']) + '</p>'
    if kind == 'callout':
        title = '<h3>' + bilingual(block['title']) + '</h3>' if 'title' in block else ''
        return '<aside class="callout ' + block.get('tone', 'info') + '">' + title + '<p>' + bilingual(block['text']) + '</p></aside>'
    if kind == 'list':
        tag = 'ol' if block.get('ordered', False) else 'ul'
        return '<' + tag + '>' + ''.join('<li>' + bilingual(item) + '</li>' for item in block['items']) + '</' + tag + '>'
    if kind == 'table':
        headers = ''.join('<th scope="col">' + bilingual(item) + '</th>' for item in block['headers'])
        rows = ''.join('<tr>' + ''.join('<td>' + bilingual(item) + '</td>' for item in row) + '</tr>' for row in block['rows'])
        return '<div class="table-wrap"><table><thead><tr>' + headers + '</tr></thead><tbody>' + rows + '</tbody></table></div>'
    return '<ul>' + ''.join('<li><a href="' + escape(item['url'], quote=True) + '" rel="noopener noreferrer">' + bilingual(item['label']) + '</a></li>' for item in block['items']) + '</ul>'


def render_document(data):
    validate_document(data)
    language = data.get('default_language', 'zh')
    visibility = {'student': {'zh': '学生使用', 'en': 'Student-facing'}, 'internal': {'zh': '仅限内部', 'en': 'Internal only'}, 'public': {'zh': '公开内容', 'en': 'Public'}}[data['visibility']]
    metadata = '<dl class="metadata">' + ''.join('<div><dt>' + bilingual(item['label']) + '</dt><dd>' + bilingual(item['value']) + '</dd></div>' for item in data['metadata']) + '</dl>' if data['metadata'] else ''
    notice = '<aside class="callout info"><p>' + bilingual(data['notice']) + '</p></aside>' if 'notice' in data else ''
    sections = []
    for section in data['sections']:
        lead = '<p class="lead">' + bilingual(section['lead']) + '</p>' if 'lead' in section else ''
        sections.append('<section id="section-' + section['id'] + '"><details class="document-section" open><summary><h2>' + bilingual(section['title']) + '</h2></summary><div class="section-body">' + lead + ''.join(render_block(block) for block in section['blocks']) + '</div></details></section>')
    shell = Template((ROOT / 'templates/document.html').read_text(encoding='utf-8'))
    return shell.substitute(default_language=language, slug=data['slug'], page_title=escape(data['title'][language]), title=bilingual(data['title']), subtitle=bilingual(data['subtitle']), metadata=metadata, notice=notice, visibility=bilingual(visibility), content='\n'.join(sections), contents=''.join('<li><a href="#section-' + section['id'] + '">' + bilingual(section['title']) + '</a></li>' for section in data['sections']), download_label=bilingual({'zh': '下载 HTML', 'en': 'Download HTML'}), print_label=bilingual({'zh': '浏览器打印', 'en': 'Print'}), contents_label=bilingual({'zh': '目录', 'en': 'Contents'}), footer=bilingual({'zh': '可离线阅读 · 中英双语文档', 'en': 'Offline-ready · Chinese / English document'}))


def readme(data):
    labels = {'student': ('学生使用', 'Student-facing'), 'internal': ('仅限内部', 'Internal only'), 'public': ('公开内容', 'Public')}
    zh, en = labels[data['visibility']]
    return f'''中英双语静态文档 / Bilingual static document
可见性 / Visibility: {zh} / {en}

本包仅包含 index.html 和 README.txt。打开 index.html 可离线阅读。
This package contains only index.html and README.txt. Open index.html offline.

可见性标签不是访问控制。内部内容需部署在启用身份验证的站点。
Internal content requires authenticated hosting. A visibility badge is not access control.
未列出的链接不等于私密；请勿将未获授权的内部内容放在公开站点。
An unlisted URL is not private. Do not publicly host unauthorized internal content.

两个语言版本均在 HTML 中。隐藏文本不是隐私保护。
Both languages are in the HTML. Hidden text is not a privacy boundary.

页面使用内联 CSS 和 JavaScript。严格 CSP 可能阻止交互；无脚本时两种语言仍可阅读。
Inline CSS/JavaScript are used. A strict CSP may block interactions; both languages remain readable without JavaScript.
部署时应评估 CSP，使用适当的哈希或 nonce，不要为此放宽整个站点的安全策略。
Review hosting CSP; use appropriate hashes or nonces rather than weakening site-wide security policy.
外部资源链接由读者自行打开；本文档不会自动请求网络资源。
External resource links are reader-initiated; this document requests no network assets.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--package', type=Path)
    args = parser.parse_args()
    created = []
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        html = render_document(data)  # validate everything before any writes
        targets = [args.output] + ([args.package] if args.package else [])
        paths = [p.resolve() for p in targets]
        if len(set(paths)) != len(paths) or args.input.resolve() in paths: raise ValueError('input/output/package paths must be distinct')
        for target in targets:
            if target.exists() or target.is_symlink(): raise ValueError(f'refusing existing output: {target}')
        for target in targets: target.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8', newline='\n') as stream:
            created.append(args.output); stream.write(html)
        if args.package:
            with args.package.open('xb') as stream:
                created.append(args.package)
                with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                    archive.writestr('index.html', html.encode('utf-8'))
                    archive.writestr('README.txt', readme(data).encode('utf-8'))
    except (OSError, ValueError) as exc:
        for target in created: target.unlink(missing_ok=True)
        parser.exit(1, f'Render failed: {exc}\n')
    print(f'Rendered HTML: {args.output.resolve()}')
    if args.package: print(f'Static package: {args.package.resolve()}')


if __name__ == '__main__': main()
