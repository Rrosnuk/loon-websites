# Translating the Calendar Corrector website

Calendar Corrector is an app for iPhone, iPad and Mac (by Loon Softworks, an independent studio) that fixes the calendars
people subscribe to. The app is already translated into all of these languages. The website must read as if a careful
native speaker wrote it for readers anywhere in the world, not for one country.

## What to translate, and where to write it

- English source: `/home/claude/loon-websites/src/calendarcorrector/i18n/source/pages/<id>.json` (14 files) and
  `/home/claude/loon-websites/src/calendarcorrector/i18n/source/ui.json`.
- Write to: `/home/claude/loon-websites/src/calendarcorrector/i18n/<code>/pages/<id>.json` and `.../i18n/<code>/ui.json`.
- For French (`fr`) only: write these 10 pages: `press`, `guides` and the 8 `guide-*` files. Skip `home`, `privacy`,
  `support`, `terms` and `ui.json`, which already exist in French. Use the French (Canada) register and wording of
  `/home/claude/loon-websites/src/calendarcorrector/pages/*.fr.html`, the existing French pages.

Each page JSON has `title`, `description`, `body` (an HTML fragment) and sometimes `ogtitle`. Write the same keys in the
same shape. `ui.json` is a flat object of interface strings: translate every value and keep the keys. In it, `updated` is
a date (write it the way the language writes dates), `tm` is Apple's and Google's trademark notice (follow Apple's
wording in that language if you know it), and `{app}` is a placeholder to keep.

Write each file with Python (`json.dump(..., ensure_ascii=False, indent=1)`) so the JSON is valid. Build the translated
body as a Python string and dump it, rather than hand-typing JSON escapes. Work page by page and write each file as soon
as it's done.

## Reuse the earlier translations

An earlier, shorter version of this site was already translated into every language:
`/home/claude/cc-site/i18n/<code>/pages/…` (`index.html.json` = home, `guides/index.html.json` = guides,
`guides/<slug>.html.json` = `guide-<slug>`, `press.html.json`, `privacy.html.json`, `support.html.json`,
`terms.html.json`). The English of those is in `/home/claude/cc-site/i18n/source/pages/`. Most guide sentences are
unchanged. Where a sentence is the same, reuse its earlier translation (after checking it's good); translate new or changed
sentences fresh. The HTML markup is new, so always follow the new English source's tags. The home page is entirely new.

## Rules for the HTML body

- Translate only human-readable text: element text and the values of `alt`, `title`, `aria-label` and `placeholder`.
- Keep every tag, in the same order, with the same `href`, `src`, `id`, `class`, `data-*`, `hreflang` and `type` values.
  Don't add, drop, merge or reorder tags (inline `<strong>`, `<em>`, `<a>`, `<span>` included). Move them within the
  sentence if the grammar needs it, but keep them all. The checker below compares the tag sequence.
- Keep the placeholders `{{EMAIL}}` and `{{UPDATED}}` exactly.
- Keep these unchanged: brand and product names (Calendar Corrector, Loon Softworks, App Store, Apple, iPhone, iPad, Mac,
  iCloud, Google, Outlook, Android, Google Play; "Family Sharing" only as Apple translates it), email addresses, URLs,
  file names (work.ics, school.ics), times and amounts, and names of other apps and services (7shifts, Homebase, When I Work,
  TeamSnap, etc.).
- Example times like "5 PM" or "6:00 AM": write them the way the language does (24-hour clock where that's normal).
- App button, menu and setting names (often in `<strong>`, `<em>` or quoted) must match the app exactly:
  `python3 /home/claude/site-i18n/applabel.py cc <code> "Hide this event" "Holidays where you live"`.
  `--search <word>` lists similar keys if an exact key isn't found. If the app has no such label, translate naturally.
- Example dialog text from the app, such as *"27 shifts end at 6am the next day. End them at 11:30pm instead?"*, should
  follow the app's own wording if `applabel.py --search` finds it; otherwise translate it naturally.
- Legal pages (`privacy`, `terms`): translate completely and accurately, keep every section, and don't add or soften
  obligations. The build adds a note that the English version applies, so don't add one yourself.
- The press page's fact sheet says "44" languages. Keep that number.
- Tone: plain, friendly and concise, like Apple's own help pages in that language. Address the reader exactly as the app
  does (formal or informal "you", polite forms). Check a few app sentences with `applabel.py cc <code> --search your` and
  follow that register throughout.
- Right-to-left languages (ar, he, ur): just translate; the build handles direction.

## Check your work

After each language, run `python3 /home/claude/site-i18n/check.py /home/claude/loon-websites/src/calendarcorrector <code>`.
It must print `OK`, except that for `fr` it will list home/privacy/support/terms/ui.json as missing, which is expected.
Fix every other problem it lists. Then reread two or three translated pages in full as a native reader would, looking for
missing sentences, English left behind, wrong app labels and awkward machine phrasing.

Only write inside the `i18n/<code>/` folders you were given. Don't modify anything else, and don't run git.

## Report

Reply briefly: the checker result for each language, and anything you weren't sure about (for example an app label with
no translation, or a legal term with two possible renderings). Keep it under 120 words.
