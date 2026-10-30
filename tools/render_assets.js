// Renders og images (1200x630) and apple-touch-icons (180x180) with the local Chromium.
// Truffe's come from its logo: furry-friends/brand/make_brand_assets.py --web <this repo>.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const root = path.resolve(__dirname, '..');
const sites = {
  studio:   { name: 'Loon Softworks', line: 'Small, careful apps from Ontario', accent: '#0f2a3a', icon: 'loon-mark.svg', ogOut: 'src/studio/static/og.png', touchOut: 'src/studio/static/apple-touch-icon.png', bg:'#f5f6f7' },
  calendar: { name: 'Calendar Corrector', line: 'Edit the calendars you subscribe to.', accent: '#1d4ed8', icon: 'calendar-icon.svg', ogOut: 'src/calendarcorrector/static/img/og.png', touchOut: 'src/calendarcorrector/static/apple-touch-icon.png', bg:'#eef3ff' },
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const s of Object.values(sites)) {
    const svg = fs.readFileSync(path.join(root, 'src/shared', s.icon), 'utf8');
    const uri = 'data:image/svg+xml;base64,' + Buffer.from(svg).toString('base64');
    await p.setViewportSize({ width: 1200, height: 630 });
    await p.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:${s.bg};font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 96px;box-sizing:border-box">
      <img src="${uri}" style="width:132px;height:132px;border-radius:30px;margin-bottom:40px">
      <div style="font-size:76px;font-weight:700;letter-spacing:-.03em;color:#111316;line-height:1.05">${s.name}</div>
      <div style="font-size:40px;color:#3d424a;margin-top:18px;letter-spacing:-.01em">${s.line}</div>
      <div style="position:absolute;bottom:56px;left:96px;font-size:26px;color:${s.accent};font-weight:600">loonsoftworks.com</div></body></html>`);
    fs.mkdirSync(path.dirname(path.join(root, s.ogOut)), { recursive: true });
    await p.screenshot({ path: path.join(root, s.ogOut) });
    await p.setViewportSize({ width: 180, height: 180 });
    await p.setContent(`<html><body style="margin:0;background:${s.accent}"><img src="${uri}" style="width:180px;height:180px;display:block"></body></html>`);
    await p.screenshot({ path: path.join(root, s.touchOut) });
  }
  await b.close(); console.log('rendered');
})();
