const { chromium } = require('playwright');
const [,, base, outDir, ...paths] = process.argv;
(async () => {
  const b = await chromium.launch();
  for (const [w, h, tag, scheme] of [[1280, 900, 'd', 'light'], [390, 844, 'm', 'light'], [1280, 900, 'dk', 'dark']]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, colorScheme: scheme });
    for (const u of paths) {
      await p.goto(base + u, { waitUntil: 'load' });
      const name = (u.replace(/\//g, '_') || '_') + '-' + tag + '.png';
      await p.screenshot({ path: `${outDir}/${name}`, fullPage: true });
      const ov = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      if (ov) console.log('OVERFLOW', u, tag);
    }
    await p.close();
  }
  await b.close();
})();
