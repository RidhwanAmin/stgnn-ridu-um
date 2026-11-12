// Approximate preview of deck slides at 1920x1080 and a content-bottom check.
// Usage: node render_slides.js <slides_dir> <out_dir> <slide-id> [<slide-id> ...]
// Limits: main slides (padding-bottom 140px) content bottom <= 940; appendix (120px) <= 960.
// Absolutely positioned elements (page number) are ignored. This is NOT the Slides artifact renderer;
// always check the published deck too.
const {chromium} = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [dir, out, ...ids] = process.argv.slice(2);
  fs.mkdirSync(out, {recursive: true});
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1920, height: 1080}});
  for (const id of ids) {
    const sec = fs.readFileSync(path.join(dir, id + '.html'), 'utf8').replace(/<aside>[\s\S]*?<\/aside>/, '');
    await p.setContent('<html><body style="margin:0"><style>section{box-sizing:border-box;width:1920px;height:1080px;position:relative;overflow:hidden} *{margin:0} section *{box-sizing:border-box} table{border-collapse:collapse} td,th{border:1px solid #8a8a8a;padding:8px 12px;vertical-align:top}</style>' + sec + '</body></html>');
    const r = await p.evaluate(() => { const s = document.querySelector('section'); let m = 0;
      s.querySelectorAll('*').forEach(e => { if (getComputedStyle(e).position === 'absolute' || e.closest('[style*="position:absolute"]')) return;
        const q = e.getBoundingClientRect(); if (q.bottom > m) m = q.bottom; }); return Math.round(m); });
    const limit = id.startsWith('app-') ? 960 : 940;
    console.log(id.padEnd(22), 'content bottom', r, r > limit ? 'OVER' : 'ok');
    await p.screenshot({path: path.join(out, id + '.png')});
  }
  await b.close();
})();
