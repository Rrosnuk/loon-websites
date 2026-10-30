# Loon Softworks websites

Source for **loonsoftworks.com** and the app sites **lugnut.**, **calendarcorrector.** and **truffe.loonsoftworks.com** (Cloudflare Pages). Follows `06-website-standard.md` in the App Build playbook.

| Folder | What it is |
|---|---|
| `src/shared/loon.css` | The one design system every site uses (tokens, header, footer, components, light and dark) |
| `src/<site>/pages/*.html` | Page content. File name = `<page-id>.<lang>.html`; pages with the same id are translations of each other (hreflang is automatic) |
| `src/<site>/static/` | Images, icons, feeds copied as-is |
| `src/<site>/redirects.txt` | Becomes `_redirects` (old URLs → new) |
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
Today: from the signed-in Cloudflare dashboard, on each project's *Create deployment → Upload assets* page, load `tools/deploy.js` and run `LOON.stage('<project>')`, then press **Save and deploy**.
Later (recommended): `npx wrangler pages deploy dist/<project> --project-name <project>` with an API token, from a `.command` script or GitHub Actions.

## Rules
- No third-party requests, cookies or analytics (keeps "no cookie banner" true).
- No official store badges until an app is actually live; use the "Coming soon" status pill.
- Every customer-facing page in English and French (Canada); legal pages say both versions are equally authoritative.
- Contact is always support@loonsoftworks.com.
