// marcos.js — marcos históricos, árvores e cidade futura como malhas paramétricas (SimpleMeshLayer, deck.gl 9.0.38).
// Carregar depois de deck.min.js. API em window.MARCOS (documentada em centro/DESIGN-PREDIOS.md).
// Convenções: malha em METROS locais (x leste, y norte, z para cima), origem no centro do lote, no chão.
// A fachada (frente) é construída olhando para −y; `rumo` (graus, horário a partir do norte) gira o prédio
// de modo que a frente aponte para esse azimute. Alturas multiplicam `ez` (padrão C.exb); z do chão multiplica C.exz.
(function () {
'use strict';
const deck = window.deck;
const rad = Math.PI / 180;
const clamp01 = k => Math.max(0, Math.min(1, k));
const ease = k => { k = clamp01(k); return k * k * (3 - 2 * k); };
const lerp = (a, b, k) => a + (b - a) * k;
const hex = h => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
const esc = (c, f) => [c[0] * f, c[1] * f, c[2] * f];
const mix = (a, b, k) => [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)];
const c255 = c => [Math.round(c[0] * 255), Math.round(c[1] * 255), Math.round(c[2] * 255)];

// ---------------------------------------------------------------- paleta (0..1) — ver DESIGN-PREDIOS.md
const P = {
  cal: hex('#EAE3D4'),        // parede caiada (não é branco puro: não estoura na luz)
  calSombra: hex('#D8D0C0'),
  soco: hex('#8F8477'),       // embasamento de pedra
  pedra: hex('#A8A196'),      // adro, escadas, laje
  azul: hex('#2E5E8E'),       // molduras e cunhais coloniais
  vinho: hex('#7B3038'),
  verde: hex('#2F6B4F'),
  ardosia: hex('#4A5560'),    // coruchéu, ferro pintado
  branco: hex('#F2EDE3'),     // molduras brancas (eclético)
  rosa: hex('#D8B4A2'),       // parede rosa-antigo (prefeitura eclética)
  creme: hex('#E6CDB3'),      // parede da estação
  tijolo: hex('#8C3B2E'),     // molduras da estação
  telha: hex('#A9533A'), telha2: hex('#964832'), telhaSombra: hex('#7E3B27'), cumeeira: hex('#7E3C28'),
  testeira: hex('#7A5A48'), sofito: hex('#5E4A3E'),
  vidro: hex('#26303A'),      // vão escuro (janela)
  veneziana: hex('#2F4A3B'),
  madeira: hex('#4A3324'),
  ferro: hex('#3A3F45'), zinco: hex('#9AA2A8'), zinco2: hex('#8A9298'),
  lastro: hex('#7D7468'), dormente: hex('#5A4636'), trilho: hex('#555B61'), concreto: hex('#BFC3C5'),
  tronco: hex('#6F4E34'), copa: hex('#4F8F3F'), copa2: hex('#3E7A33'), copa3: hex('#5FA04A'),
  palmaTronco: hex('#8A7A64'), palma: hex('#4C8A3A'), palma2: hex('#3C7530'),
  // futuro
  vidroFut: hex('#7FB6CF'), vidroFut2: hex('#5F97B3'), aco: hex('#D3D8DC'), aco2: hex('#B6BDC2'),
  concretoFut: hex('#C9CCCB'), telhadoVerde: hex('#5C9A48'), telhadoVerde2: hex('#4E8A3E'),
  solar: hex('#1E2F5E'), solarMoldura: hex('#C9CFD3'),
  leito: hex('#B9BCB8'), bonde: hex('#F2F4F5'), bondeFaixa: hex('#1F7A8C'), bondeVidro: hex('#2B3A44'),
  grama: hex('#5F9C4C'), caminho: hex('#D9CDB3'), agua: hex('#4B8FC2'), ciclovia: hex('#9B4A3B'),
  ocre: hex('#B3782A'),       // molduras ocre (foto da Coletânea) — queimado, distinto do amarelo de destaque
  ocreParede: hex('#CFA34B'), // parede amarelo-ocre (estação-castelo, corpo central da catedral)
  prata: hex('#CDD1D6'), prata2: hex('#A9AFB6'),   // cúpula "meia-laranja" de zinco
  verdeEscuro: hex('#4F6358'), vitral: hex('#3C7FA6'), bronze: hex('#6B5A3A'), claro: hex('#E8E4DA'),
  amb: hex('#FACC15'),
};
const AMB = [250, 204, 21];

// ---------------------------------------------------------------- Malha: triângulos soltos com normal e cor por vértice
class Malha {
  constructor() { this.p = []; this.n = []; this.c = []; }
  // tri com normal calculada; `ref` = ponto de referência: a normal aponta para longe dele (ou para ele, se `dentro`)
  tri(a, b, c, cor, ref, dentro) {
    const ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const l = Math.hypot(nx, ny, nz); if (l < 1e-9) return; nx /= l; ny /= l; nz /= l;
    if (ref) {
      const mx = (a[0] + b[0] + c[0]) / 3 - ref[0], my = (a[1] + b[1] + c[1]) / 3 - ref[1], mz = (a[2] + b[2] + c[2]) / 3 - ref[2];
      const d = nx * mx + ny * my + nz * mz;
      if ((d < 0) !== !!dentro) { const t = b; b = c; c = t; nx = -nx; ny = -ny; nz = -nz; }
    }
    this.p.push(a[0], a[1], a[2], b[0], b[1], b[2], c[0], c[1], c[2]);
    this.n.push(nx, ny, nz, nx, ny, nz, nx, ny, nz);
    this.c.push(cor[0], cor[1], cor[2], cor[0], cor[1], cor[2], cor[0], cor[1], cor[2]);
  }
  quad(a, b, c, d, cor, ref, dentro) { this.tri(a, b, c, cor, ref, dentro); this.tri(a, c, d, cor, ref, dentro); }
  poli(pts, cor, ref, dentro) { for (let i = 1; i < pts.length - 1; i++) this.tri(pts[0], pts[i], pts[i + 1], cor, ref, dentro); }
  // caixa alinhada aos eixos; cores: {lado, topo, fundo} ou uma cor
  caixa(x0, x1, y0, y1, z0, z1, cores) {
    const C = cores.lado ? cores : { lado: cores, topo: cores, fundo: cores };
    const ref = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2];
    this.quad([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], C.topo || C.lado, ref);
    this.quad([x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [x1, y0, z0], C.fundo || C.lado, ref);
    this.quad([x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], C.lado, ref);
    this.quad([x1, y1, z0], [x0, y1, z0], [x0, y1, z1], [x1, y1, z1], C.lado, ref);
    this.quad([x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [x1, y0, z1], C.lado, ref);
    this.quad([x0, y1, z0], [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], C.lado, ref);
  }
  // prisma vertical de um polígono convexo 2D ([[x,y],...]), de z0 a z1
  prisma(pol, z0, z1, corLado, corTopo, corFundo) {
    const n = pol.length; let cx = 0, cy = 0; for (const p of pol) { cx += p[0]; cy += p[1]; } cx /= n; cy /= n;
    const ref = [cx, cy, (z0 + z1) / 2];
    for (let i = 0; i < n; i++) { const a = pol[i], b = pol[(i + 1) % n];
      this.quad([a[0], a[1], z0], [b[0], b[1], z0], [b[0], b[1], z1], [a[0], a[1], z1], corLado, ref); }
    this.poli(pol.map(p => [p[0], p[1], z1]), corTopo || corLado, ref);
    if (corFundo !== null) this.poli(pol.map(p => [p[0], p[1], z0]), corFundo || corLado, ref);
  }
  // pirâmide (ou cone) sobre polígono convexo
  piramide(pol, z0, apice, cor) {
    const n = pol.length; let cx = 0, cy = 0; for (const p of pol) { cx += p[0]; cy += p[1]; } cx /= n; cy /= n;
    const ref = [cx, cy, z0], top = [apice[0], apice[1], apice[2]];
    for (let i = 0; i < n; i++) { const a = pol[i], b = pol[(i + 1) % n]; this.tri([a[0], a[1], z0], [b[0], b[1], z0], top, cor, ref); }
  }
  // barra: caixa ao longo do segmento p0→p1 (3D), seção w (horizontal) × h (vertical), segmento no centro da seção
  barra(p0, p1, w, h, cor) {
    let dx = p1[0] - p0[0], dy = p1[1] - p0[1], dz = p1[2] - p0[2]; const l = Math.hypot(dx, dy, dz) || 1; dx /= l; dy /= l; dz /= l;
    let sx = dy, sy = -dx, sz = 0; const sl = Math.hypot(sx, sy) || 1; sx /= sl; sy /= sl;   // lado horizontal
    if (Math.abs(dz) > 0.999) { sx = 1; sy = 0; }
    const ux = sy * dz - sz * dy, uy = sz * dx - sx * dz, uz = sx * dy - sy * dx;             // "para cima" da seção
    const v = (p, s, u) => [p[0] + sx * s + ux * u, p[1] + sy * s + uy * u, p[2] + sz * s + uz * u];
    const ref = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2];
    const a0 = v(p0, -w / 2, -h / 2), a1 = v(p0, w / 2, -h / 2), a2 = v(p0, w / 2, h / 2), a3 = v(p0, -w / 2, h / 2);
    const b0 = v(p1, -w / 2, -h / 2), b1 = v(p1, w / 2, -h / 2), b2 = v(p1, w / 2, h / 2), b3 = v(p1, -w / 2, h / 2);
    this.quad(a0, a1, a2, a3, cor, ref); this.quad(b0, b1, b2, b3, cor, ref);
    this.quad(a0, b0, b1, a1, cor, ref); this.quad(a1, b1, b2, a2, cor, ref); this.quad(a2, b2, b3, a3, cor, ref); this.quad(a3, b3, b0, a0, cor, ref);
  }
  junta(o) { for (const k of ['p', 'n', 'c']) for (let i = 0; i < o[k].length; i++) this[k].push(o[k][i]); }
  // gira (graus, anti-horário em torno de z) e desloca
  gira(th, dx = 0, dy = 0, dz = 0) {
    const c = Math.cos(th * rad), s = Math.sin(th * rad), p = this.p, n = this.n;
    for (let i = 0; i < p.length; i += 3) { const x = p[i], y = p[i + 1]; p[i] = c * x - s * y + dx; p[i + 1] = s * x + c * y + dy; p[i + 2] += dz;
      const nx = n[i], ny = n[i + 1]; n[i] = c * nx - s * ny; n[i + 1] = s * nx + c * ny; }
    return this;
  }
  // escala só o z (exagero vertical) com correção das normais
  escalaZ(ez) {
    if (ez === 1) return this; const p = this.p, n = this.n;
    for (let i = 0; i < p.length; i += 3) { p[i + 2] *= ez; const nz = n[i + 2] / ez, l = Math.hypot(n[i], n[i + 1], nz) || 1; n[i] /= l; n[i + 1] /= l; n[i + 2] = nz / l; }
    return this;
  }
  pronto() {
    return { positions: { value: new Float32Array(this.p), size: 3 }, normals: { value: new Float32Array(this.n), size: 3 }, colors: { value: new Float32Array(this.c), size: 3 }, _tris: this.p.length / 9 };
  }
}

// ---------------------------------------------------------------- peças
// polígono retângulo CCW
const ret = (x0, x1, y0, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
const poliReg = (cx, cy, r, n, fase = 0) => { const o = []; for (let i = 0; i < n; i++) { const a = fase + i / n * 2 * Math.PI; o.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return o; };

// mapeia (u, v, profundidade para fora) de uma face de caixa para 3D
function faceMap(face, x0, x1, y0, y1) {
  if (face === 'S') return (u, v, d) => [u, y0 - d, v];
  if (face === 'N') return (u, v, d) => [u, y1 + d, v];
  if (face === 'E') return (u, v, d) => [x1 + d, u, v];
  return (u, v, d) => [x0 - d, u, v];
}

// polígono 2D (u,v) de um vão, anti-horário: retângulo, com topo em arco (`arco`, meia-volta de 0 a π) ou círculo (`oculo`)
function vaoPoli2(u, v0, w, h, forma) {
  if (forma === 'oculo') { const o = []; for (let i = 0; i < 12; i++) { const a = i / 12 * 2 * Math.PI; o.push([u + w / 2 * Math.cos(a), v0 + w / 2 + w / 2 * Math.sin(a)]); } return o; }
  const o = [[u - w / 2, v0], [u + w / 2, v0]];
  if (forma === 'arco') { const r = w / 2, vc = v0 + h - r; for (let i = 0; i <= 8; i++) { const a = i / 8 * Math.PI; o.push([u + r * Math.cos(a), vc + r * Math.sin(a)]); } }
  else if (forma === 'ogival') {   // arco quebrado: dois arcos de raio w com centros nas nascenças opostas
    const vc = v0 + h - .866 * w;
    for (let i = 0; i <= 5; i++) { const a = i / 5 * Math.PI / 3; o.push([u - w / 2 + w * Math.cos(a), vc + w * Math.sin(a)]); }
    for (let i = 1; i <= 5; i++) { const a = 2 * Math.PI / 3 + i / 5 * Math.PI / 3; o.push([u + w / 2 + w * Math.cos(a), vc + w * Math.sin(a)]); } }
  else o.push([u + w / 2, v0 + h], [u - w / 2, v0 + h]);
  return o;
}
// PINÁCULO: base quadrada + pirâmide
function pinaculo(M, x, y, z, w, h, cor) { M.caixa(x - w / 2, x + w / 2, y - w / 2, y + w / 2, z, z + h * .4, cor); M.piramide(ret(x - w / 2, x + w / 2, y - w / 2, y + w / 2), z + h * .4, [x, y, z + h], cor); }
// CÚPULA "meia-laranja" (anéis × gomos, cores alternadas)
function cupula(M, cx, cy, z0, r, h, c1, c2) {
  const N = 12, R = 5, ref = [cx, cy, z0 - r], p = (a, b) => [cx + r * Math.cos(a) * Math.cos(b), cy + r * Math.cos(a) * Math.sin(b), z0 + h * Math.sin(a)];
  for (let j = 0; j < R; j++) { const a0 = j / R * Math.PI / 2, a1 = (j + 1) / R * Math.PI / 2;
    for (let i = 0; i < N; i++) { const b0 = i / N * 2 * Math.PI, b1 = (i + 1) / N * 2 * Math.PI; M.quad(p(a0, b0), p(a0, b1), p(a1, b1), p(a1, b0), (i % 2) ? c1 : c2, ref); } }
}
// FRONTÃO triangular sobre a fachada (−y): corpo, cimalhas nas rampas, cornija de base; opcional óculo, cruz (escala k), pináculos nos ombros
function frontao(M, xa, xb, yf, fz, fa, esp, cp, cm, o = {}) {
  const refF = [(xa + xb) / 2, yf + 5, fz], cx = (xa + xb) / 2;
  const tri = [[xa, yf - esp, fz], [xb, yf - esp, fz], [cx, yf - esp, fa]], tri2 = [[xa, yf + .3, fz], [xb, yf + .3, fz], [cx, yf + .3, fa]];
  M.tri(tri[0], tri[1], tri[2], cp, refF); M.tri(tri2[0], tri2[1], tri2[2], cp, [cx, yf + 20, fz]);
  M.quad(tri[0], tri[2], tri2[2], tri2[0], cp, refF); M.quad(tri[1], tri[2], tri2[2], tri2[1], cp, refF); M.quad(tri[0], tri[1], tri2[1], tri2[0], cp, refF);
  const bw = o.barra || .35;
  M.barra([xa - .2, yf - esp - .05, fz + .05], [cx, yf - esp - .05, fa + .05], bw, bw * .85, cm); M.barra([xb + .2, yf - esp - .05, fz + .05], [cx, yf - esp - .05, fa + .05], bw, bw * .85, cm);
  M.caixa(xa - .3, xb + .3, yf - esp - .1, yf + .3, fz - .1, fz + bw * .85, cm);
  if (o.pinaculos) for (const x of [xa + .3, xb - .3]) pinaculo(M, x, yf - esp / 2, fz, 1.0, 2.3, cm);
  if (o.oculo) vao(M, 'S', xa, xb, yf - esp, yf + 20, cx, fz + (o.oculo_z ?? 1.2), o.oculo, o.oculo, { moldura: cm, folha: o.oculo_cor || P.vidro, forma: 'oculo', sal: .2 });
  if (o.cruz) { const k = o.cruz; M.barra([cx, yf - esp / 2, fa], [cx, yf - esp / 2, fa + 2.2 * k], .22, .22, cm); M.barra([cx - .7 * k, yf - esp / 2, fa + 1.5 * k], [cx + .7 * k, yf - esp / 2, fa + 1.5 * k], .22, .22, cm); }
}
// AMEIAS (merlões) em volta de um retângulo no topo z, com laje escura por dentro; k escala a altura
function ameias(M, x0, x1, y0, y1, z, k, cor, corLaje) {
  const t = .35, hp = .5 * k, hm = .5 * k;
  M.caixa(x0 - .05, x1 + .05, y0 - .05, y0 + t, z, z + hp, cor); M.caixa(x0 - .05, x1 + .05, y1 - t, y1 + .05, z, z + hp, cor);
  M.caixa(x0 - .05, x0 + t, y0, y1, z, z + hp, cor); M.caixa(x1 - t, x1 + .05, y0, y1, z, z + hp, cor);
  M.caixa(x0 + t, x1 - t, y0 + t, y1 - t, z - .3, z + .05, corLaje || P.ardosia);
  const passo = 1.15, w = .6;
  for (let x = x0 + .3; x + w <= x1 - .25; x += passo) { M.caixa(x, x + w, y0 - .05, y0 + t, z + hp, z + hp + hm, cor); M.caixa(x, x + w, y1 - t, y1 + .05, z + hp, z + hp + hm, cor); }
  for (let y = y0 + .3 + passo / 2; y + w <= y1 - .25; y += passo) { M.caixa(x0 - .05, x0 + t, y, y + w, z + hp, z + hp + hm, cor); M.caixa(x1 - t, x1 + .05, y, y + w, z + hp, z + hp + hm, cor); }
}
// PLATAFORMA ferroviária atrás (+y) de um prédio: laje, faixa da borda, lastro, dormentes, trilhos; cobertura de zinco em colunas de ferro (fase coroa)
function plataforma(M, F, PX0, PX1, PY0, PY1) {
  if (F.laje > 0) { M.caixa(PX0, PX1, PY0, PY1, 0, .9 * F.laje, { lado: P.concreto, topo: esc(P.concreto, 1.04), fundo: P.concreto });
    M.caixa(PX0, PX1, PY1 - .35, PY1, .9 * F.laje, .93 * F.laje, P.branco);
    M.caixa(PX0 - 6, PX1 + 6, PY1 + .3, PY1 + 4.3, 0, .3 * F.laje, P.lastro);
    if (F.laje >= 1) { for (let x = PX0 - 6; x < PX1 + 6; x += 1.4) M.caixa(x, x + .28, PY1 + .9, PY1 + 3.7, .3, .46, P.dormente);
      for (const y of [PY1 + 1.5, PY1 + 3.1]) M.barra([PX0 - 6, y, .55], [PX1 + 6, y, .55], .09, .16, P.trilho); } }
  if (F.coroa > 0) { const k = F.coroa, zc = .9 + 3.4 * k, ref = [0, PY1 + 10, 0];
    for (let x = PX0 + 1.5; x <= PX1 - 1.4; x += 5) { M.barra([x, PY1 - 1.0, .9], [x, PY1 - 1.0, zc], .2, .2, P.ferro); M.barra([x, PY1 - 1.0, zc - .8], [x, PY1 - 2.2, zc - .05], .12, .12, P.ferro); M.barra([x, PY1 - 1.0, zc - .8], [x, PY1 + .2, zc - .05], .12, .12, P.ferro); }
    M.barra([PX0 + .5, PY1 - 1.0, zc - .1], [PX1 - .5, PY1 - 1.0, zc - .1], .25, .25, P.ferro);
    if (k >= 1) { const ya = PY0 - .3, yb = PY1 + .8, za = zc + .35, zb = zc - .1;
      M.quad([PX0 + .5, ya, za], [PX1 - .5, ya, za], [PX1 - .5, yb, zb], [PX0 + .5, yb, zb], P.zinco, ref);
      M.quad([PX0 + .5, ya, za - .12], [PX0 + .5, yb, zb - .12], [PX1 - .5, yb, zb - .12], [PX1 - .5, ya, za - .12], P.zinco2, [0, PY1, 20]);
      M.quad([PX0 + .5, yb, zb - .12], [PX1 - .5, yb, zb - .12], [PX1 - .5, yb, zb], [PX0 + .5, yb, zb], P.ferro, [0, PY0, zb]);
      for (let x = PX0 + 2; x < PX1 - .5; x += 1.9) M.barra([x, ya, za + .02], [x, yb, zb + .02], .09, .09, esc(P.zinco, .8)); } }
}
// polígono "engordado" para a moldura: afasta cada vértice do centro do vão
function engorda(pol, m) {
  let cx = 0, cy = 0; for (const p of pol) { cx += p[0]; cy += p[1]; } cx /= pol.length; cy /= pol.length;
  // para retângulos/arcos a expansão radial fica torta; usa expansão por eixo (|dx|,|dy|) + m
  return pol.map(([x, y]) => [x + Math.sign(x - cx) * m, y + Math.sign(y - cy) * m]);
}
// VÃO (porta/janela) numa face: moldura em relevo (anel) + folha escura recuada em relação à moldura
// opts: {forma:'reta'|'arco'|'oculo', moldura: cor, folha: cor, sal: saliência da moldura, mb: largura da moldura, pane: saliência da folha}
function vao(M, face, x0, x1, y0, y1, u, v0, w, h, opts) {
  const f = faceMap(face, x0, x1, y0, y1), sal = opts.sal ?? 0.14, mb = opts.mb ?? 0.18, pane = opts.pane ?? 0.05;
  const forma = opts.forma || 'reta', I = vaoPoli2(u, v0, w, h, forma), O = engorda(I, mb);
  const n = I.length; let cu = 0, cv = 0; for (const p of I) { cu += p[0]; cv += p[1]; } cu /= n; cv /= n;
  const refAtras = f(cu, cv, -1), refDentro = f(cu, cv, sal);
  const cm = opts.moldura || P.azul, cf = opts.folha || P.vidro;
  for (let i = 0; i < n; i++) { const a = I[i], b = I[(i + 1) % n], A = O[i], B = O[(i + 1) % n];
    M.quad(f(A[0], A[1], sal), f(B[0], B[1], sal), f(b[0], b[1], sal), f(a[0], a[1], sal), cm, refAtras);     // frente do anel
    M.quad(f(A[0], A[1], 0), f(B[0], B[1], 0), f(B[0], B[1], sal), f(A[0], A[1], sal), cm, refDentro);        // lado externo da moldura
    M.quad(f(a[0], a[1], pane), f(b[0], b[1], pane), f(b[0], b[1], sal), f(a[0], a[1], sal), esc(cm, .75), refDentro, true); // rebaixo interno
  }
  M.poli(I.map(p => f(p[0], p[1], pane)), cf, refAtras);                                                      // folha
  if (opts.peitoril) M.barra(f(u - w / 2 - mb - .05, v0 - .02, sal), f(u + w / 2 + mb + .05, v0 - .02, sal), .12, .1, opts.moldura || P.azul); // soleira/peitoril
}
// SACADA (balcão) sob um vão da face: laje + guarda-corpo de ferro
function sacada(M, face, x0, x1, y0, y1, u, v0, w, cor) {
  const f = faceMap(face, x0, x1, y0, y1), prof = .9, lw = w + .7, ref = f(u, v0 - .3, prof / 2);
  const q = (a, b, c, d) => M.quad(a, b, c, d, cor, ref);
  const p = (uu, dd, vv) => f(uu, vv, dd);
  const z0 = v0 - .14, z1 = v0;
  // laje
  q(p(u - lw / 2, 0, z1), p(u + lw / 2, 0, z1), p(u + lw / 2, prof, z1), p(u - lw / 2, prof, z1));
  q(p(u - lw / 2, 0, z0), p(u - lw / 2, prof, z0), p(u + lw / 2, prof, z0), p(u + lw / 2, 0, z0));
  q(p(u - lw / 2, prof, z0), p(u + lw / 2, prof, z0), p(u + lw / 2, prof, z1), p(u - lw / 2, prof, z1));
  q(p(u - lw / 2, 0, z0), p(u - lw / 2, 0, z1), p(u - lw / 2, prof, z1), p(u - lw / 2, prof, z0));
  q(p(u + lw / 2, 0, z0), p(u + lw / 2, prof, z0), p(u + lw / 2, prof, z1), p(u + lw / 2, 0, z1));
  // guarda-corpo: 3 montantes + corrimão + barra média
  const h = .95, fe = P.ferro;
  for (const uu of [u - lw / 2 + .05, u, u + lw / 2 - .05]) M.barra(p(uu, prof - .05, z1), p(uu, prof - .05, z1 + h), .06, .06, fe);
  M.barra(p(u - lw / 2, prof - .05, z1 + h), p(u + lw / 2, prof - .05, z1 + h), .07, .06, fe);
  M.barra(p(u - lw / 2, prof - .05, z1 + h * .5), p(u + lw / 2, prof - .05, z1 + h * .5), .05, .04, fe);
  M.barra(p(u - lw / 2, .03, z1 + h), p(u - lw / 2, prof - .05, z1 + h), .06, .06, fe);
  M.barra(p(u + lw / 2, .03, z1 + h), p(u + lw / 2, prof - .05, z1 + h), .06, .06, fe);
}
// faixas de telha entre a aresta do beiral (e0→e1) e a da cumeeira (r0→r1); a parte baixa de cada faixa é mais escura
function faixasTelha(M, e0, e1, r1, r0, cor, cor2, ref, passo = .85) {
  const L = Math.hypot(r0[0] - e0[0], r0[1] - e0[1], r0[2] - e0[2]), n = Math.max(2, Math.round(L / passo));
  const ip = (a, b, k) => [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)];
  for (let i = 0; i < n; i++) { const k0 = i / n, k1 = (i + 1) / n, km = k0 + (k1 - k0) * .3;
    const a0 = ip(e0, r0, k0), a1 = ip(e1, r1, k0), m0 = ip(e0, r0, km), m1 = ip(e1, r1, km), b0 = ip(e0, r0, k1), b1 = ip(e1, r1, k1);
    const c = (i % 2) ? cor2 : cor;
    M.quad(a0, a1, m1, m0, esc(c, .82), ref); M.quad(m0, m1, b1, b0, c, ref); }
}
// TELHADO DE 2 ÁGUAS: cumeeira paralela a x (eixo 'x') ou a y (eixo 'y'); beiral b; inclinação ang (graus)
// retorna {alt} (altura da cumeeira acima de z0)
function telhado2(M, x0, x1, y0, y1, z0, ang, b, eixo, cores, dz = 0) {
  if (eixo === 'y') { // constrói girado 90° e devolve
    const T = new Malha(), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const r = telhado2(T, cy - (y1 - y0) / 2, cy + (y1 - y0) / 2, cx - (x1 - x0) / 2, cx + (x1 - x0) / 2, z0, ang, b, 'x', cores, dz);
    // troca x↔y (os intervalos passados já estão centrados em cy/cx); as normais trocam junto, as faces continuam corretas
    const p = T.p, n = T.n; for (let i = 0; i < p.length; i += 3) { const x = p[i], y = p[i + 1]; p[i] = y; p[i + 1] = x; const nx = n[i], ny = n[i + 1]; n[i] = ny; n[i + 1] = nx; }
    M.junta(T); return r;
  }
  const t = Math.tan(ang * rad), esp = .2, bg = b * .6;   // bg = beiral no oitão
  const ya = y0 - b, yb = y1 + b, xa = x0 - bg, xb = x1 + bg, ym = (y0 + y1) / 2;
  const ze = z0 + .1 - b * t + dz, zr = z0 + .1 + (y1 - y0) / 2 * t + dz;
  const ref = [(x0 + x1) / 2, ym, z0 - 3 + dz];
  const C = cores;
  faixasTelha(M, [xa, ya, ze], [xb, ya, ze], [xb, ym, zr], [xa, ym, zr], C.telha, C.telha2, ref);
  faixasTelha(M, [xb, yb, ze], [xa, yb, ze], [xa, ym, zr], [xb, ym, zr], C.telha, C.telha2, ref);
  // testeiras (beiral) e tábuas de oitão; sofito
  const refc = [(x0 + x1) / 2, ym, zr - 1 + dz];
  M.quad([xa, ya, ze - esp], [xb, ya, ze - esp], [xb, ya, ze], [xa, ya, ze], C.testeira, refc);
  M.quad([xb, yb, ze - esp], [xa, yb, ze - esp], [xa, yb, ze], [xb, yb, ze], C.testeira, refc);
  for (const [x, s] of [[xa, -1], [xb, 1]]) {
    M.quad([x, ya, ze - esp], [x, ya, ze], [x, ym, zr], [x, ym, zr - esp], C.testeira, refc);
    M.quad([x, yb, ze - esp], [x, yb, ze], [x, ym, zr], [x, ym, zr - esp], C.testeira, refc);
  }
  M.quad([xa, ya, ze - esp], [xb, ya, ze - esp], [xb, ym, zr - esp], [xa, ym, zr - esp], C.sofito, [(x0 + x1) / 2, ym, zr + 5 + dz]);
  M.quad([xb, yb, ze - esp], [xa, yb, ze - esp], [xa, ym, zr - esp], [xb, ym, zr - esp], C.sofito, [(x0 + x1) / 2, ym, zr + 5 + dz]);
  M.barra([xa - .05, ym, zr + .02], [xb + .05, ym, zr + .02], .4, .2, C.cumeeira);
  // oitões (triângulos de parede nas pontas)
  const cp = C.parede || P.cal, refo = [(x0 + x1) / 2, ym, z0 + dz], za = zr - .1;   // zr já inclui dz
  M.tri([x0, y0, z0 + dz], [x0, y1, z0 + dz], [x0, ym, za], cp, refo);
  M.tri([x1, y0, z0 + dz], [x1, y1, z0 + dz], [x1, ym, za], cp, refo);
  M.tri([x0 + .3, y0, z0 + dz], [x0 + .3, y1, z0 + dz], [x0 + .3, ym, za], cp, [x0 - 5, ym, z0 + dz]);
  M.tri([x1 - .3, y0, z0 + dz], [x1 - .3, y1, z0 + dz], [x1 - .3, ym, za], cp, [x1 + 5, ym, z0 + dz]);
  return { alt: zr - z0 - dz, ze, zr };
}
// TELHADO DE 4 ÁGUAS (cumeeira no eixo maior), ou pirâmide quando quadrado
function telhado4(M, x0, x1, y0, y1, z0, ang, b, cores, dz = 0) {
  const t = Math.tan(ang * rad), esp = .2, xa = x0 - b, xb = x1 + b, ya = y0 - b, yb = y1 + b;
  const W = Math.min(xb - xa, yb - ya), ze = z0 + .1 - b * t + dz, zr = ze + W / 2 * t;
  const cx = (xa + xb) / 2, cy = (ya + yb) / 2, ref = [cx, cy, z0 - 3 + dz], C = cores;
  let r0, r1, faces;
  if (xb - xa >= yb - ya) { const L = (xb - xa - W) / 2; r0 = [cx - L, cy, zr]; r1 = [cx + L, cy, zr];
    faces = [[[xa, ya, ze], [xb, ya, ze], r1, r0], [[xb, yb, ze], [xa, yb, ze], r0, r1], [[xa, yb, ze], [xa, ya, ze], r0, r0], [[xb, ya, ze], [xb, yb, ze], r1, r1]]; }
  else { const L = (yb - ya - W) / 2; r0 = [cx, cy - L, zr]; r1 = [cx, cy + L, zr];
    faces = [[[xb, ya, ze], [xb, yb, ze], r1, r0], [[xa, yb, ze], [xa, ya, ze], r0, r1], [[xa, ya, ze], [xb, ya, ze], r0, r0], [[xb, yb, ze], [xa, yb, ze], r1, r1]]; }
  for (const [e0, e1, q1, q0] of faces) faixasTelha(M, e0, e1, q1, q0, C.telha, C.telha2, ref);
  const refc = [cx, cy, zr - 1];
  M.quad([xa, ya, ze - esp], [xb, ya, ze - esp], [xb, ya, ze], [xa, ya, ze], C.testeira, refc);
  M.quad([xb, yb, ze - esp], [xa, yb, ze - esp], [xa, yb, ze], [xb, yb, ze], C.testeira, refc);
  M.quad([xb, ya, ze - esp], [xb, yb, ze - esp], [xb, yb, ze], [xb, ya, ze], C.testeira, refc);
  M.quad([xa, yb, ze - esp], [xa, ya, ze - esp], [xa, ya, ze], [xa, yb, ze], C.testeira, refc);
  M.quad([xa, ya, ze - esp], [xa, yb, ze - esp], [xb, yb, ze - esp], [xb, ya, ze - esp], C.sofito, [cx, cy, zr + 5]);
  if (Math.hypot(r1[0] - r0[0], r1[1] - r0[1]) > .3) M.barra([r0[0], r0[1], zr + .02], [r1[0], r1[1], zr + .02], .4, .2, C.cumeeira);
  for (const [e0, e1, q1, q0] of faces) { M.barra([e0[0], e0[1], ze + .02], [q0[0], q0[1], zr + .02], .22, .14, C.cumeeira); }
  return { alt: zr - z0 - dz, ze, zr };
}
// paredes de caixa com soco, cunhais e cornija (opcionais)
function corpo(M, x0, x1, y0, y1, z0, z1, o) {
  const cp = o.parede || P.cal, cm = o.moldura || P.azul;
  M.caixa(x0, x1, y0, y1, z0, z1, { lado: cp, topo: esc(cp, .9), fundo: cp });
  if (o.soco) { const s = o.soco, e = .06; M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, z0, Math.min(z1, z0 + s), o.corSoco || P.soco); }
  if (o.cunhal) { const w = o.cunhal, e = .09;
    for (const [x, y] of [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) {
      const ax = x === x0 ? x0 - e : x1 - w + e, bx = x === x0 ? x0 + w - e : x1 + e, ay = y === y0 ? y0 - e : y1 - w + e, by = y === y0 ? y0 + w - e : y1 + e;
      M.caixa(Math.min(ax, bx), Math.max(ax, bx), Math.min(ay, by), Math.max(ay, by), z0, z1, cm); } }
  if (o.cornija) { const h = o.cornija, e = .12; M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, z1 - h, z1, { lado: o.corCornija || cm, topo: esc(cp, .9), fundo: o.corCornija || cm }); }
  if (o.beiral) { const h = o.beiral, e = .02, zc = z1 - (o.cornija || 0); M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, zc - h, zc, { lado: esc(cp, .8), topo: cp, fundo: cp }); }   // sombra do beiral na parede
}
// fases da construção a partir do progresso k (0..1)
function fases(k) {
  return { laje: ease(k / .12), paredes: ease((k - .10) / .58), telhado: ease((k - .66) / .24), coroa: ease((k - .86) / .14), k };
}

