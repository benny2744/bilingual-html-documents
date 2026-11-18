"""Behavioral checks; execute with python scripts/test_documents.py."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate import validate_document
from render import render_document


def sample():
    p = lambda s: {'zh': s, 'en': s}
    return {'slug': 'sample', 'kind': 'lesson', 'visibility': 'student',
            'title': p('示例'), 'subtitle': p('Fictional'), 'default_language': 'zh',
            'metadata': [], 'sections': [{'id': 'start', 'title': p('开始'),
             'blocks': [{'type': 'paragraph', 'text': p('Hello')}]}]}


class DocumentsTests(unittest.TestCase):
    def invalid(self, mutate):
        d = sample(); mutate(d)
        with self.assertRaises(ValueError): validate_document(d)

    def test_valid_and_default(self):
        d = sample(); del d['default_language']; validate_document(d)
        self.assertIn('data-default-language="zh"', render_document(d))

    def test_article_kind(self):
        d = sample(); d['kind'] = 'article'
        self.assertIs(validate_document(d), d)
        self.assertIn('Hello', render_document(d))
        d['kind'] = 'unknown'
        with self.assertRaises(ValueError): validate_document(d)

    def test_missing_pair(self):
        self.invalid(lambda d: d['title'].pop('en'))

    def test_empty_pair(self):
        self.invalid(lambda d: d['title'].update(en=' '))

    def test_unknown_private_fields(self):
        self.invalid(lambda d: d.update(private_notes='secret'))
        self.invalid(lambda d: d['sections'][0]['blocks'][0].update(private='secret'))
        self.invalid(lambda d: d['title'].update(private='secret'))

    def test_duplicate_ids(self):
        self.invalid(lambda d: d['sections'].append(copy.deepcopy(d['sections'][0])))

    def test_bad_slug(self):
        for slug in ['../escape', '你好', 'bad space', 'Bad', '']:
            self.invalid(lambda d: d.update(slug=slug))

    def test_protocol_rejection(self):
        for url in ['javascript:alert(1)', 'data:text/html,hi', '//evil.test', 'https:', 'https://good.test\n']:
            self.invalid(lambda d: d['sections'][0].update(blocks=[{'type': 'links', 'items': [{'label': d['title'], 'url': url}]}]))

    def test_table_width(self):
        self.invalid(lambda d: d['sections'][0].update(blocks=[{'type': 'table', 'headers': [d['title']], 'rows': [[d['title'], d['title']]]}]))

    def test_escaping(self):
        d = sample(); d['title'] = {'zh': '</script><img src=x onerror=alert(1)>', 'en': '" & <attack>'}
        out = render_document(d)
        self.assertIn('&lt;img', out); self.assertNotIn('<img src=x', out)
        self.assertIn('&lt;attack&gt;', out)

    def test_full_bilingual_and_no_js(self):
        out = render_document(sample())
        self.assertIn('lang="zh"', out); self.assertIn('lang="en"', out)
        self.assertIn('<noscript>', out); self.assertIn('data-language', out)
        self.assertIn('html:not(.has-js) .js-only{display:none!important}', out)
        self.assertNotIn('<span lang="en" data-language="en" hidden', out)
        self.assertIn('document.cloneNode(true)', out)

    def test_collapsible_sections_and_navigation(self):
        out = render_document(sample())
        self.assertIn('<details class="document-section" open><summary><h2>', out)
        for control in ('expand-all', 'collapse-all', 'document-top'):
            self.assertIn('id="' + control + '"', out)
        for label in ('展开全部', 'Expand all', '折叠全部', 'Collapse all', '返回顶部', 'Back to top'):
            self.assertIn(label, out)
        self.assertIn('position:fixed', out)
        self.assertIn("window.addEventListener('beforeprint', preparePrint)", out)
        self.assertIn("clone.querySelectorAll('details.document-section')", out)

    def test_final_command_panel(self):
        out = render_document(sample())
        panel = out.split('<nav class="rail"', 1)[1].split('</nav>', 1)[0]
        self.assertEqual(panel.count('role="switch"'), 1)
        self.assertEqual(panel.count('<svg '), 5)
        self.assertNotIn('data-switch=', out)
        for control in ('language-toggle', 'download-html', 'print-document', 'expand-all', 'collapse-all'):
            self.assertEqual(panel.count('id="' + control + '"'), 1)
        self.assertIn('data-tip-zh="下载 HTML"', panel)
        self.assertIn('data-tip-en="Download HTML"', panel)
        self.assertIn('tip-control:focus-visible::after', out)
        self.assertIn('.rail li a{display:block;padding:10px 12px;border:1px solid', out)
        self.assertIn('max-width:1600px', out)

    def test_no_external_assets(self):
        out = render_document(sample())
        self.assertNotIn('<script src=', out); self.assertNotIn('<link ', out)
        self.assertNotIn('@import', out); self.assertNotIn('fetch(', out)
        self.assertNotIn('url(', out)

    def test_cli_zip_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'data.json'; output = root / 'guide.html'; package = root / 'guide.zip'
            source.write_text(json.dumps(sample(), ensure_ascii=False), encoding='utf-8')
            command = [sys.executable, str(ROOT / 'scripts/render.py'), '--input', str(source), '--output', str(output), '--package', str(package)]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(output.read_text(encoding='utf-8'), render_document(sample()))
            with zipfile.ZipFile(package) as z:
                self.assertEqual(sorted(z.namelist()), ['README.txt', 'index.html'])
                self.assertEqual(z.read('index.html').decode('utf-8'), output.read_text(encoding='utf-8'))
                self.assertIn('unlisted', z.read('README.txt').decode('utf-8'))
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            output.unlink()
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(json.loads(source.read_text(encoding='utf-8')), sample())

    def test_invalid_cli_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'bad.json'; output = root / 'out.html'
            d = sample(); d['private'] = 'hidden'; source.write_text(json.dumps(d), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/render.py'), '--input', str(source), '--output', str(output)], capture_output=True)
            self.assertNotEqual(result.returncode, 0); self.assertFalse(output.exists())

    def test_malformed_types(self):
        for kind in [[], {}, None, 4]:
            self.invalid(lambda d: d['sections'][0]['blocks'][0].update(type=kind))
        self.invalid(lambda d: d.update({1: 'private'}))
        self.invalid(lambda d: d['sections'][0]['blocks'].append('not an object'))
        self.invalid(lambda d: d['sections'][0].update(id='download-html/evil'))

    def test_reserved_control_id_is_namespaced(self):
        d = sample(); d['sections'][0]['id'] = 'download-html'
        out = render_document(d)
        self.assertIn('<section id="section-download-html">', out)
        self.assertEqual(out.count('id="download-html"'), 1)

    def test_synthetic_fixtures(self):
        for name in ('lesson', 'meeting'):
            d = json.loads((ROOT / 'assets/examples' / (name + '.json')).read_text(encoding='utf-8'))
            validate_document(d); out = render_document(d)
            self.assertIn('虚构', out); self.assertIn('Fictional', out)
            self.assertNotIn('application/json', out)

    def test_all_blocks(self):
        d = sample(); p = d['title']
        d['sections'][0]['blocks'] += [{'type': 'callout', 'title': p, 'text': p, 'tone': 'warning'}, {'type': 'list', 'items': [p], 'ordered': True}, {'type': 'table', 'headers': [p], 'rows': [[p]]}, {'type': 'links', 'items': [{'label': p, 'url': 'https://example.org/?a=1&b=2'}]}]
        out = render_document(d)
        for tag in ['<aside', '<ol', '<table', '<a ']: self.assertIn(tag, out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
