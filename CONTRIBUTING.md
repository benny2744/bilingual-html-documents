# Contributing

Thank you for improving Bilingual HTML Documents.

## Development setup

Python 3.10 or newer is the only requirement. There are no third-party runtime or test dependencies.

Run the checks before submitting a change:

```bash
python3 scripts/test_documents.py
python3 scripts/validate.py assets/examples/lesson.json
python3 scripts/validate.py assets/examples/meeting.json
```

## Change guidelines

- Preserve offline operation, bilingual completeness, plain-text escaping, and the no-JavaScript fallback.
- Keep output paths safe: rendering must validate first and refuse to overwrite existing files.
- Update the JSON Schema, validator, renderer, tests, and documentation together when changing the input contract.
- Add regression tests for bug fixes and behavioral changes.
- Test visual or interaction changes in both languages and at desktop/mobile widths when possible.
- Prefer small, focused pull requests with a clear rationale.

## Privacy

Use fictional data only in examples, tests, issues, and pull requests. Never submit real student records, personnel reviews, private meeting content, credentials, private hostnames, or personal source paths. Generated HTML contains both languages and is not suitable for redacting secrets by hiding one language.
