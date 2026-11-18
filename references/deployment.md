# Deployment and standalone delivery

## Default artifact

One UTF-8 HTML per document. Inline styles/scripts/icons and both languages. No dependencies, account, API or build process needed for local opening. Download HTML creates another complete bilingual artifact. Never serialize private review notes or source JSON.

## Static ZIP

The optional bundle contains only `index.html` and a bilingual README. Upload or extract the bundle into a static document root. Each document has its own standalone file, even if deployed within a larger collection. A collection catalog is optional and must not expose internal metadata without approval.

## Static hosting

Local preview can use Python's standard-library `http.server`; it is not a production recommendation and not proof of live deployment. Before integrating a hosting platform, confirm its documented contract:

- Accepted archive or repository layout and static hosting support
- Upload or deployment command and any required runtime/start command
- Runtime port and route/base-path behavior, if a process is required
- MIME types and cache behavior
- Content security policy and inline CSS/JavaScript compatibility
- Authentication, authorization, and public/private visibility controls

When a process is actually required, add a small static server with verified binding, port, and start rules as an explicit extension. Do not invent platform-specific files, API calls, domains, or environment variables.

## Publication safety

- Obtain separate authorization before uploading, publishing, or sharing generated documents.
- Use credentials only through the hosting platform's documented secure authentication mechanism. Never embed them in HTML, source JSON, logs, command-line arguments, fixtures, or durable notes.
- Preserve server-returned identifiers and URLs rather than deriving them. Persist publication receipts where appropriate.
- Avoid blindly retrying ambiguous upload timeouts; first check whether the original request succeeded.
- Verify the deployed artifact against the approved local HTML, then test controls on the actual host. Upload success alone does not establish CSP compatibility or authorization correctness.
- Scope browser authentication to the intended origin and clear temporary credentials after verification. Never forward credentials across origins.

## Confidentiality

Internal meeting briefs require authenticated restricted hosting. An unlisted URL is not private. A visibility badge is advisory, not access control. Downloaded files include both languages; anyone possessing one can inspect all content. No analytics or third-party script uploads.

## CSP and testing

Inline CSS/JavaScript may need CSP hashes or a platform-approved policy. Do not silently weaken host security. Test the actual host constraints before claiming platform compatibility. Exercise local `file://` opening, offline mode, the actual downloaded file, and served `index.html`. Generating ZIPs never authorizes publishing.