// ---------------------------------------------------------------- arquétipos (frente para −y; x = largura; y = profundidade)
const ARQ = {};

// CASA TÉRREA porta-e-janela: 2 águas com cumeeira paralela à rua, beiral, 1 porta + janelas
ARQ.casa = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 8, comp = m.comp || 10, pe = m.pe || 3.4, x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2;
  const cm = cor.moldura, cp = cor.parede || P.cal;
  if (F.laje > 0) M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .25 * F.laje, P.pedra);
  const hp = pe * F.paredes; if (hp <= .02) return { M, alt: .3, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .55, cunhal: .4, cornija: F.paredes >= 1 ? .22 : 0, beiral: F.paredes >= 1 ? .4 : 0 });
  // vãos da frente: porta à esquerda, janelas no resto (só os que cabem na parede já erguida)
  const vaos = []; let u = x0 + 1.2; vaos.push({ u, w: 1.1, h: 2.3, v0: .08, porta: true }); u += 2.2;
  while (u < x1 - .9) { vaos.push({ u, w: 1.0, h: 1.45, v0: 1.0 }); u += 2.1; }
  for (const v of vaos) if (v.v0 + v.h + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, v.u, v.v0, v.w, v.h, v.porta ? { moldura: cm, folha: P.madeira } : { moldura: cm, folha: P.veneziana, peitoril: true });
  if (m.lados !== false) for (const face of ['E', 'W']) for (let uu = y0 + 2.5; uu < y1 - 1.5; uu += 3) if (1.0 + 1.45 + .2 <= hp) vao(M, face, x0, x1, y0, y1, uu, 1.0, 1.0, 1.45, { moldura: cm, folha: P.veneziana, peitoril: true });
  let alt = hp;
  if (F.telhado > 0) { const r = telhado2(M, x0, x1, y0, y1, pe, m.inclina || 30, m.beiral || .55, 'x', { telha: cor.telha || P.telha, telha2: cor.telha2 || P.telha2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira, parede: cp }, (1 - F.telhado) * 5); alt = pe + r.alt; }
  return { M, alt, sombra: hp };
};

