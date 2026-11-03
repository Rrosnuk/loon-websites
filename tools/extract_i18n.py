"""Write the English text of a site's pages for translation: src/<site>/i18n/source/pages/<id>.json.

    python3 tools/extract_i18n.py calendarcorrector
Each file holds title, description, ogtitle (if any) and body (the page's HTML). Translators write
src/<site>/i18n/<code>/pages/<id>.json with the same keys; build.py turns them into pages at /<code>/<English path>.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"404"}
# Sentences that only make sense in the English and French versions (both are authoritative there; other languages get a
# note that the English version applies instead, added by the build).
EN_ONLY = re.compile(r' (?:Also|This policy is also|These terms are also) available <a href="/fr/[a-z-]+/" hreflang="fr">in French</a>; both versions are equally authoritative\.')

def main(site):
    src = ROOT / "src" / site
    out = src / "i18n" / "source" / "pages"
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted((src / "pages").glob("*.en.html")):
        raw = p.read_text()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        meta = dict((k.strip(), v.strip()) for k, _, v in (l.partition(":") for l in m.group(1).splitlines()))
        pid = p.name[:-8]
        if pid in SKIP:
            continue
        d = {"title": meta["title"], "description": meta.get("description", "")}
        if "ogtitle" in meta:
            d["ogtitle"] = meta["ogtitle"]
        d["body"] = EN_ONLY.sub("", m.group(2))
        (out / f"{pid}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))
        n += 1
    print(n, "pages ->", out)

if __name__ == "__main__":
    main(sys.argv[1])
