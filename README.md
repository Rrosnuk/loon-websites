# Loon Softworks websites

Source for **loonsoftworks.com** and the app sites **lugnut.**, **calendarcorrector.** and **truffe.loonsoftworks.com** (Cloudflare Pages). Follows `06-website-standard.md` in the App Build playbook.

| Folder | What it is |
|---|---|
| `src/shared/loon.css` | The one design system every site uses (tokens, header, footer, components, light and dark) |
| `src/<site>/pages/*.html` | Page content. File name = `<page-id>.<lang>.html`; pages with the same id are translations of each other (hreflang is automatic) |
| `src/<site>/static/` | Images, icons, feeds copied as-is |
| `src/<site>/redirects.txt` | Becomes `_redirects` (old URLs → new) |
| `src/truffe/truffe.css` | Truffe's own look (cream paper, espresso ink, violet accent, Fraunces headings, Maymay and Murphy portraits). The build adds it to the shared file, drops rules Truffe never uses and minifies, so Truffe's `loon.css` stays under 25 KB |
| `src/truffe/home-extra.json` | Text of the Meet Maymay and Murphy and Pricing sections, per language; a language without an entry simply doesn't show them (and its menu has no Pricing link) |
| `src/truffe/mascot-names.json` | Maymay's and Murphy's names in every language, copied from the app's `brand/*/a11y-names.json` |
| `tools/truffe_assets.py` | Makes the round mascot portraits and the header wordmark mask from the app's `brand/` folder |
| `src/lugnut/lugnut.css` | Lugnut's page components; Lugnut pages are re-skinned at deploy (see `tools/deploy.js`) |
| `src/remote-assets.json` | Files the build machine can't download (App Store screenshots); the browser fetches them at deploy |
| `dist/` | Built output, one folder per Cloudflare Pages project, plus `manifest.json` |
| `tools/` | `render_assets.js` (OG images, touch icons), `shoot.js` (screenshots), `deploy.js` (browser deploy helper) |

## Build
```
node tools/render_assets.js   # only when names, taglines or icons change
python3 build.py
```

## Deploy
**Live state (2 November 2026), read before deploying:**
- `truffe`: built from this repo, in all 45 app languages (English plus 44 translations in `src/truffe/i18n/<code>/`). The site says 45 languages, matching the app.
- `calendarcorrector`: built from this repo, in all 44 App Store languages (translations in `src/calendarcorrector/i18n/<code>/`, English source text from `python3 tools/extract_i18n.py calendarcorrector`). Deploy `dist/calendarcorrector` plus the App Store screenshots in `src/remote-assets.json`.
- `loonsoftworks`: the live home page is the 44-language redesign (built outside this repo, with the studio privacy, accessibility and legal pages from `dist/loonsoftworks` added). **Don't deploy `dist/loonsoftworks` on its own**: it would replace the 44-language home with the English/French one.
- `lugnutapp`: the live Lugnut site is the 44-language build with a searchable language menu and a Loon Softworks footer column. **Don't run `LOON.stage('lugnutapp')`**: the re-skin only knows en/fr/es/de and would break the language menu.

Dashboard uploads (`LOON.stage`) stopped working on 2 November 2026 (Cloudflare answers "Authorization failed" when checking files). What works: Wrangler from the Mac, `npx --yes wrangler@4 pages deploy <folder> --project-name <project> --branch main` (sign in once with `npx --yes wrangler@4 login`).

## Rules
- No third-party requests, cookies or analytics (keeps "no cookie banner" true).
- No official store badges until an app is actually live; use the "Coming soon" status pill.
- Every customer-facing page in English and French (Canada); legal pages say both versions are equally authoritative.
- Contact is always support@loonsoftworks.com.