// SOBRADO: 2 pavimentos (ou `andares`), 4 águas, beiral, portas embaixo, janelas com sacada em cima
ARQ.sobrado = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 12, comp = m.comp || 13, andares = m.andares || 2, pe = m.pe || 3.6, H = pe * andares;
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2, cm = cor.moldura, cp = cor.parede || P.cal;
  if (F.laje > 0) M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .25 * F.laje, P.pedra);
  const hp = H * F.paredes; if (hp <= .02) return { M, alt: .3, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .6, cunhal: .45, cornija: F.paredes >= 1 ? .28 : 0, beiral: F.paredes >= 1 ? .45 : 0 });
  for (let a = 1; a < andares; a++) if (a * pe + .1 <= hp) M.caixa(x0 - .1, x1 + .1, y0 - .1, y1 + .1, a * pe - .18, a * pe, cm); // cimalha entre pisos
  const passo = 2.5, n = Math.max(1, Math.floor((larg - 1.2) / passo)), u0 = -(n - 1) * passo / 2;
  for (let i = 0; i < n; i++) { const u = u0 + i * passo;
    if (.08 + 2.7 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, u, .08, 1.2, 2.7, { moldura: cm, folha: P.madeira, forma: m.arcos ? 'arco' : 'reta' });
    for (let a = 1; a < andares; a++) { const v0 = a * pe + .95; if (v0 + 1.9 + .2 <= hp) {
      vao(M, 'S', x0, x1, y0, y1, u, v0 - .9, 1.15, 2.6, { moldura: cm, folha: P.veneziana, forma: m.arcos ? 'arco' : 'reta' });
      if (m.sacadas !== false) sacada(M, 'S', x0, x1, y0, y1, u, v0 - .9, 1.15, cm); } } }
  for (const face of ['E', 'W', 'N']) { const L = face === 'N' ? larg : comp, c0 = face === 'N' ? x0 : y0;
    for (let uu = c0 + 2; uu < c0 + L - 1.4; uu += 3.2) for (let a = 0; a < andares; a++) { const v0 = a * pe + (a ? .95 : 1.0); if (v0 + 1.6 + .2 <= hp) vao(M, face, x0, x1, y0, y1, uu, v0, 1.1, 1.6, { moldura: cm, folha: P.veneziana, peitoril: true }); } }
  let alt = hp;
  if (F.telhado > 0) { const r = telhado4(M, x0, x1, y0, y1, H, m.inclina || 27, m.beiral || .65, { telha: cor.telha || P.telha, telha2: cor.telha2 || P.telha2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira }, (1 - F.telhado) * 6); alt = H + r.alt; }
  return { M, alt, sombra: hp };
};

// IGREJA colonial luso-brasileira: nave com 2 águas (cumeeira perpendicular à fachada), frontão com óculo e cruz, torre(s) com cúpula ou coruchéu, sacristia, adro
// m.torre_lado: 'direita' (padrão: à direita de quem olha a fachada — Matriz de Itaguaí) | 'esquerda'; m.torres: 1|2; m.coroa: 'cupula' (padrão) | 'piramide'
ARQ.igreja = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 12, comp = m.comp || 28, pe = m.pe || 10, torres = m.torres ?? 1, tl = m.torre_m || 4.6, tAlt = m.torre_alt || 21, coroa = m.coroa || 'cupula';
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2, cm = cor.moldura, cp = cor.parede || P.cal;
  const ct = cor.telha || P.telha, ct2 = cor.telha2 || P.telha2, cores = { telha: ct, telha2: ct2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira, parede: cp };
  // adro (pátio de pedra à frente)
  if (F.laje > 0) { M.caixa(x0 - 3, x1 + 3, y0 - 9, y0 + .5, 0, .18 * F.laje, P.pedra); M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .3 * F.laje, P.pedra); }
  const hp = pe * F.paredes; if (hp <= .02) return { M, alt: .4, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .8, cunhal: .6, cornija: F.paredes >= 1 ? .35 : 0, beiral: F.paredes >= 1 ? .5 : 0 });
  // vãos da fachada: porta central em arco, 2 janelas laterais, 3 janelas do coro, óculo
  const pw = 2.4, ph = 4.6;
  if (.1 + ph + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, 0, .1, pw, ph, { moldura: cm, folha: P.madeira, forma: 'arco', sal: .22, mb: .3 });
  for (const u of [-larg * .3, larg * .3]) if (1.2 + 2.6 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, u, 1.2, 1.4, 2.6, { moldura: cm, folha: P.veneziana, forma: 'arco', peitoril: true });
  for (const u of [-larg * .3, 0, larg * .3]) if (pe * .62 + 2.6 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, u, pe * .62, 1.5, 2.6, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: true });
  // janelas altas das naves laterais
  for (const face of ['E', 'W']) for (let uu = y0 + 6; uu < y1 - 3; uu += 5) if (pe * .55 + 2.8 + .2 <= hp) vao(M, face, x0, x1, y0, y1, uu, pe * .55, 1.3, 2.8, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: true });
  // sacristia atrás (mais baixa)
  const sl = larg * .7, sc = m.sacristia || 7, sh = pe * .55 * F.paredes;
  if (sh > .05) { corpo(M, -sl / 2, sl / 2, y1, y1 + sc, 0, sh, { parede: cp, moldura: cm, soco: .6, cunhal: .4 });
    if (F.telhado > 0) telhado4(M, -sl / 2, sl / 2, y1, y1 + sc, pe * .55, 28, .5, cores, (1 - F.telhado) * 5); }
  let alt = hp;
  // telhado da nave
  if (F.telhado > 0) { const r = telhado2(M, x0, x1, y0, y1, pe, m.inclina || 32, .5, 'y', cores, (1 - F.telhado) * 7); alt = pe + r.alt;
    // FRONTÃO: triângulo da fachada acima da cornija, com cimalha nas rampas, pináculos nos ombros, óculo e cruz
    if (F.telhado >= 1) frontao(M, -larg / 2 - .2, larg / 2 + .2, y0, pe + .2, pe + r.alt + .9, .55, cp, cm, { pinaculos: true, oculo: 1.6, cruz: F.coroa }); }
  // TORRE(S): base quadrada encostada na fachada, saliente; sineira com 4 arcos; cornija; cúpula prateada com 4 pináculos ou coruchéu piramidal; cruz
  const lados = torres === 2 ? [-1, 1] : [(m.torre_lado || 'direita') === 'esquerda' ? -1 : 1];   // +x = direita de quem olha a fachada
  for (const s of lados) {
    const tx0 = s < 0 ? x0 - .4 : x1 + .4 - tl, tx1 = tx0 + tl, ty0 = y0 - .8, ty1 = ty0 + tl;
    const hBase = Math.min(hp, pe), hTorre = (tAlt - 5.5), kt = ease((F.k - .62) / .28);   // corpo da torre sobe junto com o telhado; o coruchéu entra na coroa
    const ht = pe + (hTorre - pe) * kt;
    if (hBase > .05) corpo(M, tx0, tx1, ty0, ty1, 0, Math.max(hBase, kt > 0 ? ht : hBase), { parede: cp, moldura: cm, soco: .8, cunhal: .6, cornija: kt >= 1 ? .35 : 0 });
    if (.1 + 2.6 + .2 <= hp) vao(M, 'S', tx0, tx1, ty0, ty1, (tx0 + tx1) / 2, .1, 1.3, 2.6, { moldura: cm, folha: P.madeira, forma: 'arco' });
    if (kt > 0) {
      const zs = ht - 4.2 * kt; // sineira: 4 arcos
      for (const face of ['S', 'N', 'E', 'W']) { const cu = face === 'S' || face === 'N' ? (tx0 + tx1) / 2 : (ty0 + ty1) / 2; vao(M, face, tx0, tx1, ty0, ty1, cu, zs, 1.5, 3.2 * kt, { moldura: cm, folha: P.vidro, forma: 'arco', sal: .18 }); }
      M.caixa(tx0 - .15, tx1 + .15, ty0 - .15, ty1 + .15, ht, ht + .35, cm); }
    if (F.coroa > 0) {
      const cx = (tx0 + tx1) / 2, cy = (ty0 + ty1) / 2, k = F.coroa, zb = ht + .35; let topo;
      if (coroa === 'cupula') { const r = tl / 2 + .05, hc = r * 1.15 * k;   // meia-laranja prateada sobre tambor baixo + 4 pináculos nos cantos
        M.prisma(poliReg(cx, cy, r + .1, 12), zb, zb + .5 * k, cm, esc(cm, .9), null);
        cupula(M, cx, cy, zb + .5 * k, r, hc, P.prata, P.prata2);
        for (const [px, py] of [[tx0 - .1, ty0 - .1], [tx1 + .1, ty0 - .1], [tx1 + .1, ty1 + .1], [tx0 - .1, ty1 + .1]]) pinaculo(M, px, py, zb, .75, 2.6 * k, cm);
        topo = zb + .5 * k + hc; }
      else { const hc = 5 * k; M.piramide(ret(tx0 - .15, tx1 + .15, ty0 - .15, ty1 + .15), zb, [cx, cy, zb + hc], cor.coruchéu || P.ardosia); topo = zb + hc; }
      M.prisma(poliReg(cx, cy, .3, 8), topo, topo + .35, cm);   // bola
      M.barra([cx, cy, topo + .3], [cx, cy, topo + 2.0 * k], .2, .2, cm); M.barra([cx - .6 * k, cy, topo + 1.4 * k], [cx + .6 * k, cy, topo + 1.4 * k], .2, .2, cm);
      alt = Math.max(alt, topo + 2);
    }
  }
  return { M, alt, sombra: hp };
};

