// Loon Softworks website deploy helper. Runs inside the Cloudflare dashboard tab (signed in by Rayn),
// on the project's "Upload assets" page: https://dash.cloudflare.com/<account>/pages/view/<project>/deployments/new
// Load:  (0,eval)(await (await fetch(RAW+'tools/deploy.js',{cache:'no-store'})).text())
// Use:   await LOON.stage('truffe')   -> builds the zip and puts it in the upload box (does not click deploy)
window.LOON = (() => {
  const RAW = 'https://raw.githubusercontent.com/Rrosnuk/loon-websites/main/';
  const ACCOUNT = '629529b97761dc8207359cacd5a5690d';
  const HOSTS = { lugnutapp: 'https://lugnutapp.pages.dev' };
  const api = (p) => fetch('/api/v4/accounts/' + ACCOUNT + '/pages/projects/' + p, { credentials: 'include', headers: { 'x-cross-site-security': 'dash' } }).then(r => r.json());
  const get = async (u) => { const r = await fetch(u, { cache: 'no-store' }); if (!r.ok) throw new Error(u + ' ' + r.status); return new Uint8Array(await r.arrayBuffer()); };
  const dec = new TextDecoder(), enc = new TextEncoder();

  // ---- zip (store only) ----
  const T = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc = (u8) => { let c = 0xFFFFFFFF; for (let i = 0; i < u8.length; i++) c = T[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  const zip = (entries) => { const parts = [], central = []; let off = 0; for (const e of entries) { const nm = enc.encode(e.name), c = crc(e.data), sz = e.data.length; const lh = new DataView(new ArrayBuffer(30)); lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true); lh.setUint16(12, 0x21, true); lh.setUint32(14, c, true); lh.setUint32(18, sz, true); lh.setUint32(22, sz, true); lh.setUint16(26, nm.length, true); parts.push(new Uint8Array(lh.buffer), nm, e.data); const ch = new DataView(new ArrayBuffer(46)); ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true); ch.setUint16(8, 0x0800, true); ch.setUint16(14, 0x21, true); ch.setUint32(16, c, true); ch.setUint32(20, sz, true); ch.setUint32(24, sz, true); ch.setUint16(28, nm.length, true); ch.setUint32(42, off, true); central.push(new Uint8Array(ch.buffer), nm); off += 30 + nm.length + sz; } const cd = central.reduce((a, b) => a + b.length, 0); const end = new DataView(new ArrayBuffer(22)); end.setUint32(0, 0x06054b50, true); end.setUint16(8, entries.length, true); end.setUint16(10, entries.length, true); end.setUint32(12, cd, true); end.setUint32(16, off, true); return new Blob([...parts, ...central, new Uint8Array(end.buffer)], { type: 'application/zip' }); };

  // ---- built sites from GitHub ----
  async function builtEntries(project) {
    const m = JSON.parse(dec.decode(await get(RAW + 'dist/manifest.json')));
    const entries = [];
    for (const f of m[project]) entries.push({ name: f, data: await get(RAW + 'dist/' + project + '/' + f) });
    for (const [k, url] of Object.entries(m._remote || {})) {
      if (!k.startsWith(project + '/')) continue;
      entries.push({ name: k.slice(project.length + 1), data: await get(url) });
    }
    return entries;
  }

  // ---- Lugnut re-skin ----
  function lugnutTransform(path, src, C) {
    const doc = new DOMParser().parseFromString(src, 'text/html');
    const root = doc.documentElement;
    const lang = (root.getAttribute('lang') || 'en').slice(0, 2);
    const L = C.langs[lang] || C.langs.en;
    root.setAttribute('data-site', 'lugnut');
    const head = doc.head;
    head.querySelectorAll('link[rel=preload][as=font]').forEach(e => e.remove());
    const css = head.querySelector('link[rel=stylesheet]'); if (css) css.setAttribute('href', '/site.css?v=' + C.cssHash);
    if (!head.querySelector('meta[name=color-scheme]')) { const m = doc.createElement('meta'); m.name = 'color-scheme'; m.content = 'light dark'; head.querySelector('meta[name=viewport]').after(m); }
    if (/^\/((fr|es|de)\/)?index\.html$/.test(path)) {
      doc.title = L.homeTitle;
      const ogt = head.querySelector('meta[property="og:title"]'); if (ogt) ogt.content = L.homeTitle;
    }
    head.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
      try { const j = JSON.parse(s.textContent); if (j.author) { delete j.author; j.publisher = { '@type': 'Organization', name: 'Loon Softworks', url: 'https://loonsoftworks.com/', email: C.email }; s.textContent = JSON.stringify(j); } } catch (e) { }
    });
    const body = doc.body;
    // Android note
    const oldNote = doc.getElementById('android-note'); if (oldNote) oldNote.remove();
    body.querySelectorAll('script:not([src])').forEach(s => { if (s.textContent.includes('android-note')) s.remove(); });
    // Header
    const oldHeader = body.querySelector('header.band');
    const home = lang === 'en' ? '/' : '/' + lang + '/';
    if (oldHeader) {
      const nav = [...oldHeader.querySelectorAll('nav a')].map(a => `<li><a href="${a.getAttribute('href')}"${a.getAttribute('aria-current') ? ' aria-current="page"' : ''}>${a.textContent.trim()}</a></li>`).join('');
      const langs = [...oldHeader.querySelectorAll('.langs a')].map(a => { const l = a.getAttribute('hreflang'); return `<li><a href="${a.getAttribute('href')}" hreflang="${l}" lang="${C.htmlLang[l]}"${l === lang ? ' aria-current="true"' : ''}>${C.names[l]}</a></li>`; }).join('');
      const h = doc.createElement('header'); h.className = 'site-header';
      h.innerHTML = `<div class="wrap bar"><a class="brand" href="${home}"><img src="/favicon.svg" alt="" width="32" height="32"><span>Lugnut</span></a><nav class="primary" aria-label="${oldHeader.querySelector('nav')?.getAttribute('aria-label') || 'Main'}"><ul>${nav}</ul></nav><details class="lang"><summary aria-label="${L.language}: ${C.names[lang]}">${C.globe}<span>${C.names[lang]}</span></summary><ul>${langs}</ul></details></div>`;
      oldHeader.replaceWith(h);
      // keep the language list for the footer
      h.dataset.langs = langs;
    }
    const skip = body.querySelector('a.skip'); if (skip) skip.textContent = L.skip;
    const note = doc.createElement('div'); note.className = 'android-note'; note.id = 'android-note'; note.hidden = true;
    note.innerHTML = `${L.android[0]} <a href="mailto:${C.email}?subject=${encodeURIComponent(L.android[2])}">${L.android[1]}</a>`;
    body.prepend(note);
    // Store buttons -> honest status pill
    body.querySelectorAll('.cta').forEach(cta => {
      const stores = cta.querySelectorAll('.btn-store'); if (!stores.length) return;
      const pill = doc.createElement('span'); pill.className = 'status'; pill.textContent = L.status;
      stores[0].before(pill); stores.forEach(s => s.remove());
    });
    // Footer
    const oldFooter = body.querySelector('footer.site');
    if (oldFooter) {
      const cols = [...oldFooter.querySelectorAll('.cols > div')].map(d => {
        const items = [...d.querySelectorAll('li')].filter(li => !/impressum/.test(li.querySelector('a')?.getAttribute('href') || '')).map(li => `<li>${li.innerHTML}</li>`).join('');
        return `<div><h2>${d.querySelector('.h')?.textContent || ''}</h2><ul>${items}</ul></div>`;
      }).join('');
      const legal = `<div><h2>${L.legalTitle}</h2><ul>${L.legalLinks.map(([t, u]) => `<li><a href="${u}">${t}</a></li>`).join('')}</ul></div>`;
      const studio = `<div><h2><a class="studio-mark" href="${L.about[1]}">Loon Softworks</a></h2><ul>${L.studioItems.map(([t, u]) => `<li><a href="${u}">${t}</a></li>`).join('')}<li><a href="${L.about[1]}">${L.about[0]}</a></li></ul></div>`;
      const langCol = `<div><h2>${L.language}</h2><ul>${body.querySelector('header.site-header')?.dataset.langs || ''}</ul></div>`;
      let disclaimer = (oldFooter.querySelector('.legal p')?.textContent || '').replace(/^©\s*\d{4}\s*Lugnut\.\s*/, '');
      const cut = disclaimer.search(/Apple,?\s/); if (cut > 0) disclaimer = disclaimer.slice(0, cut).trim();
      const f = doc.createElement('footer'); f.className = 'site-footer';
      f.innerHTML = `<div class="wrap cols">${cols}${legal}${studio}${langCol}</div><div class="wrap fineprint"><p>${L.fineprint[0]}</p>${disclaimer ? `<p>${disclaimer}</p>` : ''}<p>${L.fineprint[1]}</p><p>${L.fineprint[2]}</p></div>`;
      oldFooter.replaceWith(f);
    }
    body.querySelector('header.site-header')?.removeAttribute('data-langs');
    const js = doc.createElement('script'); js.src = '/site.js'; js.defer = true; body.append(js);
    return '<!doctype html>\n' + root.outerHTML + '\n';
  }

  async function lugnutEntries() {
    const C = JSON.parse(dec.decode(await get(RAW + 'dist/lugnutapp-overlay/chrome.json')));
    const d = await api('lugnutapp/deployments?per_page=1&env=production');
    const full = await api('lugnutapp/deployments/' + d.result[0].id);
    const entries = [], changed = [];
    for (const f of Object.keys(full.result.files)) {
      if (f.startsWith('/fonts/')) continue;           // system fonts now
      if (f === '/site.css') continue;                 // replaced below
      let u8 = await get(HOSTS.lugnutapp + f);
      if (/\.html$/.test(f)) { const t = dec.decode(u8); const t2 = lugnutTransform(f, t, C); if (t2 !== t) changed.push(f); u8 = enc.encode(t2); }
      entries.push({ name: f.slice(1), data: u8 });
    }
    entries.push({ name: 'site.css', data: await get(RAW + 'dist/lugnutapp-overlay/site.css') });
    entries.push({ name: 'site.js', data: await get(RAW + 'dist/lugnutapp-overlay/site.js') });
    for (const ic of ['lugnut-icon.svg', 'calendar-icon.svg', 'truffe-icon.svg']) entries.push({ name: 'img/' + ic, data: await get(RAW + 'dist/lugnutapp-overlay/' + ic) });
    return { entries, changed };
  }

  async function stage(project) {
    let entries, changed = [];
    if (project === 'lugnutapp') ({ entries, changed } = await lugnutEntries()); else entries = await builtEntries(project);
    const z = zip(entries);
    const inp = [...document.querySelectorAll('input[type=file]')].find(i => i.accept === '.zip');
    if (!inp) return { error: 'upload input not found on this page' };
    const dt = new DataTransfer(); dt.items.add(new File([z], project + '.zip', { type: 'application/zip' })); inp.files = dt.files; inp.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(r => setTimeout(r, 6000));
    const status = (document.querySelector('main')?.innerText.match(/\d+\/\d+ files uploaded|All files were successfully uploaded\.|error[^\n]*/gi) || []);
    return { project, files: entries.length, bytes: z.size, changed: changed.length, status };
  }

  return { RAW, stage, lugnutTransform, builtEntries, lugnutEntries, zip };
})();
'loaded';
