const puppeteer = require('puppeteer');
const path = require('path');

const OUTPUT_DIR = path.resolve(__dirname, '..');

const MANUALS = [
  {
    input:  path.resolve(__dirname, 'templates/odoo.html'),
    output: path.join(OUTPUT_DIR, 'manual_odoo_empleados.pdf'),
    label:  'Manual Odoo Empleados',
  },
  {
    input:  path.resolve(__dirname, 'templates/android.html'),
    output: path.join(OUTPUT_DIR, 'manual_android.pdf'),
    label:  'Manual App Android',
  },
];

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });

  for (const manual of MANUALS) {
    console.log(`⏳  Generando: ${manual.label} ...`);
    const page = await browser.newPage();

    await page.goto(`file://${manual.input}`, { waitUntil: 'networkidle0' });

    // Esperar a que las Google Fonts carguen completamente
    await page.evaluate(() => document.fonts.ready);
    // Pequeña pausa extra para que Tailwind CDN termine de generar las clases
    await new Promise(r => setTimeout(r, 1500));

    await page.pdf({
      path: manual.output,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      scale: 1,
    });

    await page.close();
    console.log(`✅  ${manual.label} → ${manual.output}`);
  }

  await browser.close();
  console.log('\n🎉  PDFs generados correctamente.');
})();
