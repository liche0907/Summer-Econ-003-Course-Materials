const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  fs.mkdirSync('png', { recursive: true });
  for (const f of fs.readdirSync('svg').filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join('svg', f), 'utf8');
    await p.setContent(`<body style="margin:0;background:#00214F">${svg}</body>`);
    await p.waitForTimeout(120);
    await p.screenshot({ path: 'png/' + f.replace('.svg', '.png') });
  }
  await b.close(); console.log('done');
})();
