"""Every language the sites are published in: the App Store's languages.

code: the app's language code (also the translation folder name), url: the path prefix,
hreflang/html: the language tag, og: the Open Graph locale, name: the language's own name, rtl: right to left.
"""

LANG_INFO = {
    "en": dict(url="", tag="en", og="en_US", name="English"),
    "ar": dict(url="ar", tag="ar", og="ar_AR", name="العربية", rtl=True),
    "bn": dict(url="bn", tag="bn", og="bn_BD", name="বাংলা"),
    "ca": dict(url="ca", tag="ca", og="ca_ES", name="Català"),
    "cs": dict(url="cs", tag="cs", og="cs_CZ", name="Čeština"),
    "da": dict(url="da", tag="da", og="da_DK", name="Dansk"),
    "de": dict(url="de", tag="de", og="de_DE", name="Deutsch"),
    "el": dict(url="el", tag="el", og="el_GR", name="Ελληνικά"),
    "es": dict(url="es", tag="es", og="es_ES", name="Español"),
    "fi": dict(url="fi", tag="fi", og="fi_FI", name="Suomi"),
    "fr": dict(url="fr", tag="fr", og="fr_FR", name="Français"),
    "gu": dict(url="gu", tag="gu", og="gu_IN", name="ગુજરાતી"),
    "he": dict(url="he", tag="he", og="he_IL", name="עברית", rtl=True),
    "hi": dict(url="hi", tag="hi", og="hi_IN", name="हिन्दी"),
    "hr": dict(url="hr", tag="hr", og="hr_HR", name="Hrvatski"),
    "hu": dict(url="hu", tag="hu", og="hu_HU", name="Magyar"),
    "id": dict(url="id", tag="id", og="id_ID", name="Bahasa Indonesia"),
    "it": dict(url="it", tag="it", og="it_IT", name="Italiano"),
    "ja": dict(url="ja", tag="ja", og="ja_JP", name="日本語"),
    "kn": dict(url="kn", tag="kn", og="kn_IN", name="ಕನ್ನಡ"),
    "ko": dict(url="ko", tag="ko", og="ko_KR", name="한국어"),
    "ml": dict(url="ml", tag="ml", og="ml_IN", name="മലയാളം"),
    "mr": dict(url="mr", tag="mr", og="mr_IN", name="मराठी"),
    "ms": dict(url="ms", tag="ms", og="ms_MY", name="Bahasa Melayu"),
    "nb": dict(url="nb", tag="nb", og="nb_NO", name="Norsk bokmål"),
    "nl": dict(url="nl", tag="nl", og="nl_NL", name="Nederlands"),
    "or": dict(url="or", tag="or", og="or_IN", name="ଓଡ଼ିଆ"),
    "pa": dict(url="pa", tag="pa", og="pa_IN", name="ਪੰਜਾਬੀ"),
    "pl": dict(url="pl", tag="pl", og="pl_PL", name="Polski"),
    "pt-BR": dict(url="pt-br", tag="pt-BR", og="pt_BR", name="Português (Brasil)"),
    "pt-PT": dict(url="pt-pt", tag="pt-PT", og="pt_PT", name="Português (Portugal)"),
    "ro": dict(url="ro", tag="ro", og="ro_RO", name="Română"),
    "ru": dict(url="ru", tag="ru", og="ru_RU", name="Русский"),
    "sk": dict(url="sk", tag="sk", og="sk_SK", name="Slovenčina"),
    "sl": dict(url="sl", tag="sl", og="sl_SI", name="Slovenščina"),
    "sv": dict(url="sv", tag="sv", og="sv_SE", name="Svenska"),
    "ta": dict(url="ta", tag="ta", og="ta_IN", name="தமிழ்"),
    "te": dict(url="te", tag="te", og="te_IN", name="తెలుగు"),
    "th": dict(url="th", tag="th", og="th_TH", name="ไทย"),
    "tr": dict(url="tr", tag="tr", og="tr_TR", name="Türkçe"),
    "uk": dict(url="uk", tag="uk", og="uk_UA", name="Українська"),
    "ur": dict(url="ur", tag="ur", og="ur_PK", name="اردو", rtl=True),
    "vi": dict(url="vi", tag="vi", og="vi_VN", name="Tiếng Việt"),
    "zh-Hans": dict(url="zh-hans", tag="zh-Hans", og="zh_CN", name="简体中文"),
    "zh-Hant": dict(url="zh-hant", tag="zh-Hant", og="zh_TW", name="繁體中文"),
}
for _c, _n in {'en': 'English', 'ar': 'Arabic', 'bn': 'Bengali', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'es': 'Spanish', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada', 'ko': 'Korean', 'ml': 'Malayalam', 'mr': 'Marathi', 'ms': 'Malay', 'nb': 'Norwegian', 'nl': 'Dutch', 'or': 'Odia Oriya', 'pa': 'Punjabi', 'pl': 'Polish', 'pt-BR': 'Portuguese Brazil', 'pt-PT': 'Portuguese Portugal', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-Hans': 'Chinese Simplified', 'zh-Hant': 'Chinese Traditional'}.items():
    LANG_INFO[_c]["en_name"] = _n