// ESTAÇÃO ferroviária: prédio baixo de 4 águas com beiral largo, plataforma, cobertura metálica em colunas de ferro, linha com dormentes e trilhos
ARQ.estacao = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 24, comp = m.comp || 9, pe = m.pe || 4.6, x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2;
  const cm = cor.moldura || P.tijolo, cp = cor.parede || P.creme, pl = m.plataforma || 18;   // plataforma: extensão além do prédio, de cada lado
  const PX0 = x0 - pl, PX1 = x1 + pl, PY0 = y1, PY1 = y1 + 4.2;                              // plataforma atrás (+y)
  if (F.laje > 0) M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .25 * F.laje, P.pedra);
  plataforma(M, F, PX0, PX1, PY0, PY1);
  const hp = pe * F.paredes; if (hp <= .02) return { M, alt: .9, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .5, cunhal: .5, cornija: F.paredes >= 1 ? .3 : 0, corCornija: cm, beiral: F.paredes >= 1 ? .5 : 0 });
  const passo = 2.9, n = Math.max(1, Math.floor((larg - 1.5) / passo)), u0 = -(n - 1) * passo / 2;
  for (let i = 0; i < n; i++) { const u = u0 + i * passo, porta = i % 2 === 0;
    for (const face of ['S', 'N']) { const v0 = porta ? .08 : 1.1, h = porta ? 3.1 : 2.0; if (v0 + h + .2 <= hp) vao(M, face, x0, x1, y0, y1, u, v0, 1.35, h, { moldura: cm, folha: porta ? P.madeira : P.vidro, forma: 'arco', peitoril: !porta }); } }
  for (const face of ['E', 'W']) if (1.1 + 2 + .2 <= hp) vao(M, face, x0, x1, y0, y1, 0, 1.1, 1.35, 2.0, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: true });
  let alt = hp;
  if (F.telhado > 0) { const r = telhado4(M, x0, x1, y0, y1, pe, m.inclina || 25, m.beiral || .9, { telha: cor.telha || P.telha, telha2: cor.telha2 || P.telha2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira }, (1 - F.telhado) * 5); alt = pe + r.alt; }
  return { M, alt, sombra: hp };
};

// ESTAÇÃO-CASTELO (Itaguaí 1910, hoje Casa de Cultura): eclético "acastelado" — torre quadrada de 2 pavimentos + alas de 1 pavimento,
// platibanda com AMEIAS em toda a volta, cornija com furinhos redondos na torre, janelas ogivais no 2º pavimento, óculos no térreo;
// parede amarelo-ocre com cunhais/frisos/molduras brancas. m.plataforma: true → plataforma + cobertura + linha atrás (+y)
ARQ.estacao_castelo = (m, F, cor) => {
  const M = new Malha(), tl = m.torre_m || 6, th = m.torre_alt || 11.5, ala = m.ala || 9, comp = m.comp || 7, ha = m.ala_alt || 4.6;
  const cp = cor.parede || P.ocreParede, cm = cor.moldura || P.branco, y0 = -comp / 2, y1 = comp / 2;
  const tx0 = -tl / 2, tx1 = tl / 2, A = [[tx0 - ala, tx0], [tx1, tx1 + ala]];   // alas (esquerda, direita)
  if (F.laje > 0) M.caixa(tx0 - ala - .3, tx1 + ala + .3, y0 - .3, y1 + .3, 0, .3 * F.laje, P.pedra);
  if (m.plataforma !== false) plataforma(M, F, tx0 - ala - 10, tx1 + ala + 10, y1, y1 + 4.2);
  const hpT = th * F.paredes, hpA = ha * F.paredes; if (hpT <= .02) return { M, alt: .9, sombra: 0 };
  // torre
  corpo(M, tx0, tx1, y0, y1, 0, hpT, { parede: cp, moldura: cm, soco: .7, cunhal: .5 });
  if (.1 + 3.0 + .2 <= hpT) vao(M, 'S', tx0, tx1, y0, y1, 0, .1, 1.5, 3.0, { moldura: cm, folha: P.madeira, forma: 'arco', sal: .18, mb: .25 });
  for (const u of [-1.9, 1.9]) if (2.4 + 1.0 + .2 <= hpT) vao(M, 'S', tx0, tx1, y0, y1, u, 2.4, 1.0, 1.0, { moldura: cm, folha: P.vidro, forma: 'oculo' });
  for (const face of ['E', 'W']) if (2.4 + 1.0 + .2 <= hpT) vao(M, face, tx0, tx1, y0, y1, 0, 2.4, 1.0, 1.0, { moldura: cm, folha: P.vidro, forma: 'oculo' });
  for (const u of [-1.6, 0, 1.6]) if (6.0 + 2.6 + .2 <= hpT) vao(M, 'S', tx0, tx1, y0, y1, u, 6.0, .95, 2.6, { moldura: cm, folha: P.vidro, forma: 'ogival', peitoril: true });
  for (const face of ['E', 'W', 'N']) if (6.0 + 2.6 + .2 <= hpT) vao(M, face, tx0, tx1, y0, y1, 0, 6.0, .95, 2.6, { moldura: cm, folha: P.vidro, forma: 'ogival', peitoril: true });
  if (F.paredes >= 1) { M.caixa(tx0 - .12, tx1 + .12, y0 - .12, y1 + .12, th - 1.1, th - .6, cm);   // cornija da torre com fileira de furinhos redondos
    for (const [f, n] of [['S', 1], ['N', 1], ['E', 1], ['W', 1]]) { const fm = faceMap(f, tx0, tx1, y0, y1), L = f === 'S' || f === 'N' ? tl : comp, c0 = f === 'S' || f === 'N' ? tx0 : y0;
      for (let u = c0 + .45; u < c0 + L - .3; u += .55) M.prisma(poliReg(0, 0, .11, 8).map(([a, b]) => { const p = fm(u + a, th - 1.45 + b, .14); return [p[0], p[1]]; }), 0, 0, P.vidro, P.vidro, null), M.poli(poliReg(0, 0, .11, 8).map(([a, b]) => fm(u + a, th - 1.45 + b, .15)), P.vidro, fm(u, th - 1.45, -1)); } }
  // alas
  for (const [ax0, ax1] of A) { if (hpA <= .02) continue;
    corpo(M, ax0, ax1, y0 + .5, y1, 0, hpA, { parede: cp, moldura: cm, soco: .6, cunhal: .4 });
    const cu = (ax0 + ax1) / 2;
    if (.1 + 2.6 + .2 <= hpA) vao(M, 'S', ax0, ax1, y0 + .5, y1, cu, .1, 1.3, 2.6, { moldura: cm, folha: P.madeira, forma: 'arco' });
    for (const u of [cu - 2.6, cu + 2.6]) if (1.2 + 1.3 + .2 <= hpA) vao(M, 'S', ax0, ax1, y0 + .5, y1, u, 1.2, 1.4, 1.3, { moldura: cm, folha: P.vidro, forma: 'reta', peitoril: true });
    if (1.0 + 1.0 + .2 <= hpA) vao(M, 'S', ax0, ax1, y0 + .5, y1, cu, 3.1, .9, .9, { moldura: cm, folha: P.vidro, forma: 'oculo' });
    for (let u = y0 + 2.2; u < y1 - 1; u += 2.4) if (1.2 + 1.3 + .2 <= hpA) vao(M, ax0 === tx1 ? 'E' : 'W', ax0, ax1, y0 + .5, y1, u, 1.2, 1.2, 1.3, { moldura: cm, folha: P.vidro, peitoril: true }); }
  let alt = hpT;
  if (F.telhado > 0) { const k = F.telhado; ameias(M, tx0, tx1, y0, y1, th, k, cm); for (const [ax0, ax1] of A) ameias(M, ax0, ax1, y0 + .5, y1, ha, k, cm); alt = th + 1.0 * k; }
  return { M, alt, sombra: hpT };
};

// CHAFARIZ (1847): "pequena casa" ~3×3 m, frontão triangular com cornija na fachada, arco pleno grande fechado em pedra com saídas de água,
// tanque retangular de pedra embaixo; branco com pilastras, frontão e moldura do arco em cinza/verde-escuro; laterais com vãos abertos
ARQ.chafariz = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 3.2, comp = m.comp || 3.0, pe = m.pe || 3.2, x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2;
  const cp = cor.parede || P.branco, cm = cor.moldura || P.verdeEscuro;
  if (F.laje > 0) { M.caixa(x0 - .4, x1 + .4, y0 - 1.6, y1 + .4, 0, .2 * F.laje, P.pedra);
    M.caixa(x0 - .1, x1 + .1, y0 - 1.4, y0, 0, .75 * F.laje, P.soco);                                    // tanque de pedra
    if (F.laje >= 1) M.caixa(x0 + .05, x1 - .05, y0 - 1.25, y0 - .15, .55, .66, { lado: P.agua, topo: P.agua, fundo: P.agua }); }   // água
  const hp = pe * F.paredes; if (hp <= .02) return { M, alt: .8, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .35, cunhal: .35, cornija: F.paredes >= 1 ? .2 : 0 });
  if (.4 + 2.4 + .2 <= hp) { vao(M, 'S', x0, x1, y0, y1, 0, .4, 1.7, 2.4, { moldura: cm, folha: P.pedra, forma: 'arco', sal: .12, mb: .2, pane: .06 });
    for (const u of [-.35, .35]) M.caixa(u - .07, u + .07, y0 - .4, y0 + .02, 1.05, 1.17, P.bronze);       // bicas
    M.caixa(-.6, .6, y0 - .09, y0 - .07, 2.0, 2.6, P.ferro); }                                             // bandeira de ferro
  for (const face of ['E', 'W']) if (.4 + 2.0 + .2 <= hp) vao(M, face, x0, x1, y0, y1, 0, .4, 1.2, 2.0, { moldura: cm, folha: P.vidro, forma: 'arco' });
  let alt = hp;
  if (F.telhado > 0) { const r = telhado4(M, x0, x1, y0, y1, pe, 16, .2, { telha: cor.telha || P.telha, telha2: cor.telha2 || P.telha2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira }, (1 - F.telhado) * 3); alt = pe + r.alt;
    if (F.telhado >= 1) frontao(M, x0 - .15, x1 + .15, y0, pe + .1, pe + 1.5, .35, cp, cm, { barra: .22 }); alt = pe + 1.6; }
  return { M, alt, sombra: hp };
};

