# Translating the Truffe website

Truffe is a pet health records app for iPhone and Android, coming soon, from Loon Softworks, an independent studio. You
photograph any vet paper, and Truffe fills in vaccines, due dates, medicines and costs, then reminds you before anything is
due, including the pet licence. The website must read as if a careful native speaker wrote it for pet owners anywhere in the
world, not for one country.

## What to translate, and where to write it

- English source: `/home/claude/loon-websites/src/truffe/i18n/source/pages/<id>.json` (4 files: home, privacy,
  support, terms) and `/home/claude/loon-websites/src/truffe/i18n/source/ui.json` (one string).
- Write to: `/home/claude/loon-websites/src/truffe/i18n/<code>/pages/<id>.json` and `.../i18n/<code>/ui.json`.
- The French site already exists and is a good model for tone and for how the English adapts:
  `/home/claude/loon-websites/src/truffe/pages/*.fr.html`.

Each page JSON has `title`, `description` and `body` (an HTML fragment). Write the same keys in the same shape. Write each
file with Python (`json.dump(..., ensure_ascii=False, indent=1)`) so the JSON is valid. Build the translated body as a
Python string and dump it, rather than hand-typing JSON escapes. Write each page as soon as it's done.

Work in your own scratch folder (for example `/tmp/claude-0/truffe-<your first language code>/`), never in a shared one.

## Rules for the HTML body

- Translate only human-readable text: element text and the values of `alt`, `title`, `aria-label` and `placeholder`.
- Keep every tag, in the same order, with the same `href`, `src`, `id`, `class`, `data-*`, `hreflang` and `type` values.
  Don't add, drop, merge or reorder tags (inline `<strong>`, `<em>`, `<a>`, `<span>` included). Move them within the
  sentence if the grammar needs it, but keep them all. The checker below compares the tag sequence.
- Keep the placeholders `{{EMAIL}}` and `{{UPDATED}}` exactly.
- Keep these unchanged: Truffe, Loon Softworks, App Store, Apple, iPhone, Android, Google Play, iCloud, email addresses,
  URLs, numbers and amounts, and names of laws and agencies (PIPEDA, Law 25, GDPR …). You may add a short explanation in
  brackets.
- App menu names (for example "More → Language and region"): the app's translations into these languages are still being
  made, so translate them naturally, the way the iPhone app would label them in that language, and use the same wording
  every time the same menu appears.
- Pet and veterinary vocabulary: use the words pet owners and vets in that language actually use (vaccine names such as
  rabies, distemper; "licence" means the city or municipal pet licence/registration). Example dog and cat names can stay.
- The comparison table on the home page compares Truffe with other apps: keep its meaning exactly.
- The home page's "44 languages" is the number of languages; keep it.
- Legal pages (`privacy`, `terms`): translate completely and accurately, keep every section, and don't add or soften
  obligations. The build adds a note that the English version applies, so don't add one yourself. For consistent legal
  wording, look at the Calendar Corrector translations of similar text in
  `/home/claude/loon-websites/src/calendarcorrector/i18n/<code>/pages/privacy.json` and `terms.json`.
- Tone: warm, plain and concise, like Apple's own pages in that language. Address the reader the way Calendar Corrector's
  site does in that language (formal or informal "you"; see its translations above) and keep it consistent.
- Right-to-left languages (ar, he, ur): just translate; the build handles direction.

`ui.json` has one key, `help`: the word for "Help" as a menu item (the Help/support page).

## Check your work

After each language, run `python3 /home/claude/site-i18n/check.py /home/claude/loon-websites/src/truffe <code>`. It must
print `OK`. Fix every problem it lists. Then reread the home page in full as a native reader would: missing sentences,
English left behind, awkward machine phrasing.

Only write inside the `i18n/<code>/` folders you were given, plus your own scratch folder. Don't modify anything else,
and don't run git.

## Report

Reply briefly: the checker result for each language, and anything you weren't sure about. Under 100 words.
