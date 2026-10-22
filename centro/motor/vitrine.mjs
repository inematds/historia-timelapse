// node vitrine.mjs [--vistas lateral,drone,...] [--luz se|ne] [--ez 1] [--saida ../vitrine] [--prefixo vitrine] [--rotulos 0]
// Captura a vitrine dos marcos (vitrine.html) em JPG, uma imagem por vista. Mesma GPU/flags do render.mjs.
import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const resto = process.argv.slice(2);
const opt = (k, d) => { const i = resto.indexOf(k); return i >= 0 ? resto[i + 1] : d; };
const vistas = opt('--vistas', 'lateral,drone,igreja,nasce,praca,estacao,futuro').match(/\{[^}]*\}|[^,]+/g);   // nomes ou JSON {"xy":[x,y],"zoom","pitch","bearing"}
const saida = path.resolve(aqui, opt('--saida', '../vitrine')); fs.mkdirSync(saida, { recursive: true });
const prefixo = opt('--prefixo', 'vitrine');
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };

const srv = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]), f = path.join(aqui, u === '/' ? 'vitrine.html' : u);
  if (!f.startsWith(aqui)) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); res.end(b); });
}).listen(0, '127.0.0.1');
await new Promise(r => srv.once('listening', r));
const q = new URLSearchParams({ luz: opt('--luz', 'se'), ez: opt('--ez', '1'), rotulos: opt('--rotulos', '1') });
if (opt('--k')) q.set('k', opt('--k'));   // progresso fixo da construção (0..1) para todos os marcos sem k próprio
const url = `http://127.0.0.1:${srv.address().port}/vitrine.html?${q}`;

const browser = await chromium.launch({ args: (process.env.GL || '--use-angle=vulkan --enable-features=Vulkan').split(' ').concat(['--ignore-gpu-blocklist', '--enable-gpu-rasterization']) });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('pageerror', e => console.error('pageerror', e.message));
page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.error(m.type(), m.text().slice(0, 300)); });
const t0 = Date.now();
await page.goto(url);
await page.waitForFunction(() => window.pronto, null, { timeout: 120000 });
await page.evaluate(() => window.pronto);
console.error(`carregado em ${((Date.now() - t0) / 1000).toFixed(1)} s`);
for (const v of vistas) {
  const vista = v.startsWith('{') ? JSON.parse(v) : v;
  await page.evaluate(v => window.render(v), vista);
  await page.evaluate(v => window.render(v), vista);   // 2ª passada: garante malhas e texturas carregadas
  const f = path.join(saida, `${prefixo}_${typeof vista === 'string' ? vista : 'custom'}.jpg`);
  await page.screenshot({ path: f, type: 'jpeg', quality: 92 });
  console.log(f);
}
await browser.close(); srv.close();