// CLAUSTRO (colégio jesuíta): quadra com pátio central aberto, 2 pavimentos, telhado cerâmico em anel, caiado, janelas regulares;
// galeria de arcos no térreo do pátio. m.lado (30), m.ala_larg (8), m.andares (2)
ARQ.claustro = (m, F, cor) => {
  const M = new Malha(), lado = m.lado || m.larg || 30, prof = m.comp || lado, ww = m.ala_larg || 8, andares = m.andares || 2, pe = m.pe || 3.6, H = pe * andares;
  const x0 = -lado / 2, x1 = lado / 2, y0 = -prof / 2, y1 = prof / 2, cx0 = x0 + ww, cx1 = x1 - ww, cy0 = y0 + ww, cy1 = y1 - ww;
  const cp = cor.parede || P.cal, cm = cor.moldura || P.azul, cores = { lado: cp, topo: esc(cp, .9), fundo: cp };
  if (F.laje > 0) { M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .3 * F.laje, P.pedra); M.caixa(cx0, cx1, cy0, cy1, .3 * F.laje, .32 * F.laje, { lado: P.grama, topo: P.grama, fundo: P.grama }); }
  const hp = H * F.paredes; if (hp <= .02) return { M, alt: .3, sombra: 0 };
  // 4 alas (anel de caixas)
  M.caixa(x0, x1, y0, cy0, 0, hp, cores); M.caixa(x0, x1, cy1, y1, 0, hp, cores); M.caixa(x0, cx0, cy0, cy1, 0, hp, cores); M.caixa(cx1, x1, cy0, cy1, 0, hp, cores);
  const anel = (X0, X1, Y0, Y1, t, z0, z1, c) => { M.caixa(X0, X1, Y0, Y0 + t, z0, z1, c); M.caixa(X0, X1, Y1 - t, Y1, z0, z1, c); M.caixa(X0, X0 + t, Y0 + t, Y1 - t, z0, z1, c); M.caixa(X1 - t, X1, Y0 + t, Y1 - t, z0, z1, c); };
  anel(x0 - .06, x1 + .06, y0 - .06, y1 + .06, .12, 0, Math.min(hp, .6), P.soco);                                   // soco externo
  for (const [px, py] of [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) M.caixa(px - (px === x0 ? .09 : .36), px + (px === x0 ? .36 : .09), py - (py === y0 ? .09 : .36), py + (py === y0 ? .36 : .09), 0, hp, cm);   // cunhais externos
  for (let a = 1; a < andares; a++) if (a * pe + .1 <= hp) { anel(x0 - .1, x1 + .1, y0 - .1, y1 + .1, .15, a * pe - .16, a * pe, cm); anel(cx0, cx1, cy0, cy1, .1, a * pe - .16, a * pe, cm); }
  if (F.paredes >= 1) { anel(x0 - .12, x1 + .12, y0 - .12, y1 + .12, .17, H - .26, H, { lado: cm, topo: esc(cp, .9), fundo: cm }); anel(x0 - .02, x1 + .02, y0 - .02, y1 + .02, .06, H - .7, H - .26, { lado: esc(cp, .8), topo: cp, fundo: cp });
    anel(cx0, cx1, cy0, cy1, .1, H - .26, H, { lado: cm, topo: esc(cp, .9), fundo: cm }); }
  // janelas externas (2 pisos) + porta central na frente; pátio: arcos no térreo, janelas em cima
  for (const face of ['S', 'N', 'E', 'W']) { const L = face === 'S' || face === 'N' ? lado : prof, c0 = face === 'S' || face === 'N' ? x0 : y0;
    for (let u = c0 + 2.0; u < c0 + L - 1.4; u += 3.2) for (let a = 0; a < andares; a++) { const v0 = a * pe + 1.0;
      if (face === 'S' && a === 0 && Math.abs(u) < 1.7) { if (.1 + 3.2 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, 0, .1, 1.8, 3.2, { moldura: cm, folha: P.madeira, forma: 'arco', sal: .18, mb: .25 }); continue; }
      if (v0 + 1.7 + .2 <= hp) vao(M, face, x0, x1, y0, y1, u, v0, 1.1, 1.7, { moldura: cm, folha: P.veneziana, peitoril: true }); } }
  for (const face of ['S', 'N', 'E', 'W']) { const L = face === 'S' || face === 'N' ? cx1 - cx0 : cy1 - cy0, c0 = face === 'S' || face === 'N' ? cx0 : cy0;
    // faces internas: a face 'S' do pátio é a parede norte da ala sul etc. → usa o retângulo do pátio como caixa "invertida" (faceMap com x0/x1 trocados)
    const fm = face === 'S' ? 'N' : face === 'N' ? 'S' : face === 'E' ? 'W' : 'E', X0 = cx0, X1 = cx1, Y0 = cy0, Y1 = cy1;
    for (let u = c0 + 1.6; u < c0 + L - 1.2; u += 3.0) { if (.1 + 2.8 + .2 <= hp) vao(M, fm, X1, X0, Y1, Y0, u, .1, 1.6, 2.8, { moldura: cm, folha: P.vidro, forma: 'arco', sal: .16, mb: .22 });
      for (let a = 1; a < andares; a++) if (a * pe + 1.0 + 1.6 + .2 <= hp) vao(M, fm, X1, X0, Y1, Y0, u, a * pe + 1.0, 1.1, 1.6, { moldura: cm, folha: P.veneziana, peitoril: true }); } }
  let alt = hp;
  if (F.telhado > 0) { const dz = (1 - F.telhado) * 6, b = m.beiral || .5, t = Math.tan((m.inclina || 28) * rad), esp = .2;
    const xa = x0 - b, xb = x1 + b, ya = y0 - b, yb = y1 + b, ze = H + .1 - b * t + dz, zr = ze + (ww / 2 + b) * t, m2 = ww / 2 + b;   // cumeeira em anel no meio da ala
    const rx0 = xa + m2, rx1 = xb - m2, ry0 = ya + m2, ry1 = yb - m2, ct = cor.telha || P.telha, ct2 = cor.telha2 || P.telha2;
    const refO = [0, 0, dz - 3];
    faixasTelha(M, [xa, ya, ze], [xb, ya, ze], [rx1, ry0, zr], [rx0, ry0, zr], ct, ct2, refO); faixasTelha(M, [xb, yb, ze], [xa, yb, ze], [rx0, ry1, zr], [rx1, ry1, zr], ct, ct2, refO);
    faixasTelha(M, [xa, yb, ze], [xa, ya, ze], [rx0, ry0, zr], [rx0, ry1, zr], ct, ct2, refO); faixasTelha(M, [xb, ya, ze], [xb, yb, ze], [rx1, ry1, zr], [rx1, ry0, zr], ct, ct2, refO);
    const ix0 = cx0 + b, ix1 = cx1 - b, iy0 = cy0 + b, iy1 = cy1 - b;   // beiral do pátio
    faixasTelha(M, [ix1, iy0, ze], [ix0, iy0, ze], [rx0, ry0, zr], [rx1, ry0, zr], ct, ct2, [0, ry0, dz - 3]); faixasTelha(M, [ix0, iy1, ze], [ix1, iy1, ze], [rx1, ry1, zr], [rx0, ry1, zr], ct, ct2, [0, ry1, dz - 3]);
    faixasTelha(M, [ix0, iy0, ze], [ix0, iy1, ze], [rx0, ry1, zr], [rx0, ry0, zr], ct, ct2, [rx0, 0, dz - 3]); faixasTelha(M, [ix1, iy1, ze], [ix1, iy0, ze], [rx1, ry0, zr], [rx1, ry1, zr], ct, ct2, [rx1, 0, dz - 3]);
    const refc = [0, 0, zr - 1];
    M.quad([xa, ya, ze - esp], [xb, ya, ze - esp], [xb, ya, ze], [xa, ya, ze], P.testeira, refc); M.quad([xb, yb, ze - esp], [xa, yb, ze - esp], [xa, yb, ze], [xb, yb, ze], P.testeira, refc);
    M.quad([xb, ya, ze - esp], [xb, yb, ze - esp], [xb, yb, ze], [xb, ya, ze], P.testeira, refc); M.quad([xa, yb, ze - esp], [xa, ya, ze - esp], [xa, ya, ze], [xa, yb, ze], P.testeira, refc);
    const refi = [0, 0, zr + 30];
    M.quad([ix0, iy0, ze - esp], [ix1, iy0, ze - esp], [ix1, iy0, ze], [ix0, iy0, ze], P.testeira, refi, true); M.quad([ix1, iy1, ze - esp], [ix0, iy1, ze - esp], [ix0, iy1, ze], [ix1, iy1, ze], P.testeira, refi, true);
    M.quad([ix1, iy0, ze - esp], [ix1, iy1, ze - esp], [ix1, iy1, ze], [ix1, iy0, ze], P.testeira, refi, true); M.quad([ix0, iy1, ze - esp], [ix0, iy0, ze - esp], [ix0, iy0, ze], [ix0, iy1, ze], P.testeira, refi, true);
    for (const [p0, p1] of [[[rx0, ry0], [rx1, ry0]], [[rx1, ry0], [rx1, ry1]], [[rx1, ry1], [rx0, ry1]], [[rx0, ry1], [rx0, ry0]]]) M.barra([p0[0], p0[1], zr + .02], [p1[0], p1[1], zr + .02], .4, .2, P.cumeeira);
    for (const [e, r] of [[[xa, ya], [rx0, ry0]], [[xb, ya], [rx1, ry0]], [[xb, yb], [rx1, ry1]], [[xa, yb], [rx0, ry1]], [[ix0, iy0], [rx0, ry0]], [[ix1, iy0], [rx1, ry0]], [[ix1, iy1], [rx1, ry1]], [[ix0, iy1], [rx0, ry1]]]) M.barra([e[0], e[1], ze + .02], [r[0], r[1], zr + .02], .22, .14, P.cumeeira);
    alt = zr - dz; }
  return { M, alt, sombra: hp };
};

// MODERNO (Patronato São José, 1968): 3 pavimentos sobre muro de pedra, faixas horizontais de janelas, cobogós no 1º andar,
// pilares aparentes, lajes salientes, terraço com volume e estátua de santo (m.estatua). Claro, concreto nos pilares.
ARQ.moderno = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 22, comp = m.comp || 12, andares = m.andares || 3, pe = m.pe || 3.3, H = andares * pe + .3;
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2, cp = cor.parede || P.claro, cc = cor.moldura || P.concretoFut, cv = P.bondeVidro;
  if (F.laje > 0) M.caixa(x0 - .4, x1 + .4, y0 - .4, y1 + .4, 0, 1.2 * F.laje, { lado: P.soco, topo: esc(P.soco, 1.1), fundo: P.soco });   // muro de pedra
  const hp = (H - 1.2) * F.paredes + 1.2; if (F.paredes <= .02) return { M, alt: 1.2, sombra: 0 };
  M.caixa(x0, x1, y0, y1, 1.2, hp, { lado: cp, topo: esc(cp, .92), fundo: cp });
  for (let a = 1; a <= andares; a++) { const z = 1.2 + a * pe; if (z <= hp) M.caixa(x0 - .35, x1 + .35, y0 - .35, y1 + .35, z - .28, z, cc); }   // lajes salientes
  for (let x = x0 + .2; x <= x1 - .2 + .01; x += (larg - .4) / Math.max(1, Math.round((larg - .4) / 3.6))) for (const [yy, s] of [[y0, -1], [y1, 1]]) M.caixa(x - .22, x + .22, yy + (s < 0 ? -.32 : -.1), yy + (s < 0 ? .1 : .32), 1.2, hp, cc);   // pilares aparentes
  for (let a = 0; a < andares; a++) { const zb = 1.2 + a * pe + .9, zt = zb + 1.5; if (zt + .2 > hp) continue;
    for (const [face, yy, d] of [['S', y0, -1], ['N', y1, 1]]) {
      if (a === 1 && face === 'S') { for (let x = x0 + .9; x + .35 < x1 - .9; x += .42) for (let z = zb; z + .35 < zt; z += .42) if (((Math.round(x * 10) + Math.round(z * 10)) & 1) === 0) M.caixa(x, x + .35, yy + (d < 0 ? -.08 : .02), yy + (d < 0 ? -.02 : .08), z, z + .35, cv); }   // cobogós
      else { M.caixa(x0 + .8, x1 - .8, yy + (d < 0 ? -.05 : .01), yy + (d < 0 ? -.01 : .05), zb, zt, cv);
        for (let x = x0 + .8; x <= x1 - .8 + .01; x += 1.2) M.caixa(x - .04, x + .04, yy + (d < 0 ? -.08 : .02), yy + (d < 0 ? -.02 : .08), zb, zt, P.branco); } } }
  let alt = hp;
  if (F.telhado > 0 && hp >= H - .01) { const k = F.telhado;
    M.caixa(x0 - .1, x1 + .1, y0 - .1, y0 + .25, H, H + .7 * k, cc); M.caixa(x0 - .1, x1 + .1, y1 - .25, y1 + .1, H, H + .7 * k, cc); M.caixa(x0 - .1, x0 + .25, y0, y1, H, H + .7 * k, cc); M.caixa(x1 - .25, x1 + .1, y0, y1, H, H + .7 * k, cc);
    alt = H + .7; }
  if (F.coroa > 0 && hp >= H - .01) { const k = F.coroa, vw = Math.min(7, larg * .3), vd = Math.min(5, comp * .5);
    M.caixa(-vw / 2, vw / 2, -vd / 2, vd / 2, H, H + 2.8 * k, { lado: cp, topo: esc(cp, .92), fundo: cp });
    M.caixa(-vw / 2 + .6, vw / 2 - .6, -vd / 2 - .04, -vd / 2 - .01, H + .9, H + 2.2 * k, cv);
    if (m.estatua !== false) { const z = H + 2.8 * k, e = m.estatua_alt || 3.6; M.caixa(-.7, .7, -.7, .7, z, z + .6 * k, cc);   // santo: pedestal, corpo, cabeça, braços abertos
      M.prisma(poliReg(0, 0, .55, 8), z + .6 * k, z + (.6 + e * .72) * k, P.branco, P.branco, null); M.prisma(poliReg(0, 0, .34, 8), z + (.6 + e * .72) * k, z + (.6 + e * .9) * k, P.branco, P.branco, null);
      M.barra([-1.1 * k, 0, z + (.6 + e * .55) * k], [1.1 * k, 0, z + (.6 + e * .55) * k], .28, .28, P.branco); }
    alt = H + 2.8 + 4.2; }
  return { M, alt, sombra: hp };
};

