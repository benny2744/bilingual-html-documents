"""Strict plain-text bilingual document validation, using only stdlib."""
import argparse
import json
import re
from urllib.parse import urlsplit
from typing import NoReturn

SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z', re.ASCII)


def fail(path, message) -> NoReturn:
    raise ValueError(f'{path}: {message}')


def obj(value, required, optional, path):
    if not isinstance(value, dict): fail(path, 'expected object')
    if any(not isinstance(key, str) for key in value): fail(path, 'object keys must be strings')
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing: fail(path, 'missing keys: ' + ', '.join(sorted(missing)))
    if extra: fail(path, 'unknown keys: ' + ', '.join(sorted(extra)))


def pair(value, path):
    obj(value, ('zh', 'en'), (), path)
    for lang in ('zh', 'en'):
        text = value[lang]
        if not isinstance(text, str) or not text.strip(): fail(path + '.' + lang, 'expected nonempty plain text')
        if any(ord(c) < 32 and c not in '\n\r\t' for c in text): fail(path, 'control characters forbidden')
        try: text.encode('utf-8')
        except UnicodeEncodeError: fail(path, 'invalid UTF-8 text')


def array(value, path, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value): fail(path, 'expected ' + ('nonempty ' if nonempty else '') + 'list')


def url(value, path):
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 for c in value): fail(path, 'invalid URL')
    try:
        parts = urlsplit(value)
        if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username is not None or parts.password is not None: fail(path, 'only absolute http/https URLs without credentials allowed')
        parts.port
    except ValueError: fail(path, 'invalid URL')


def block(value, path):
    if not isinstance(value, dict): fail(path, 'expected block object')
    kind = value.get('type')
    formats = {'paragraph': (('text',), ()), 'callout': (('text',), ('title', 'tone')), 'list': (('items',), ('ordered',)), 'table': (('headers', 'rows'), ()), 'links': (('items',), ())}
    if not isinstance(kind, str) or kind not in formats: fail(path, 'unsupported block type')
    required, optional = formats[kind]
    obj(value, ('type',) + required, optional, path)
    if kind in ('paragraph', 'callout'):
        pair(value['text'], path + '.text')
        if 'title' in value: pair(value['title'], path + '.title')
        if 'tone' in value and value['tone'] not in ('info', 'warning'): fail(path, 'invalid tone')
    elif kind == 'list':
        array(value['items'], path + '.items')
        for i, item in enumerate(value['items']): pair(item, f'{path}.items[{i}]')
        if 'ordered' in value and type(value['ordered']) is not bool: fail(path, 'ordered must be boolean')
    elif kind == 'table':
        array(value['headers'], path + '.headers'); array(value['rows'], path + '.rows')
        for i, item in enumerate(value['headers']): pair(item, f'{path}.headers[{i}]')
        for i, row in enumerate(value['rows']):
            array(row, f'{path}.rows[{i}]')
            if len(row) != len(value['headers']): fail(path, 'table row width differs from headers')
            for j, item in enumerate(row): pair(item, f'{path}.rows[{i}][{j}]')
    else:
        array(value['items'], path + '.items')
        for i, item in enumerate(value['items']):
            p = f'{path}.items[{i}]'; obj(item, ('label', 'url'), (), p)
            pair(item['label'], p + '.label'); url(item['url'], p + '.url')


def validate_document(data):
    """Return the original valid object unchanged, or raise ValueError."""
    obj(data, ('slug', 'kind', 'visibility', 'title', 'subtitle', 'metadata', 'sections'), ('default_language', 'notice'), '$')
    if not isinstance(data['slug'], str) or not SLUG.fullmatch(data['slug']): fail('$.slug', 'expected lowercase ASCII hyphenated slug')
    if data['kind'] not in ('lesson', 'meeting', 'article'): fail('$.kind', 'invalid kind')
    if data['visibility'] not in ('student', 'internal', 'public'): fail('$.visibility', 'invalid visibility')
    if data.get('default_language', 'zh') not in ('zh', 'en'): fail('$.default_language', 'invalid language')
    for key in ('title', 'subtitle', 'notice'):
        if key in data: pair(data[key], '$.' + key)
    array(data['metadata'], '$.metadata', False)
    for i, item in enumerate(data['metadata']):
        p = f'$.metadata[{i}]'; obj(item, ('label', 'value'), (), p)
        pair(item['label'], p + '.label'); pair(item['value'], p + '.value')
    array(data['sections'], '$.sections'); seen = set()
    for i, section in enumerate(data['sections']):
        p = f'$.sections[{i}]'; obj(section, ('id', 'title', 'blocks'), ('lead',), p)
        sid = section['id']
        if not isinstance(sid, str) or not SLUG.fullmatch(sid): fail(p, 'invalid section ID')
        if sid in seen: fail(p, 'duplicate section ID')
        seen.add(sid); pair(section['title'], p + '.title')
        if 'lead' in section: pair(section['lead'], p + '.lead')
        array(section['blocks'], p + '.blocks', False)
        for j, item in enumerate(section['blocks']): block(item, f'{p}.blocks[{j}]')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('input'); args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as f: validate_document(json.load(f))
    except (ValueError, OSError) as exc: parser.exit(1, f'Validation failed: {exc}\n')
    print('Valid bilingual document: ' + args.input)


if __name__ == '__main__': main()
