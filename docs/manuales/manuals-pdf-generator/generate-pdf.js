const puppeteer = require('puppeteer');
const path = require('path');

const OUTPUT_DIR = path.resolve(__dirname, '..');

const MANUALS = [
  {
    input:  path.resolve(__dirname, 'templates/odoo.html'),
    output: path.join(OUTPUT_DIR, 'manual_odoo_empleados.pdf'),
    label:  'Manual Odoo Empleados',
    coverId: 'cover',
  },
  {
    input:  path.resolve(__dirname, 'templates/android.html'),
    output: path.join(OUTPUT_DIR, 'manual_android.pdf'),
    label:  'Manual App Android',
    coverId: 'cover',
  },
];

// A4 at 96 dpi = 794 x 1123 px
const A4_W = 794;
const A4_H = 1123;

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });

  for (const manual of MANUALS) {
    console.log(`⏳  Generando: ${manual.label} ...`);

    // ── Step 1: render cover as raster image (screen mode) ──────────
    const screenPage = await browser.newPage();
    await screenPage.setViewport({ width: A4_W, height: A4_H, deviceScaleFactor: 2 });
    await screenPage.goto(`file://${manual.input}`, { waitUntil: 'networkidle0' });
    await screenPage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1500));

    const coverB64 = await screenPage.screenshot({
      encoding: 'base64',
      clip: { x: 0, y: 0, width: A4_W, height: A4_H },
    });
    await screenPage.close();

    // ── Step 2: generate PDF with cover replaced by the screenshot ───
    const pdfPage = await browser.newPage();
    await pdfPage.goto(`file://${manual.input}`, { waitUntil: 'networkidle0' });
    await pdfPage.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1500));

    await pdfPage.evaluate(({ coverId, b64 }) => {
      const coverDiv = document.getElementById(coverId);
      if (coverDiv) {
        coverDiv.innerHTML =
          `<img src="data:image/png;base64,${b64}"
                style="display:block;width:210mm;height:297mm;" />`;
        coverDiv.style.cssText =
          'width:210mm;height:297mm;overflow:hidden;page-break-after:always;margin:0;padding:0;';
      }
    }, { coverId: manual.coverId, b64: coverB64 });

    await pdfPage.pdf({
      path: manual.output,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      scale: 1,
    });

    await pdfPage.close();
    console.log(`✅  ${manual.label} → ${manual.output}`);
  }

  await browser.close();
  console.log('\n🎉  PDFs generados correctamente.');
})();