// CATEDRAL MODERNA: dois volumes curvos brancos (quartos de cilindro) abraçando um corpo central amarelo-ocre com rosácea e porta em arco,
// campanário em arco aberto no eixo com sino e cruz branca grande, escada de 5 degraus, nave atrás com cobertura baixa de zinco
ARQ.catedral_moderna = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 24, comp = m.comp || 36, cl = m.corpo || 10, hc = m.pe || 12, hv = m.volume_alt || 9, r = (larg - cl) / 2, hn = m.nave_alt || 9;
  const y0 = -comp / 2, y1 = comp / 2, cb = cor.parede || P.ocreParede, cw = P.branco, cm = cor.moldura || P.ocre;
  if (F.laje > 0) { M.caixa(-larg / 2 - 1, larg / 2 + 1, y0 - 4, y1 + .5, 0, .2 * F.laje, P.pedra);
    for (let i = 0; i < 5; i++) M.caixa(-cl / 2 - 1 + i * .15, cl / 2 + 1 - i * .15, y0 - 1.6 + i * .32, y0 + .02, 0, (.2 + .16 * i) * F.laje, P.pedra); }
  const k = F.paredes; if (k <= .02) return { M, alt: .5, sombra: 0 };
  M.caixa(-cl / 2, cl / 2, y0, y0 + 6, 0, hc * k, { lado: cb, topo: esc(cb, .9), fundo: cb });                             // corpo central
  for (const s of [-1, 1]) { const c = [s * cl / 2, y0 + r], pol = [[c[0], c[1]]]; for (let i = 0; i <= 8; i++) { const a = s < 0 ? Math.PI + i / 8 * Math.PI / 2 : 2 * Math.PI - i / 8 * Math.PI / 2; pol.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
    if (s > 0) pol.reverse(); M.prisma(pol, 0, hv * k, cw, esc(cw, .9), null); }                                           // volumes curvos
  M.caixa(-10, 10, y0 + 6, y1, 0, hn * k, { lado: cw, topo: esc(cw, .9), fundo: cw });                                      // nave
  if (.1 + 4.5 + .2 <= hc * k) vao(M, 'S', -cl / 2, cl / 2, y0, y0 + 6, 0, .1, 3.0, 4.5, { moldura: cm, folha: P.ferro, forma: 'arco', sal: .2, mb: .3 });
  if (6.2 + 4.0 + .2 <= hc * k) vao(M, 'S', -cl / 2, cl / 2, y0, y0 + 6, 0, 6.2, 4.0, 4.0, { moldura: cw, folha: P.vitral, forma: 'oculo', sal: .22, mb: .3 });   // rosácea
  for (const u of [-cl / 2 + 1.1, cl / 2 - 1.1]) for (const v0 of [1.2, 7.0]) if (v0 + 2.4 + .2 <= hc * k) vao(M, 'S', -cl / 2, cl / 2, y0, y0 + 6, u, v0, .6, 2.4, { moldura: cm, folha: P.vidro });
  for (const face of ['E', 'W']) for (let u = y0 + 9; u < y1 - 2; u += 4) if (2 + 4 + .2 <= hn * k) vao(M, face, -10, 10, y0 + 6, y1, u, 2, .7, 4, { moldura: cm, folha: P.vitral });
  let alt = hc * k;
  if (F.telhado > 0) { const rr = telhado2(M, -10, 10, y0 + 6, y1, hn, 14, .4, 'y', { telha: P.aco2, telha2: esc(P.aco2, .94), testeira: P.aco2, sofito: esc(P.aco2, .8), cumeeira: esc(P.aco2, .8), parede: cw }, (1 - F.telhado) * 4); alt = Math.max(alt, hn + rr.alt); }
  if (F.coroa > 0) { const kc = F.coroa, yz = y0 + 3, zt = hc + 6 * kc, ra = 2.2;                                           // campanário em arco aberto + sino + cruz
    for (const s of [-1, 1]) M.caixa(s * ra - .4 + (s < 0 ? -.4 : 0), s * ra + .4 + (s > 0 ? .4 : 0), yz - .5, yz + .5, hc, zt, cw);
    const arco = []; for (let i = 0; i <= 8; i++) { const a = Math.PI - i / 8 * Math.PI; arco.push([ra * Math.cos(a) * (1 + .2 * (1 - Math.abs(Math.cos(a)))), yz, zt + ra * Math.sin(a) * kc]); }
    for (let i = 0; i < 8; i++) M.barra(arco[i], arco[i + 1], 1.0, .8, cw);
    M.prisma(poliReg(0, yz, .4, 8), zt - .2, zt + .5 * kc, P.bronze, P.bronze, P.bronze); M.barra([0, yz, zt + .5 * kc], [0, yz, zt + ra * kc], .08, .08, P.ferro);   // sino
    const zc = zt + ra * kc + .4; M.barra([0, yz, zc], [0, yz, zc + 4.5 * kc], .5, .5, cw); M.barra([-1.6 * kc, yz, zc + 3.2 * kc], [1.6 * kc, yz, zc + 3.2 * kc], .5, .5, cw);
    alt = Math.max(alt, zc + 4.5); }
  return { M, alt, sombra: hc * k };
};

// PREFEITURA / CÂMARA eclética (~1900): 2 pisos, pilastras claras sobre parede cor, janelas em arco, platibanda com frontispício, escadaria
ARQ.prefeitura = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 18, comp = m.comp || 14, pe1 = m.pe || 4.3, pe2 = (m.pe || 4.3) - .3, H = pe1 + pe2, plat = m.platibanda || 1.3;
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2, cp = cor.parede || P.rosa, cm = cor.moldura || P.branco;
  if (F.laje > 0) { M.caixa(x0 - .3, x1 + .3, y0 - .3, y1 + .3, 0, .4 * F.laje, P.pedra);
    for (let i = 0; i < 4; i++) M.caixa(-3.2 + i * .25, 3.2 - i * .25, y0 - 2.2 + i * .5, y0 + .1, 0, (.12 + .15 * i) * F.laje, P.pedra); } // escadaria
  const hp = H * F.paredes; if (hp <= .02) return { M, alt: .4, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: .9, cunhal: .6, cornija: 0, corSoco: P.soco });
  if (pe1 + .1 <= hp) M.caixa(x0 - .14, x1 + .14, y0 - .14, y1 + .14, pe1 - .25, pe1, cm);   // cimalha entre pisos
  const passo = 2.9, n = Math.max(3, Math.floor((larg - 1.4) / passo) | 1), u0 = -(n - 1) * passo / 2;
  for (let i = 0; i < n; i++) { const u = u0 + i * passo, centro = i === (n - 1) / 2;
    if (i < n - 1 && hp > .5) M.caixa(u + passo / 2 - .25, u + passo / 2 + .25, y0 - .12, y0 + .1, .9, hp, cm);            // pilastras da fachada
    if (centro) { if (.1 + 3.6 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, u, .1, 2.4, 3.6, { moldura: cm, folha: P.madeira, forma: 'arco', sal: .2, mb: .28 }); }
    else if (.9 + 2.5 + .2 <= hp) vao(M, 'S', x0, x1, y0, y1, u, .9, 1.3, 2.5, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: true });
    if (pe1 + .9 + 2.6 + .2 <= hp) { vao(M, 'S', x0, x1, y0, y1, u, pe1 + .9, 1.3, 2.6, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: !centro }); if (centro || Math.abs(i - (n - 1) / 2) === 1) sacada(M, 'S', x0, x1, y0, y1, u, pe1 + .9, 1.3, cm); } }
  for (const face of ['E', 'W', 'N']) { const L = face === 'N' ? larg : comp, c0 = face === 'N' ? x0 : y0;
    for (let uu = c0 + 1.8; uu < c0 + L - 1.4; uu += 3.0) for (const [v0, h] of [[.9, 2.5], [pe1 + .9, 2.6]]) if (v0 + h + .2 <= hp) vao(M, face, x0, x1, y0, y1, uu, v0, 1.25, h, { moldura: cm, folha: P.vidro, forma: 'arco', peitoril: true }); }
  let alt = hp;
  if (F.telhado > 0) { const k = F.telhado, e = .12;   // platibanda (sobe com a fase do telhado), cornija e laje de cobertura
    M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, H, H + .35, cm);
    M.caixa(x0, x1, y0, y1, H + .35, H + .35 + plat * k, { lado: cp, topo: cm, fundo: cp });
    M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, H + .35 + plat * k - .2, H + .35 + plat * k, cm);
    M.caixa(x0 + .35, x1 - .35, y0 + .35, y1 - .35, H, H + .2, P.ardosia);   // cobertura plana escura atrás da platibanda
    alt = H + .35 + plat; }
  if (F.coroa > 0) { const k = F.coroa, zt = H + .35 + plat, fw = 3.4;   // frontispício central e pináculos nos cantos
    M.caixa(-fw, fw, y0 - .2, y0 + 1.0, zt, zt + .9 * k, { lado: cp, topo: cm });
    M.tri([-fw - .2, y0 - .25, zt + .9 * k], [fw + .2, y0 - .25, zt + .9 * k], [0, y0 - .25, zt + .9 * k + 1.6 * k], cm, [0, 5, zt]);
    M.tri([-fw - .2, y0 + 1.0, zt + .9 * k], [fw + .2, y0 + 1.0, zt + .9 * k], [0, y0 + 1.0, zt + .9 * k + 1.6 * k], cm, [0, -5, zt]);
    M.quad([-fw - .2, y0 - .25, zt + .9 * k], [0, y0 - .25, zt + .9 * k + 1.6 * k], [0, y0 + 1.0, zt + .9 * k + 1.6 * k], [-fw - .2, y0 + 1.0, zt + .9 * k], cm, [0, 0, zt]);
    M.quad([fw + .2, y0 - .25, zt + .9 * k], [0, y0 - .25, zt + .9 * k + 1.6 * k], [0, y0 + 1.0, zt + .9 * k + 1.6 * k], [fw + .2, y0 + 1.0, zt + .9 * k], cm, [0, 0, zt]);
    for (const [x, y] of [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]) { const px = x === x0 ? x0 + .35 : x1 - .35, py = y === y0 ? y0 + .35 : y1 - .35;
      M.caixa(px - .4, px + .4, py - .4, py + .4, zt, zt + .6 * k, cm); M.piramide(ret(px - .4, px + .4, py - .4, py + .4), zt + .6 * k, [px, py, zt + .6 * k + .9 * k], cm); }
    alt = Math.max(alt, zt + 2.5); }
  return { M, alt, sombra: hp };
};

// CORETO de praça: base octogonal de pedra, 8 colunas de ferro, guarda-corpo, cobertura octogonal de zinco com remate
ARQ.coreto = (m, F, cor) => {
  const M = new Malha(), r = m.raio || 3.6, cm = cor.moldura || P.verde;
  if (F.laje > 0) M.prisma(poliReg(0, 0, r + .3, 8, Math.PI / 8), 0, 1.0 * F.laje, P.soco, P.pedra);
  const k = F.paredes; if (k <= .02) return { M, alt: 1, sombra: 0 };
  const hc = 3.3 * k, base = poliReg(0, 0, r - .25, 8, Math.PI / 8);
  for (const [x, y] of base) M.barra([x, y, 1.0], [x, y, 1.0 + hc], .22, .22, cm);
  if (k >= 1) for (let i = 0; i < 8; i++) { const a = base[i], b = base[(i + 1) % 8];
    M.barra([a[0], a[1], 1.95], [b[0], b[1], 1.95], .07, .07, P.ferro); M.barra([a[0], a[1], 1.45], [b[0], b[1], 1.45], .05, .05, P.ferro);
    for (let j = 1; j < 4; j++) { const x = lerp(a[0], b[0], j / 4), y = lerp(a[1], b[1], j / 4); M.barra([x, y, 1.0], [x, y, 1.95], .05, .05, P.ferro); } }
  let alt = 1 + hc;
  if (F.telhado > 0) { const dz = (1 - F.telhado) * 4, z0 = 1 + 3.3 + dz, topo = poliReg(0, 0, r + .5, 8, Math.PI / 8);
    M.prisma(topo, z0 - .3, z0, P.ferro, null, P.sofito);
    M.piramide(topo, z0, [0, 0, z0 + 2.2], cor.telha || P.zinco); M.piramide(poliReg(0, 0, r + .5 - .35, 8, Math.PI / 8), z0, [0, 0, z0 + 2.2 - .2], esc(cor.telha || P.zinco, .9)); // sob o telhado (duas camadas)
    M.barra([0, 0, z0 + 2.1], [0, 0, z0 + 3.1], .16, .16, cm); M.prisma(poliReg(0, 0, .28, 8), z0 + 2.2, z0 + 2.5, cm); alt = z0 + 3.1 - dz; }
  return { M, alt, sombra: 1 + hc };
};

// GENÉRICO: casarão/galpão de 4 águas (usa o sobrado com 1 andar e sem sacadas)
ARQ.casarao = (m, F, cor) => ARQ.sobrado({ ...m, andares: m.andares || 1, sacadas: false }, F, cor);