LANGS = list(LANG_INFO)          # English first, then by code
WORLD = [c for c in LANGS if c != "en"]


def prefix(code):
    """The path prefix for a language: "" for English, "/fr" for French."""
    u = LANG_INFO[code]["url"]
    return f"/{u}" if u else ""


def localize(path, code):
    """/support/ → /fr/support/ (English paths stay as they are)."""
    return prefix(code) + path if path.startswith("/") else path


# The language menu: a search box that narrows the list as you type (by the language's own name, its English name
# or its code), then the list. Without JavaScript the full list still works.
PICKER_JS = """<script>
document.querySelectorAll('.langpick').forEach(function(d){
var q=d.querySelector('input'),items=[].slice.call(d.querySelectorAll('li'));
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
function filter(){var v=norm(q.value.trim());items.forEach(function(li){li.hidden=v&&norm(li.dataset.k).indexOf(v)<0;});}
d.addEventListener('toggle',function(){if(d.open){q.value='';filter();setTimeout(function(){q.focus();},0);}});
q.addEventListener('input',filter);
q.addEventListener('keydown',function(e){
if(e.key==='Enter'){var a=d.querySelector('li:not([hidden]) a');if(a){e.preventDefault();location.href=a.href;}}
if(e.key==='Escape'){d.open=false;d.querySelector('summary').focus();}
if(e.key==='ArrowDown'){var f=d.querySelector('li:not([hidden]) a');if(f){e.preventDefault();f.focus();}}});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.open=false;d.querySelector('summary').focus();}});
document.addEventListener('click',function(e){if(d.open&&!d.contains(e.target))d.open=false;});
});
</script>"""


def picker_items(href_for, current, esc):
    out = []
    for code in LANGS:
        i = LANG_INFO[code]
        cur = ' aria-current="true"' if code == current else ""
        key = esc(f'{i["name"]} {i["en_name"]} {code}')
        out.append(f'<li data-k="{key}"><a href="{href_for(code)}" hreflang="{i["tag"]}" lang="{i["tag"]}"{cur}>{esc(i["name"])}</a></li>')
    return "".join(out)

# "Search languages", the placeholder of the menu's search box, in each language.
SEARCH = {
    "en": "Search languages", "ar": "ابحث عن لغة", "bn": "ভাষা খুঁজুন", "ca": "Cerca un idioma", "cs": "Hledat jazyk",
    "da": "Søg efter sprog", "de": "Sprache suchen", "el": "Αναζήτηση γλώσσας", "es": "Buscar idioma", "fi": "Hae kieltä",
    "fr": "Rechercher une langue", "gu": "ભાષા શોધો", "he": "חיפוש שפה", "hi": "भाषा खोजें", "hr": "Traži jezik",
    "hu": "Nyelv keresése", "id": "Cari bahasa", "it": "Cerca una lingua", "ja": "言語を検索", "kn": "ಭಾಷೆ ಹುಡುಕಿ",
    "ko": "언어 검색", "ml": "ഭാഷ തിരയുക", "mr": "भाषा शोधा", "ms": "Cari bahasa", "nb": "Søk etter språk",
    "nl": "Taal zoeken", "or": "ଭାଷା ଖୋଜନ୍ତୁ", "pa": "ਭਾਸ਼ਾ ਖੋਜੋ", "pl": "Szukaj języka", "pt-BR": "Buscar idioma",
    "pt-PT": "Procurar idioma", "ro": "Caută o limbă", "ru": "Поиск языка", "sk": "Hľadať jazyk", "sl": "Iskanje jezika",
    "sv": "Sök språk", "ta": "மொழியைத் தேடுக", "te": "భాషను వెతకండి", "th": "ค้นหาภาษา", "tr": "Dil ara",
    "uk": "Пошук мови", "ur": "زبان تلاش کریں", "vi": "Tìm ngôn ngữ", "zh-Hans": "搜索语言", "zh-Hant": "搜尋語言",
}


def picker(href_for, current, esc, label, globe):
    """The whole language menu for a page in `current`."""
    return (f'<details class="langpick"><summary aria-label="{esc(label)}">{globe}<span>{esc(LANG_INFO[current]["name"])}</span></summary>'
            f'<div class="langpanel"><input type="search" placeholder="{esc(SEARCH[current])}" aria-label="{esc(SEARCH[current])}" autocomplete="off" spellcheck="false">'
            f'<ul>{picker_items(href_for, current, esc)}</ul></div></details>')
