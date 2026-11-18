# Bilingual HTML Documents

A standalone agent skill and dependency-free Python renderer for turning structured Chinese/English content into polished, offline-ready HTML documents.

It supports lesson guides, meeting briefs, and full bilingual article editions. The generated pages include a language switch, collapsible sections, contents navigation, browser printing, and a **Download HTML** action. CSS, JavaScript, and SVG icons are inline; no CDN, web font, package install, or build step is required.

> **Translation is not performed by the Python code.** An agent or human supplies both `zh` and `en` text in the input JSON. The scripts validate and render that content without calling an LLM or external service.

## Features

- Complete Chinese and English versions in every document
- Warm editorial layout with responsive desktop and mobile navigation
- Lesson, meeting, and exact-source-wording article workflows
- Paragraph, callout, list, table, and external-link blocks
- Strict schema validation and HTML escaping
- Offline operation with no external assets or analytics
- Language preference persistence with a no-JavaScript bilingual fallback
- Accessible controls, keyboard focus styles, reduced-motion support, and print CSS
- Optional deployment ZIP containing only `index.html` and `README.txt`
- Standard-library-only Python 3.10+ implementation and tests

## Quick start

Clone the repository and render the fictional lesson example:

```bash
git clone https://github.com/benny2744/bilingual-html-documents.git
cd bilingual-html-documents
python3 scripts/render.py \
  --input assets/examples/lesson.json \
  --output artifacts/lesson.html \
  --package artifacts/lesson.zip
```

Open `artifacts/lesson.html` directly in a browser. The `--package` argument is optional.

The renderer refuses to overwrite existing files. Choose new output paths or move previous artifacts aside before rerunning a command.

## Install as a Hermes skill

Clone or copy this directory into your configured Hermes skills directory, preserving `SKILL.md` at the skill root. For a typical local installation:

```bash
git clone https://github.com/benny2744/bilingual-html-documents.git \
  ~/.hermes/skills/bilingual-html-documents
```

Reload or restart Hermes if required by your version. The scripts resolve templates relative to their own location, so they can be invoked from any working directory.

The skill instructions are agent-neutral and can also be adapted to other coding agents that can read files, write JSON, run Python, and inspect HTML in a browser.

## Input format

Every reader-facing string is an object with nonempty `zh` and `en` values:

```json
{
  "zh": "学习目标",
  "en": "Learning objective"
}
```

A document has a lowercase slug, a `kind` (`lesson`, `meeting`, or `article`), a visibility label (`student`, `internal`, or `public`), bilingual title and subtitle, metadata, and one or more sections. See:

- [`templates/document.schema.json`](templates/document.schema.json) for the JSON Schema
- [`assets/examples/lesson.json`](assets/examples/lesson.json) for a fictional lesson
- [`assets/examples/meeting.json`](assets/examples/meeting.json) for a fictional meeting
- [`references/article-mode.md`](references/article-mode.md) for exact-wording article editions

### Content blocks

| Type | Purpose |
| --- | --- |
| `paragraph` | A bilingual paragraph |
| `callout` | An informational or warning aside, with an optional title |
| `list` | An ordered or unordered bilingual list |
| `table` | A table with bilingual headers and equally sized rows |
| `links` | Bilingual labels linking to absolute HTTP(S) URLs |

All content is treated as plain text and escaped. Raw HTML and Markdown are not interpreted.

## Validate and test

```bash
python3 scripts/validate.py assets/examples/lesson.json
python3 scripts/validate.py assets/examples/meeting.json
python3 scripts/test_documents.py
```

For real documents, also open the generated HTML in a browser and verify both languages, section navigation, mobile overflow, printing, offline operation, the no-JavaScript fallback, and the actual downloaded HTML file. Automated pair-completeness checks do not replace semantic, source-fidelity, or confidentiality review.

## Repository layout

```text
SKILL.md                         Agent instructions
assets/examples/                Fictional input fixtures
references/                     Content, design, article, and deployment guides
scripts/render.py               HTML and optional ZIP renderer
scripts/validate.py             Strict standard-library validator
scripts/test_documents.py       Behavioral and security-oriented unit tests
templates/document.html         Standalone HTML shell
templates/document.schema.json  Input JSON Schema
```

## Privacy and deployment

- Both languages are embedded in the HTML. Switching or hiding a language is **not** a privacy boundary.
- The `student`, `internal`, and `public` values are labels, not access controls. Internal content requires authenticated hosting.
- Keep private source material, evidence reports, credentials, and review notes out of document JSON and shareable packages.
- Do not upload or publish generated documents without separate authorization.
- Review [`references/deployment.md`](references/deployment.md) before hosting output.

## Contributing

Contributions are welcome. Run the full test suite, keep the renderer dependency-free unless a change is discussed first, and use only fictional content in fixtures and bug reports. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © Benny2744