// ---- futuro
// TORRE DE VIDRO moderada: planta chanfrada, faixas por pavimento (vidro + peitoril), pódio, coroamento
ARQ.torre_vidro = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 18, comp = m.comp || 18, andares = m.andares || 10, pe = m.pe || 3.4, ch = Math.min(larg, comp) * .18;
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2;
  const pol = [[x0 + ch, y0], [x1 - ch, y0], [x1, y0 + ch], [x1, y1 - ch], [x1 - ch, y1], [x0 + ch, y1], [x0, y1 - ch], [x0, y0 + ch]];
  const vd = cor.vidro || P.vidroFut, vd2 = cor.vidro2 || P.vidroFut2, ac = cor.aco || P.aco;
  M.prisma(pol.map(([x, y]) => [x * 1.12, y * 1.12]), 0, pe * 1.4, P.concretoFut, esc(P.telhadoVerde, 1), P.concretoFut);   // pódio com telhado verde
  for (let a = 0; a < andares; a++) { const z = pe * 1.4 + a * pe; M.prisma(pol, z, z + pe * .72, (a % 3 === 2) ? vd2 : vd, null, null); M.prisma(pol.map(([x, y]) => [x * 1.01, y * 1.01]), z + pe * .72, z + pe, ac, null, null); }
  const zt = pe * 1.4 + andares * pe;
  M.prisma(pol, zt, zt + .3, ac, P.telhadoVerde2, null);
  M.prisma(pol.map(([x, y]) => [x * .45, y * .45]), zt + .3, zt + 2.2, P.aco2, P.aco2, null);
  if (m.solar !== false) paineis(M, x0 * .9, x1 * .9, y0 * .9, y1 * .9, zt + .3, P.solar);
  return { M, alt: zt + 2.2, sombra: zt };
};
// painéis solares inclinados em fileiras sobre um telhado plano (z)
function paineis(M, x0, x1, y0, y1, z, cor) {
  for (let y = y0 + .5; y + 2.2 < y1; y += 2.9) for (let x = x0 + .5; x + 1.8 < x1; x += 2.0) {
    const ref = [x + .9, y + 1.1, z - 1]; M.quad([x, y, z + .3], [x + 1.8, y, z + .3], [x + 1.8, y + 2.0, z + 1.1], [x, y + 2.0, z + 1.1], cor, ref);
    M.quad([x, y, z + .25], [x + 1.8, y, z + .25], [x + 1.8, y + 2.0, z + 1.05], [x, y + 2.0, z + 1.05], P.solarMoldura, [x + .9, y + 1.1, z + 5]);
    M.barra([x + .9, y + 1.6, z], [x + .9, y + 1.6, z + .9], .08, .08, P.aco2); }
}
// PRÉDIO COM TELHADO VERDE (4–6 pisos), varandas, painéis solares
ARQ.telhado_verde = (m, F, cor) => {
  const M = new Malha(), larg = m.larg || 22, comp = m.comp || 14, andares = m.andares || 5, pe = m.pe || 3.2, H = andares * pe;
  const x0 = -larg / 2, x1 = larg / 2, y0 = -comp / 2, y1 = comp / 2, cp = cor.parede || P.concretoFut;
  M.caixa(x0, x1, y0, y1, 0, H, { lado: cp, topo: P.telhadoVerde, fundo: cp });
  const pb = { lado: cp, topo: esc(cp, .92), fundo: cp };   // platibanda em anel (4 caixas), para o telhado verde aparecer
  M.caixa(x0 - .1, x1 + .1, y0 - .1, y0 + .3, H, H + .9, pb); M.caixa(x0 - .1, x1 + .1, y1 - .3, y1 + .1, H, H + .9, pb);
  M.caixa(x0 - .1, x0 + .3, y0, y1, H, H + .9, pb); M.caixa(x1 - .3, x1 + .1, y0, y1, H, H + .9, pb);
  M.caixa(x0 + .3, x1 - .3, y0 + .3, y1 - .3, H, H + .35, { lado: P.telhadoVerde2, topo: P.telhadoVerde, fundo: P.telhadoVerde2 });
  for (let a = 0; a < andares; a++) { const z = a * pe + .9;
    for (let u = x0 + 1.6; u + 2.6 < x1; u += 3.4) { M.caixa(u, u + 2.6, y0 - .04, y0 - .01, z, z + 1.7, P.bondeVidro); M.caixa(u - .2, u + 2.8, y0 - 1.2, y0, z - .9, z - .75, cp); M.barra([u - .2, y0 - 1.2, z - .75], [u + 2.8, y0 - 1.2, z + .25], .05, .05, P.aco2); M.barra([u - .2, y0 - 1.15, z + .25], [u + 2.8, y0 - 1.15, z + .25], .06, .05, P.aco2); }
    for (let u = x0 + 1.6; u + 2.6 < x1; u += 3.4) M.caixa(u, u + 2.6, y1 + .01, y1 + .04, z, z + 1.7, P.bondeVidro); }
  if (m.solar !== false) paineis(M, x0 + .6, x1 - .6, y0 + comp * .5, y1 - .6, H + .35, P.solar);
  for (let i = 0; i < 4; i++) { const x = x0 + 2 + i * (larg - 4) / 3; M.caixa(x - .6, x + .6, y0 + 1.2, y0 + 2.4, H + .35, H + .85, P.aco2); }   // floreiras
  return { M, alt: H + .9, sombra: H };
};
// BONDE / VLT: carro arredondado (chanfros), faixa colorida, janelas contínuas; comprimento ao longo de +x
ARQ.bonde = (m, F, cor) => {
  const M = new Malha(), L = m.comp || 24, W = 2.6, H = 3.3, ch = .35, x0 = -L / 2, x1 = L / 2;
  const pol = [[x0 + ch, -W / 2], [x1 - ch, -W / 2], [x1, -W / 2 + ch], [x1, W / 2 - ch], [x1 - ch, W / 2], [x0 + ch, W / 2], [x0, W / 2 - ch], [x0, -W / 2 + ch]];
  M.prisma(pol, .35, 1.0, cor.faixa || P.bondeFaixa, null, P.ferro);
  M.prisma(pol, 1.0, 1.2, P.bonde, null, null);
  M.prisma(pol.map(([x, y]) => [x, y * .985]), 1.2, 2.6, P.bondeVidro, null, null);
  M.prisma(pol, 2.6, H, P.bonde, esc(P.bonde, .9), null);
  M.prisma(pol.map(([x, y]) => [x * .9, y * .8]), H, H + .35, P.aco2, P.aco2, null);
  for (let x = x0 + 1.5; x < x1 - 1; x += 5.5) M.caixa(x, x + .18, -W / 2 - .02, W / 2 + .02, 1.0, 2.6, P.bonde);   // montantes entre janelas
  return { M, alt: H + .35, sombra: H };
};
// ÁRVORE: tronco hexagonal + copa low-poly em anéis; ou palmeira (tronco fino com 9 folhas)
ARQ.arvore = (m, F, cor) => {
  const M = new Malha(), tipo = m.arvore || 'redonda';
  if (tipo === 'palmeira') {
    const h = 11; M.prisma(poliReg(0, 0, .26, 6), 0, h * .55, P.palmaTronco, null, P.palmaTronco); M.prisma(poliReg(0, 0, .2, 6), h * .55, h, esc(P.palmaTronco, 1.06), esc(P.palmaTronco, 1.06), null);
    M.prisma(poliReg(0, 0, .45, 8), h - .3, h + .4, esc(P.palma, .8), esc(P.palma, .8), null);
    for (let i = 0; i < 9; i++) { const a = i / 9 * 2 * Math.PI + (i % 2) * .2, cx = Math.cos(a), sy = Math.sin(a), c = i % 2 ? P.palma : P.palma2;
      const pts = [[0, 0, h + .2], [cx * 1.6, sy * 1.6, h + 1.3], [cx * 3.2, sy * 3.2, h + 1.1], [cx * 4.6, sy * 4.6, h - .3], [cx * 5.2, sy * 5.2, h - 1.8]];
      const w = [.15, .45, .55, .4, .1], px = -sy, py = cx, ref = [cx * 2.5, sy * 2.5, h - 4];
      for (let j = 0; j < pts.length - 1; j++) { const a0 = pts[j], a1 = pts[j + 1], w0 = w[j], w1 = w[j + 1];
        M.quad([a0[0] - px * w0, a0[1] - py * w0, a0[2]], [a0[0] + px * w0, a0[1] + py * w0, a0[2]], [a1[0] + px * w1, a1[1] + py * w1, a1[2]], [a1[0] - px * w1, a1[1] - py * w1, a1[2]], c, ref);
        M.quad([a0[0] - px * w0, a0[1] - py * w0, a0[2] - .06], [a0[0] + px * w0, a0[1] + py * w0, a0[2] - .06], [a1[0] + px * w1, a1[1] + py * w1, a1[2] - .06], [a1[0] - px * w1, a1[1] - py * w1, a1[2] - .06], esc(c, .7), [cx * 2.5, sy * 2.5, h + 8]); } }
    return { M, alt: h + 1.5, sombra: h };
  }
  const h = 7.5; M.prisma(poliReg(0, 0, .32, 6), 0, 3.0, P.tronco, null, P.tronco);
  const aneis = [[2.2, 1.4, 0], [3.3, 2.7, .35], [4.6, 2.9, .1], [5.8, 2.2, .5], [6.7, 1.1, .2]];
  const ring = (r, z, f) => poliReg(0, 0, r, 7, f).map(([x, y]) => [x, y, z]);
  let prev = ring(.4, 1.9, 0); const refc = [0, 0, 4.3];
  for (let i = 0; i < aneis.length; i++) { const [z, r, f] = aneis[i], cur = ring(r, z, f);
    for (let j = 0; j < 7; j++) { const c = (i + j) % 3 === 0 ? P.copa2 : (i + j) % 3 === 1 ? P.copa : P.copa3; M.quad(prev[j], prev[(j + 1) % 7], cur[(j + 1) % 7], cur[j], c, refc); }
    prev = cur; }
  M.poli(prev.map(p => [p[0], p[1], h + .1]), P.copa3, refc);
  for (let j = 0; j < 7; j++) M.tri(prev[j], prev[(j + 1) % 7], [0, 0, h + .3], P.copa, refc);
  return { M, alt: h + .3, sombra: h };
};

// ---------------------------------------------------------------- malha de um marco (com cache)
const CACHE = new Map();
function coresDe(m, dest) {
  const cm = m.cor ? (typeof m.cor === 'string' ? P[m.cor] || hex(m.cor) : m.cor.map(v => v / 255)) : null;
  const base = { moldura: cm || (ARQ_MOLD[m.tipo] || P.azul), parede: m.parede ? (P[m.parede] || hex(m.parede)) : undefined,
    telha: m.telha ? (P[m.telha] || hex(m.telha)) : undefined, telha2: m.telha ? esc(P[m.telha] || hex(m.telha), .88) : undefined };
  if (dest) base.moldura = P.amb;   // destaque: molduras/cunhais/cruz em amarelo INEMA
  return base;
}
const ARQ_MOLD = { estacao: P.tijolo, prefeitura: P.branco, coreto: P.verde, estacao_castelo: P.branco, chafariz: P.verdeEscuro, moderno: P.concretoFut, catedral_moderna: P.ocre, claustro: P.azul };
// m: {id, tipo, rumo, larg, comp, andares, cor, ...}; k: progresso 0..1; dest: destaque; ez: exagero vertical
function malha(m, k = 1, dest = false, ez = 1) {
  const F = fases(k), fn = ARQ[m.tipo]; if (!fn) throw new Error('marco sem tipo conhecido: ' + m.tipo);
  const r = fn(m, F, coresDe(m, dest)), th = 180 - (m.rumo ?? 180);
  r.M.gira(th).escalaZ(ez);
  const o = r.M.pronto(); o.alt = r.alt * ez; o.sombra = r.sombra * ez; o.th = th; return o;
}
function malhaCache(m, k, dest, ez) {
  const kq = k >= 1 ? 'ok' : Math.round(k * 60), chave = `${m.id}|${m.tipo}|${kq}|${dest ? 1 : 0}|${ez}`;
  if (CACHE.has(chave)) return CACHE.get(chave);
  const o = malha(m, k, dest, ez);
  if (kq === 'ok') CACHE.set(chave, o); else { for (const c of [...CACHE.keys()]) if (c.startsWith(`${m.id}|${m.tipo}|`) && !/\|ok\|/.test(c)) CACHE.delete(c); CACHE.set(chave, o); }
  return o;
}
const malhaUnidade = (tipo, extra = {}) => { const ch = `unid|${tipo}|${JSON.stringify(extra)}`; if (!CACHE.has(ch)) CACHE.set(ch, malha({ id: 'u', tipo, rumo: 180, ...extra }, 1, false, 1)); return CACHE.get(ch); };

// ---------------------------------------------------------------- geometria auxiliar
const M_LAT = 111320;
const mLon = lat => M_LAT * Math.cos(lat * rad);
// sombra no chão: casco convexo da base ∪ base deslocada pela luz (altura h)
function sombraPoli(m, larg, comp, h, luz) {
  const th = (180 - (m.rumo ?? 180)) * rad, c = Math.cos(th), s = Math.sin(th);
  const dx = -luz[0] / luz[2] * h, dy = -luz[1] / luz[2] * h, pts = [];
  for (const [x, y] of [[-larg / 2, -comp / 2], [larg / 2, -comp / 2], [larg / 2, comp / 2], [-larg / 2, comp / 2]]) {
    const X = c * x - s * y, Y = s * x + c * y; pts.push([X, Y], [X + dx, Y + dy]); }
  pts.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lower = []; for (const p of pts) { while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) lower.pop(); lower.push(p); }
  const upper = []; for (const p of pts.slice().reverse()) { while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) upper.pop(); upper.push(p); }
  const hull = lower.slice(0, -1).concat(upper.slice(0, -1)), kx = 1 / mLon(m.lat), ky = 1 / M_LAT;
  return hull.map(([x, y]) => [m.lon + x * kx, m.lat + y * ky]);
}
function dimsDe(m) {
  const t = m.tipo; if (t === 'igreja') return [(m.larg || 12) + 5, (m.comp || 28) + (m.sacristia || 7)];
  if (t === 'coreto') return [(m.raio || 3.6) * 2, (m.raio || 3.6) * 2]; if (t === 'estacao') return [m.larg || 24, (m.comp || 9) + 4];
  if (t === 'estacao_castelo') return [(m.torre_m || 6) + 2 * (m.ala || 9), (m.comp || 7) + (m.plataforma !== false ? 4 : 0)];
  if (t === 'chafariz') return [(m.larg || 3.2) + .8, (m.comp || 3) + 1.6]; if (t === 'claustro') return [m.lado || m.larg || 30, m.comp || m.lado || 30];
  if (t === 'moderno') return [m.larg || 22, m.comp || 12]; if (t === 'catedral_moderna') return [m.larg || 24, m.comp || 36];
  return [m.larg || 12, m.comp || 13];
}
// ponto dentro de polígono [[lon,lat],...]
function dentroPoli(p, pol) { let c = false; for (let i = 0, j = pol.length - 1; i < pol.length; j = i++) { const a = pol[i], b = pol[j];
  if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; }
// semeia n pontos num polígono (lon/lat), com distância mínima dmin (m); determinístico pela semente
function semear(pol, n, semente = 1, dmin = 4) {
  let sd = semente * 7919 + 13; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
  const lons = pol.map(p => p[0]), lats = pol.map(p => p[1]), w = Math.min(...lons), e = Math.max(...lons), s = Math.min(...lats), nn = Math.max(...lats);
  const out = [], kx = mLon((s + nn) / 2); let tent = 0;
  while (out.length < n && tent++ < n * 60) { const p = [w + rnd() * (e - w), s + rnd() * (nn - s)];
    if (!dentroPoli(p, pol)) continue; if (out.some(q => Math.hypot((q[0] - p[0]) * kx, (q[1] - p[1]) * M_LAT) < dmin)) continue;
    out.push(p); }
  return out.map((p, i) => ({ lon: p[0], lat: p[1], esc: .75 + rnd() * .5, giro: rnd() * 360, tinta: [230 + rnd() * 25, 235 + rnd() * 20, 215 + rnd() * 40].map(Math.round), i }));
}
// t em que anoEm(t) atinge `ano` (inverte C.anos, que é linear por trechos)
function tDoAno(C, ano) {
  const A = C.anos; if (!A) return 0; if (ano <= A[0][1]) return A[0][0];
  for (let i = 1; i < A.length; i++) if (A[i][1] >= ano) { const [t0, a0] = A[i - 1], [t1, a1] = A[i]; return a1 === a0 ? t1 : t0 + (ano - a0) / (a1 - a0) * (t1 - t0); }
  return Infinity;
}
const dentroJ = (t, j) => !!j && j.some(([a, b]) => t >= a && t <= b);
// caminho [[lon,lat,z?],...] → função s (m) → {p:[lon,lat,z], yaw}
function aoLongo(caminho) {
  const cum = [0], m = []; for (let i = 1; i < caminho.length; i++) { const a = caminho[i - 1], b = caminho[i], kx = mLon((a[1] + b[1]) / 2);
    const dx = (b[0] - a[0]) * kx, dy = (b[1] - a[1]) * M_LAT; m.push([dx, dy]); cum.push(cum[i - 1] + Math.hypot(dx, dy)); }
  const L = cum[cum.length - 1];
  return { L, em(s) { s = ((s % L) + L) % L; let i = 1; while (i < cum.length - 1 && cum[i] < s) i++;
    const u = (s - cum[i - 1]) / ((cum[i] - cum[i - 1]) || 1), a = caminho[i - 1], b = caminho[i];
    return { p: [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2] || 0, b[2] || 0, u)], yaw: Math.atan2(m[i - 1][1], m[i - 1][0]) / rad }; } };
}

// ---------------------------------------------------------------- camadas
const MAT = { ambient: .5, diffuse: .45, shininess: 20, specularColor: [40, 40, 40] };
const MAT_VIDRO = { ambient: .55, diffuse: .5, shininess: 60, specularColor: [120, 130, 140] };
const BRANCO = [255, 255, 255];
const LUZ_PADRAO = [-2, 3, -3.2];   // sol do sudeste, meio baixo: ilumina as fachadas sul e leste, sombras legíveis (ver DESIGN-PREDIOS.md)

