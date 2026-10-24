// node render.mjs <pasta-da-cena (tem cena.js)> <saida.mp4 | --quadros t1,t2,...> [--fps 30] [--de s] [--ate s]
// node render.mjs <pasta-da-cena> --camada <pasta-saida> [--de s] [--ate s] [--quadros t1,t2]: modo luz real (Mitsuba):
//   grava c_NNNNN.png (camada transparente) + info.jsonl (câmera e ano de cada quadro) para scripts/mitsuba_render.py.
// Serve o motor por HTTP local (fetch de binários não funciona em file://) e captura quadro a quadro.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const [, , pasta, saida, ...resto] = process.argv;
const opt = k => { const i = resto.indexOf(k); return i >= 0 ? resto[i + 1] : null; };
const fps = Number(opt('--fps') || 30);
const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };

const srv = http.createServer((req, res) => {
  const u = decodeURIComponent(req.url.split('?')[0]);
  const daCidade = u.startsWith('/assets/') ? path.resolve(pasta, '..', u.slice(1)) : null;
  const f = u === '/cena.js' ? path.resolve(pasta, 'cena.js')
    : (daCidade && fs.existsSync(daCidade)) ? daCidade : path.join(aqui, u === '/' ? 'mapa.html' : u);
  if (!f.startsWith(aqui) && !f.startsWith(path.resolve(pasta, '..'))) { res.writeHead(403); return res.end(); }
  fs.readFile(f, (e, b) => { if (e) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f)] || 'application/octet-stream' }); res.end(b); });
}).listen(0, '127.0.0.1');
await new Promise(r => srv.once('listening', r));
const url = `http://127.0.0.1:${srv.address().port}/`;

const browser = await chromium.launch({ args: (process.env.GL || '--use-angle=vulkan --enable-features=Vulkan').split(' ')
  .concat(['--ignore-gpu-blocklist', '--enable-gpu-rasterization']) });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('pageerror', e => console.error('pageerror', e.message));
page.on('console', m => { if (m.type() === 'error') console.error('console', m.text()); });
const t0 = Date.now();
await page.goto(saida === '--camada' ? url + '?camada' : url);
await page.waitForFunction(() => window.pronto, null, { timeout: 120000 });
await page.evaluate(() => window.pronto);
console.error(`carregado em ${((Date.now() - t0) / 1000).toFixed(1)} s`);
const dur = await page.evaluate(() => window.CENA.duracao);

if (saida === '--camada') {
  const dir = path.resolve(resto[0]); fs.mkdirSync(dir, { recursive: true });
  const qs = opt('--quadros');
  const lista = qs ? qs.split(',').map(x => Math.round(Number(x) * fps))
    : (() => { const a = []; for (let i = Math.round(Number(opt('--de') || 0) * fps); i < Math.round(Number(opt('--ate') || dur) * fps); i++) a.push(i); return a; })();
  const info = fs.createWriteStream(path.join(dir, 'info.jsonl'), { flags: 'a' }); const ti = Date.now();
  for (const [k, i] of lista.entries()) {
    await page.evaluate(t => window.render(t), i / fps);
    if (qs) await page.evaluate(t => window.render(t), i / fps);
    await page.screenshot({ path: path.join(dir, `c_${String(i).padStart(5, '0')}.png`), omitBackground: true });
    info.write(JSON.stringify({ i, ...(await page.evaluate(() => window.INFO)) }) + '\n');
    if (k % 30 === 0) process.stderr.write(`quadro ${k}/${lista.length} ${((Date.now() - ti) / 1000 / (k + 1)).toFixed(2)} s/quadro\n`);
  }
  await new Promise(r => info.end(r));
} else if (saida === '--quadros') {
  const ts = (opt('--quadros') || resto[0]).split(',').map(Number);
  for (const t of ts) {
    await page.evaluate(t => window.render(t), t);
    await page.evaluate(t => window.render(t), t); // 2ª passada: garante teto/filtros aplicados
    const f = path.resolve(pasta, `q_${String(t).replace('.', '_')}.jpg`);
    await page.screenshot({ path: f, type: 'jpeg', quality: 90 });
    console.log(f);
  }
} else {
  const de = Number(opt('--de') || 0), ate = Number(opt('--ate') || dur);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', saida], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n0 = Math.round(de * fps), n1 = Math.round(ate * fps); const ti = Date.now();
  for (let i = n0; i < n1; i++) {
    await page.evaluate(t => window.render(t), i / fps);
    const b = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r));
    if ((i - n0) % 30 === 0) process.stderr.write(`quadro ${i - n0}/${n1 - n0} ${((Date.now() - ti) / 1000 / (i - n0 + 1)).toFixed(2)} s/quadro\n`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.error(`ok ${saida}`);
}
await browser.close(); srv.close();
