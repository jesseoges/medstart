# MedStart article publishing

- `articles.html` now loads public published articles from Firestore.
- The private Studio includes a server-side Firebase Cloud Function that creates `articles/<slug>.html` in this repository after publishing.
- Deploy the function and configure its server-side GitHub token and repository parameters using the Studio `SETUP.md`.
- The vertical navigation is intentionally always open and stacked vertically across all pages, including phones.
- Do not put a GitHub token in any HTML or browser JavaScript.