// MARCOS.camadas(t, ano, C, D, opts) → camadas deck (marcos, sombras, destaques, árvores, futuro, pisos)
// C.marcos, C.arvores, C.arvores_auto, C.futuro, C.pisos, C.ruas; opts: {terreno: [ext], luz: [x,y,z], ez}
function camadas(t, ano, C, D, opts = {}) {
  const L = [], EXZ = C.exz || 1, ez = opts.ez ?? C.marcos_ez ?? C.exb ?? 1, luz = opts.luz || C.luz || LUZ_PADRAO, ext = opts.terreno || [];
  D._marcos = D._marcos || {};
  const zDe = o => (o.z ?? (D.elev ? elevEm(D, o.lon, o.lat) : 0)) * EXZ;
  const sombras = [], halos = [];
  // --- pisos (praças, adros) e ruas desenhadas
  for (const p of (C.pisos || [])) { if (ano < (p.ano ?? -1e9) || t < (p.t0 ?? -1) || t > (p.t1 ?? 1e9)) continue;
    L.push(new deck.SolidPolygonLayer({ id: 'piso-' + p.id, data: [p], getPolygon: d => d.poligono.map(q => [q[0], q[1], (q[2] ?? p.z ?? 0) * EXZ + .05]), getFillColor: p.cor || [160, 154, 142], material: false, extensions: ext })); }
  // ruas numa camada só (versão centro: ~2.500 trechos); cada rua aparece no seu ano (fade de 3 anos) — data em ordem: calçadas antes do asfalto
  if (C.ruas && C.ruas.length) {
    const ra = Math.round(ano * 4) / 4;
    L.push(new deck.PathLayer({ id: 'ruas', data: C.ruas, getPath: d => d._p || (d._p = d.caminho.map(q => [q[0], q[1], (q[2] ?? d.z ?? 0) * EXZ + .08])),
      getColor: d => [...(d.cor || [120, 116, 108]), Math.round(255 * clamp01((ra - (d.ano ?? -1e9)) / 3))], getWidth: d => d.larg || 8,
      widthUnits: 'meters', capRounded: true, jointRounded: true, extensions: ext, updateTriggers: { getColor: ra } })); }
  // --- marcos
  for (const m of (C.marcos || [])) {
    if (m._t0 === undefined) { m._t0 = m.t0 ?? tDoAno(C, m.ano ?? -1e9);
      const ate = m.ate ?? m.some_ano; m._t1 = ate !== undefined ? tDoAno(C, ate) : Infinity;                    // `ate`/`some_ano`: desmonta em `desmonta` s (padrão 2) a partir do ano
      m._dura = m.pronto !== undefined ? Math.max(.5, tDoAno(C, m.pronto) - m._t0) : (m.dura || 3); }           // `pronto`: a obra vai do t do `ano` ao t do `pronto`
    let k = m.k !== undefined ? m.k : m.sempre ? 1 : clamp01((t - m._t0) / m._dura);
    if (t > m._t1) k = Math.min(k, 1 - clamp01((t - m._t1) / (m.desmonta || 2)));
    if (k <= 0) continue;
    const dest = dentroJ(t, m.destaque), o = malhaCache(m, k, dest, ez), z = zDe(m);
    m._data = m._data || [m];
    L.push(new deck.SimpleMeshLayer({ id: 'marco-' + m.id, data: m._data, mesh: o, getPosition: [m.lon, m.lat, z], getColor: BRANCO, getOrientation: [0, 0, 0], material: MAT }));
    const [dl, dc] = dimsDe(m);
    if (o.sombra > 0) sombras.push({ p: sombraPoli(m, dl, dc, o.sombra, luz).map(q => [q[0], q[1], z + .04]), a: Math.round(92 * Math.min(1, k * 2)) });
    if (dest) halos.push({ lon: m.lon, lat: m.lat, z, r: Math.hypot(dl, dc) / 2 + 5 });
  }
  // --- futuro
  const Fz = C.futuro;
  if (Fz && t >= Fz.t0 && t <= (Fz.t1 ?? 1e9) + 1) {
    const nasce = Fz.nasce || 2.5, atraso = Fz.atraso ?? .12, some = Fz.t1 !== undefined ? clamp01((Fz.t1 + 1 - t) / 1) : 1;
    (Fz.elementos || []).forEach((e, i) => {
      const k = ease((t - Fz.t0 - i * atraso) / nasce) * some; if (k <= 0) return;
      const id = 'fut-' + (e.id || i), z = zDe(e);
      if (e.tipo === 'parque') {
        L.push(new deck.SolidPolygonLayer({ id, data: [e], getPolygon: d => d.poligono.map(q => [q[0], q[1], z + .06]), getFillColor: [...c255(P.grama), Math.round(235 * k)], material: false, extensions: ext, updateTriggers: { getFillColor: k } }));
        if (e.agua) L.push(new deck.PathLayer({ id: id + '-agua', data: [e], getPath: d => d.agua.map(q => [q[0], q[1], z + .07]), getColor: [...c255(P.agua), Math.round(235 * k)], getWidth: e.agua_larg || 6, widthUnits: 'meters', capRounded: true, jointRounded: true, extensions: ext, updateTriggers: { getColor: k } }));
        if (e.caminho) L.push(new deck.PathLayer({ id: id + '-caminho', data: [e], getPath: d => d.caminho.map(q => [q[0], q[1], z + .09]), getColor: [...c255(P.caminho), Math.round(255 * k)], getWidth: 2.5, widthUnits: 'meters', capRounded: true, jointRounded: true, extensions: ext, updateTriggers: { getColor: k } }));
        if (e.arvores) { e._arv = e._arv || semear(e.poligono, e.arvores, e.semente || 3, 5).map(a => ({ ...a, z: e.z, tipo: a.i % 4 === 0 ? 'palmeira' : 'redonda' })); arvoresCamadas(L, id + '-arv', e._arv, k, EXZ, zDe); }
      } else if (e.tipo === 'ciclovia') {
        L.push(new deck.PathLayer({ id, data: [e], getPath: d => d.caminho.map(q => [q[0], q[1], z + .1]), getColor: [...c255(P.ciclovia), Math.round(255 * k)], getWidth: e.larg || 2.5, widthUnits: 'meters', capRounded: true, jointRounded: true, extensions: ext, updateTriggers: { getColor: k } }));
      } else if (e.tipo === 'vlt') {
        L.push(new deck.PathLayer({ id: id + '-leito', data: [e], getPath: d => d.caminho.map(q => [q[0], q[1], z + .1]), getColor: [...c255(P.leito), Math.round(255 * k)], getWidth: 3.2, widthUnits: 'meters', capRounded: true, jointRounded: true, extensions: ext, updateTriggers: { getColor: k } }));
        e._ao = e._ao || aoLongo(e.caminho);
        const trilhos = []; for (const s of [-.8, .8]) trilhos.push(e.caminho.map((q, j) => { const a = e._ao.em(Math.min(e._ao.L - .01, e._ao.L * j / (e.caminho.length - 1))); const yaw = a.yaw * rad;
          return [q[0] + (-Math.sin(yaw) * s) / mLon(q[1]), q[1] + (Math.cos(yaw) * s) / M_LAT, z + .12]; }));
        L.push(new deck.PathLayer({ id: id + '-trilhos', data: trilhos, getPath: d => d, getColor: [...c255(P.trilho), Math.round(255 * k)], getWidth: .2, widthUnits: 'meters', extensions: ext, updateTriggers: { getColor: k } }));
        if (e.bonde !== false && k > .5) { const s = (t - Fz.t0) * (e.vel || 7), a = e._ao.em(s), u = malhaUnidade('bonde', { comp: e.comp || 24 });
          e._bd = e._bd || [{}];
          L.push(new deck.SimpleMeshLayer({ id: id + '-bonde', data: e._bd, mesh: u, getPosition: [a.p[0], a.p[1], z + .15], getOrientation: [0, a.yaw, 0], getColor: BRANCO, material: MAT, updateTriggers: { getPosition: s, getOrientation: s } }));
          sombras.push({ p: sombraPoli({ lon: a.p[0], lat: a.p[1], rumo: 180 - a.yaw }, e.comp || 24, 2.6, 3, luz).map(q => [q[0], q[1], z + .04]), a: 60 }); }   // rumo = 180 − yaw: mesma rotação da malha
      } else {
        const u = malhaUnidade(e.tipo, { larg: e.larg, comp: e.comp, andares: e.andares, pe: e.pe, solar: e.solar, cor: e.cor });
        e._data = e._data || [e];
        L.push(new deck.SimpleMeshLayer({ id, data: e._data, mesh: u, getPosition: [e.lon, e.lat, z], getOrientation: [0, 180 - (e.rumo ?? 180), 0], getScale: [1, 1, Math.max(.001, k) * ez], getColor: BRANCO, material: e.tipo === 'torre_vidro' ? MAT_VIDRO : MAT, updateTriggers: { getScale: k } }));
        const [dl, dc] = [e.larg || 18, e.comp || 18];
        sombras.push({ p: sombraPoli(e, dl, dc, u.sombra * k * ez, luz).map(q => [q[0], q[1], z + .04]), a: Math.round(92 * k) });
      }
    });
  }
  // --- árvores (lista + auto em polígonos)
  if (C.arvores_auto && !D._marcos.arvAuto) D._marcos.arvAuto = C.arvores_auto.flatMap((a, i) => semear(a.poligono, a.n, a.semente || i + 1, a.dmin || 5).map(p => ({ ...p, z: a.z, ano: a.ano, t0: a.t0, dura: a.dura, tipo: a.tipo || (p.i % 5 === 0 ? 'palmeira' : 'redonda') })));
  const arvs = (C.arvores || []).concat(D._marcos.arvAuto || []);
  if (arvs.length) {
    for (const a of arvs) if (a._t0 === undefined) a._t0 = a.t0 ?? tDoAno(C, a.ano ?? -1e9);
    const vis = arvs.filter(a => t >= a._t0), cresc = vis.some(a => t < a._t0 + (a.dura || 4));
    if (vis.length) { D._marcos.arvVis = D._marcos.arvVis && D._marcos.arvVis.length === vis.length ? D._marcos.arvVis : vis;
      arvoresCamadas(L, 'arvores', D._marcos.arvVis, null, EXZ, zDe, a => ease((t - a._t0) / (a.dura || 4)), cresc ? Math.round(t * 30) : 'fixo'); }
  }
  if (sombras.length) L.push(new deck.SolidPolygonLayer({ id: 'marco-sombras', data: sombras, getPolygon: d => d.p, getFillColor: d => [15, 15, 25, d.a], material: false, extensions: ext, updateTriggers: { getPolygon: t, getFillColor: t } }));
  if (halos.length) {
    L.push(new deck.ScatterplotLayer({ id: 'marco-halo', data: halos, getPosition: d => [d.lon, d.lat, d.z + .1], getRadius: d => d.r, radiusUnits: 'meters', stroked: true, filled: true, getFillColor: [...AMB, 28], getLineColor: [...AMB, 230], getLineWidth: 1.4, lineWidthUnits: 'meters', extensions: [] }));
    L.push(new deck.ScatterplotLayer({ id: 'marco-pulso', data: halos, getPosition: d => [d.lon, d.lat, d.z + .1], getRadius: d => d.r * (1 + .6 * ((t / 1.6) % 1)), radiusUnits: 'meters', stroked: true, filled: false, getLineColor: [...AMB, Math.round(200 * (1 - ((t / 1.6) % 1)))], getLineWidth: .8, lineWidthUnits: 'meters', extensions: [], updateTriggers: { getRadius: t, getLineColor: t } }));
  }
  return L;
}
function arvoresCamadas(L, id, lista, kFixo, EXZ, zDe, kDe, trig) {
  for (const tipo of ['redonda', 'palmeira']) { const d = lista.filter(a => (a.tipo || 'redonda') === tipo); if (!d.length) continue;
    L.push(new deck.SimpleMeshLayer({ id: id + '-' + tipo, data: d, mesh: malhaUnidade('arvore', { arvore: tipo }), getPosition: a => [a.lon, a.lat, zDe(a)],
      getScale: a => { const k = kFixo ?? kDe(a), s = (a.esc || 1) * Math.max(.001, k); return [s, s, s]; }, getOrientation: a => [0, a.giro || 0, 0], getColor: a => a.tinta || BRANCO, material: MAT,
      updateTriggers: { getScale: kFixo ?? trig } })); }
}
// elevação (m) do chão em lon/lat a partir de D.elev (carregaElev)
function elevEm(D, lon, lat) {
  const E = D.elev, [W, S, Ea, N] = E.bbox, x = Math.max(0, Math.min(E.w - 1.001, (lon - W) / (Ea - W) * E.w)), y = Math.max(0, Math.min(E.h - 1.001, (N - lat) / (N - S) * E.h));
  const xi = x | 0, yi = y | 0, fx = x - xi, fy = y - yi, v = (i, j) => { const o = ((yi + j) * E.w + xi + i) * 4; return E.d[o] * 256 + E.d[o + 1] + E.d[o + 2] / 256 - 32768; };
  return v(0, 0) * (1 - fx) * (1 - fy) + v(1, 0) * fx * (1 - fy) + v(0, 1) * (1 - fx) * fy + v(1, 1) * fx * fy;
}
async function carregaElev(D, url, bbox) {
  const im = new Image(); im.src = url; await im.decode(); const c = document.createElement('canvas'); c.width = im.width; c.height = im.height;
  const x = c.getContext('2d'); x.drawImage(im, 0, 0); D.elev = { w: im.width, h: im.height, d: x.getImageData(0, 0, im.width, im.height).data, bbox }; return D.elev;
}
// esconde os prédios do OSM que caem dentro do lote de um marco (ANO = 9999 → nunca nascem). POS: Float32 xyz; INI: índices por prédio
function ocultaOSM(POS, INI, ANO, marcos, folga = 3) {
  let n = 0;
  for (let p = 0; p < ANO.length; p++) { const v = INI[p] * 3, lon = POS[v], lat = POS[v + 1];
    for (const m of marcos) { const [dl, dc] = dimsDe(m), th = -(180 - (m.rumo ?? 180)) * rad, dx = (lon - m.lon) * mLon(m.lat), dy = (lat - m.lat) * M_LAT;
      const x = Math.cos(th) * dx - Math.sin(th) * dy, y = Math.sin(th) * dx + Math.cos(th) * dy;
      if (Math.abs(x) <= dl / 2 + folga && Math.abs(y) <= dc / 2 + folga) { ANO[p] = 9999; n++; break; } } }
  return n;
}

window.MARCOS = { camadas, malha, malhaCache, malhaUnidade, semear, tDoAno, ocultaOSM, carregaElev, elevEm, sombraPoli, aoLongo, fases, Malha, ARQ, PALETA: P, MAT, MAT_VIDRO, LUZ_PADRAO, hex, c255,
  pecas: { vao, frontao, pinaculo, cupula, ameias, plataforma, telhado2, telhado4, corpo, sacada, faixasTelha } };
})();
