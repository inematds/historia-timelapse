// marcos-capitais.js — arquétipos novos para "As capitais do Brasil" (Brasília, Rio, Salvador).
// Carregar DEPOIS de marcos.js: só acrescenta tipos em window.MARCOS.ARQ (os tipos antigos não mudam).
// Convenções iguais às de marcos.js: metros locais, frente para −y, `rumo` gira a frente para esse azimute.
(function () {
'use strict';
const { Malha, ARQ, PALETA: P, hex, pecas } = window.MARCOS;
const clamp01 = k => Math.max(0, Math.min(1, k));
const ease = k => { k = clamp01(k); return k * k * (3 - 2 * k); };
const lerp = (a, b, k) => a + (b - a) * k;
const esc = (c, f) => [c[0] * f, c[1] * f, c[2] * f];
const ret = (x0, x1, y0, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
const TAU = Math.PI * 2;

const Q = {
  conc: hex('#EFEDE6'), conc2: hex('#DAD7CE'), concSombra: hex('#BDB9AE'),
  vidro: hex('#2B3944'), vidro2: hex('#3D5363'), vidroVerde: hex('#4A6A66'),
  marmore: hex('#F4F2EC'), agua: hex('#3F7FAE'), aguaClara: hex('#5B97C2'), grama: hex('#6E9E55'),
  vitral: hex('#3E7DB0'), vitral2: hex('#7FB4D6'), bronze: hex('#7A6440'),
};

// superfície de revolução: perfil [[r, z], ...] em torno de (cx, cy); n gomos; normal para fora (ou para o eixo, se dentro)
function revol(M, perfil, cx, cy, n, cor, dentro = false, cor2) {
  for (let j = 0; j < perfil.length - 1; j++) { const [r0, z0] = perfil[j], [r1, z1] = perfil[j + 1];
    for (let i = 0; i < n; i++) { const a0 = i / n * TAU, a1 = (i + 1) / n * TAU;
      const p = (r, z, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a), z];
      const zm = (z0 + z1) / 2, ref = [cx, cy, zm];
      M.quad(p(r0, z0, a0), p(r0, z0, a1), p(r1, z1, a1), p(r1, z1, a0), (cor2 && i % 2) ? cor2 : cor, ref, dentro); } }
}
// disco (tampa) horizontal
function disco(M, cx, cy, r, z, n, cor) { const o = []; for (let i = 0; i < n; i++) { const a = i / n * TAU; o.push([cx + r * Math.cos(a), cy + r * Math.sin(a), z]); } M.poli(o, cor, [cx, cy, z - 1]); }
// placa fina: polígono no plano vertical, extrudado `esp` na direção normal ao plano.
// eixo 'x': o polígono é (y, z) e a placa vai de x−esp/2 a x+esp/2; eixo 'y': polígono (x, z), placa em y.
function placa(M, pol, eixo, c, esp, cor) {
  const n = pol.length, a = [], b = [];
  for (const [u, z] of pol) { if (eixo === 'x') { a.push([c - esp / 2, u, z]); b.push([c + esp / 2, u, z]); } else { a.push([u, c - esp / 2, z]); b.push([u, c + esp / 2, z]); } }
  let mu = 0, mz = 0; for (const [u, z] of pol) { mu += u; mz += z; } mu /= n; mz /= n;
  const ref = eixo === 'x' ? [c, mu, mz] : [mu, c, mz];
  // faces grandes (polígono pode ser côncavo: triangula em leque a partir do centro)
  const cen = eixo === 'x' ? [[c - esp / 2, mu, mz], [c + esp / 2, mu, mz]] : [[mu, c - esp / 2, mz], [mu, c + esp / 2, mz]];
  for (let i = 0; i < n; i++) { const j = (i + 1) % n;
    M.tri(cen[0], a[i], a[j], cor, eixo === 'x' ? [c + 5, mu, mz] : [mu, c + 5, mz]);
    M.tri(cen[1], b[i], b[j], cor, eixo === 'x' ? [c - 5, mu, mz] : [mu, c - 5, mz]);
    M.quad(a[i], a[j], b[j], b[i], esc(cor, .93), ref); }
}
// faixas de janela (vidro + linha de piso) numa face plana de caixa
function fachadaVidro(M, face, x0, x1, y0, y1, z0, z1, pe, corV, corL, mont) {
  const d = .06;
  if (face === 'S' || face === 'N') { const yy = face === 'S' ? y0 - d : y1 + d, s = face === 'S' ? -1 : 1;
    M.caixa(x0 + .3, x1 - .3, Math.min(yy, yy - s * .04), Math.max(yy, yy - s * .04), z0, z1, corV);
    for (let z = z0; z <= z1 + .01; z += pe) M.caixa(x0 + .2, x1 - .2, Math.min(yy, yy + s * .25), Math.max(yy, yy + s * .25), z - .25, z + .1, corL);
    if (mont) for (let x = x0 + mont; x < x1 - .3; x += mont) M.caixa(x - .06, x + .06, Math.min(yy, yy + s * .12), Math.max(yy, yy + s * .12), z0, z1, corL);
  } else { const xx = face === 'W' ? x0 - d : x1 + d, s = face === 'W' ? -1 : 1;
    M.caixa(Math.min(xx, xx - s * .04), Math.max(xx, xx - s * .04), y0 + .3, y1 - .3, z0, z1, corV);
    for (let z = z0; z <= z1 + .01; z += pe) M.caixa(Math.min(xx, xx + s * .25), Math.max(xx, xx + s * .25), y0 + .2, y1 - .2, z - .25, z + .1, corL);
    if (mont) for (let y = y0 + mont; y < y1 - .3; y += mont) M.caixa(Math.min(xx, xx + s * .12), Math.max(xx, xx + s * .12), y - .06, y + .06, z0, z1, corL); }
}
const espelho = (M, x0, x1, y0, y1, z = .15) => { M.caixa(x0, x1, y0, y1, 0, z, { lado: Q.conc2, topo: Q.agua, fundo: Q.conc2 }); };

// ============================================================ BRASÍLIA
// CONGRESSO NACIONAL: laje horizontal (plataforma), rampa na frente, cúpula do Senado (convexa, à esquerda de quem olha a frente)
// e "cuia" da Câmara (côncava, à direita), duas torres gêmeas atrás ligadas por passarela (o "H"), espelhos d'água.
// m: larg (x da laje), comp (y), alt_laje, torre_alt, torre_larg, torre_esp, torre_vao, cupula_r, cupula_h, cuia_r, cuia_rb, cuia_h, lado_camara (+1 direita | −1)
ARQ.congresso = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 160, C = m.comp || 65, h = m.alt_laje || 11, x0 = -L / 2, x1 = L / 2, y0 = -C / 2, y1 = C / 2;
  const cc = Q.conc, sc = Q.conc2, lc = m.lado_camara ?? 1;
  // chão: gramado da frente + espelhos d'água
  if (F.laje > 0) { const k = F.laje;
    espelho(M, x0 - 10, x1 + 10, y1 + 2, y1 + 2 + 70 * k, .12);                  // espelho d'água atrás (em volta das torres)
    M.caixa(x0, x1, y0, y1, 0, .6 * k, { lado: sc, topo: Q.concSombra }); }
  // corpo da laje: térreo de vidro recuado + laje branca grossa por cima (cobertura = praça)
  const hp = h * F.paredes;
  if (hp > .05) {
    const zv = Math.min(hp, h - 2.4);
    if (zv > .05) { M.caixa(x0 + 4, x1 - 4, y0 + 4, y1 - 4, .6, zv, { lado: Q.vidro, topo: Q.vidro });
      for (let x = x0 + 8; x < x1 - 6; x += 8) M.caixa(x - .35, x + .35, y0 + 3.6, y0 + 4.4, .6, zv, cc); }   // pilares atrás do vidro
    if (hp > h - 2.4) M.caixa(x0, x1, y0, y1, h - 2.4, hp, { lado: cc, topo: Q.marmore, fundo: Q.concSombra });
  }
  let alt = hp;
  // rampa da frente: do gramado até a cobertura, no meio
  if (F.paredes > .3) { const k = ease((F.paredes - .3) / .7), rw = m.rampa_larg || 12, rl = m.rampa_comp || 75;
    const za = h * k, yA = y0 - rl, yB = y0;
    M.quad([-rw / 2, yA, .05], [rw / 2, yA, .05], [rw / 2, yB, za], [-rw / 2, yB, za], Q.marmore, [0, yA, -5]);
    for (const s of [-1, 1]) { const xs = s * rw / 2;
      M.quad([xs, yA, .05], [xs, yB, za], [xs, yB, za + .9 * k], [xs, yA, .9 * k], cc, [0, (yA + yB) / 2, za / 2]);
      M.quad([xs, yA, .05], [xs, yB, 0], [xs, yB, za], [xs, yA, .05], cc, [0, (yA + yB) / 2, za / 2]); } }
  // cúpulas: sobem na fase do telhado
  if (F.telhado > 0) { const k = F.telhado, z = h;
    // Senado: cúpula convexa, baixa, assentada num anel
    const rs = m.cupula_r || 19, hs = (m.cupula_h || 10) * k, xs = -lc * (m.cupula_dx || L * .27);
    const perfS = []; for (let i = 0; i <= 10; i++) { const a = i / 10 * Math.PI / 2; perfS.push([rs * Math.cos(a), z + hs * Math.sin(a)]); }
    revol(M, perfS, xs, 0, 40, cc); disco(M, xs, 0, .4, z + hs, 8, cc);
    // Câmara: "cuia" (tigela aberta para cima): pé estreito, borda larga; por dentro um pouco mais escura
    const rb = m.cuia_rb || 11, rt = m.cuia_r || 31, hc = (m.cuia_h || 10) * k, xc = lc * (m.cuia_dx || L * .27);
    const ext = [], int = []; for (let i = 0; i <= 10; i++) { const u = i / 10, r = rb + (rt - rb) * (1 - Math.cos(u * Math.PI / 2)) ** .9;
      ext.push([r, z + hc * Math.sin(u * Math.PI / 2) ** .8]); }
    for (let i = 10; i >= 0; i--) { const [r, zz] = ext[i]; int.push([Math.max(0, r - 1.2), Math.max(z + hc * .35, zz - (i === 10 ? 0 : 1.0))]); }
    revol(M, ext, xc, 0, 48, cc);
    revol(M, int.slice().reverse(), xc, 0, 48, Q.conc2, true);
    disco(M, xc, 0, Math.max(0, rt * .55), z + hc * .35, 32, Q.concSombra);   // fundo da cuia
    alt = Math.max(alt, z + Math.max(hs, hc)); }
  // torres gêmeas (o "H"): atrás da laje; lado maior (45 m) ao longo do Eixo (y); empenas de mármore nas pontas (frente e fundo),
  // vidro nas faces longas; passarela entre elas nos andares do meio
  { const th = m.torre_alt || 100, tw = m.torre_larg || 11.4, te = m.torre_comp || 45, gap = m.torre_vao || 9, ty = y1 + (m.torre_dy || 40);
    const kt = clamp01(F.paredes * 1.25), hz = th * kt;
    if (hz > .3) for (const s of [-1, 1]) { const xa = s > 0 ? gap / 2 : -gap / 2 - tw, xb = xa + tw;
      M.caixa(xa, xb, ty - te / 2, ty + te / 2, 0, hz, { lado: cc, topo: Q.conc2 });
      const zt = Math.min(hz, th - 1.5);
      if (zt > 3) for (const face of ['E', 'W']) fachadaVidro(M, face, xa, xb, ty - te / 2 + .9, ty + te / 2 - .9, 3, zt, 3.5, Q.vidro2, cc); }
    const pz0 = th * (m.passarela_z0 || .40), pz1 = th * (m.passarela_z1 || .47);
    if (hz > pz1) M.caixa(-gap / 2 - .2, gap / 2 + .2, ty - te / 2 + 4, ty + te / 2 - 4, pz0, pz1, { lado: cc, topo: Q.conc2 });
    if (hz > 0) alt = Math.max(alt, hz); }
  return { M, alt, sombra: Math.max(hp, 1) };
};

// PALÁCIO COM COLUNAS (Planalto, Alvorada, STF): caixa de vidro com laje de cobertura saliente, colunas na frente e atrás.
// m.colunas: 'planalto' (aleta curva no plano perpendicular à fachada) | 'alvorada' (arcos invertidos no plano da fachada) | 'stf'
// m: larg, comp, pisos, pe, recuo (m da laje até o vidro), col_n, col_h, rampa (true no Planalto), espelho (true)
ARQ.palacio_colunas = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 140, C = m.comp || 60, pisos = m.pisos || 3, pe = m.pe || 4.2, tipo = m.colunas || 'planalto';
  const x0 = -L / 2, x1 = L / 2, y0 = -C / 2, y1 = C / 2, rec = m.recuo ?? 6, cc = Q.marmore, lajeE = 1.1;
  const H = pisos * pe + (m.base || 1.2);
  if (F.laje > 0) { const k = F.laje;
    if (m.espelho !== false) espelho(M, x0 - 14, x1 + 14, y0 - 30 * k, y0 - 6, .12);
    M.caixa(x0 + rec, x1 - rec, y0 + rec, y1 - rec, 0, (m.base || 1.2) * k, { lado: Q.conc2, topo: Q.conc2 }); }
  const hp = (H - (m.base || 1.2)) * F.paredes + (m.base || 1.2);
  if (F.paredes > .02) {
    M.caixa(x0 + rec, x1 - rec, y0 + rec, y1 - rec, m.base || 1.2, hp, { lado: Q.vidro, topo: Q.vidro });
    for (const face of ['S', 'N']) fachadaVidro(M, face, x0 + rec, x1 - rec, y0 + rec, y1 - rec, m.base || 1.2, hp, pe, Q.vidro2, cc, 5);
    for (let p = 1; p < pisos; p++) { const z = (m.base || 1.2) + p * pe; if (z < hp) M.caixa(x0 + rec - 1.2, x1 - rec + 1.2, y0 + rec - 1.2, y1 - rec + 1.2, z - .45, z, cc); }
  }
  let alt = hp;
  // laje de cobertura saliente (fica branca e fina)
  if (F.telhado > 0 && hp >= H - .01) { const k = F.telhado; M.caixa(x0, x1, y0, y1, H, H + lajeE * k, { lado: cc, topo: Q.conc2, fundo: Q.concSombra }); alt = H + lajeE; }
  // colunas (coroa)
  if (F.coroa > 0) { const k = F.coroa, n = m.col_n || Math.round(L / 12), Hc = H + lajeE;
    for (const [yy, s] of [[y0, -1], [y1, 1]]) {
      if (tipo === 'alvorada') {
        // arcos invertidos no plano da fachada: cada coluna é larga em cima e afina até tocar o chão num ponto
        const passo = L / n;
        for (let i = 0; i < n; i++) { const xa = x0 + i * passo, xb = xa + passo, xm = (xa + xb) / 2, w = passo * .5, pol = [];
          pol.push([xa + passo * .06, Hc]);
          for (let j = 1; j <= 8; j++) { const u = j / 8; pol.push([lerp(xa + passo * .06, xm - .25, u ** .55), Hc - (Hc - .6) * u ** 1.7]); }
          pol.push([xm, 0]);
          for (let j = 8; j >= 1; j--) { const u = j / 8; pol.push([lerp(xb - passo * .06, xm + .25, u ** .55), Hc - (Hc - .6) * u ** 1.7]); }
          pol.push([xb - passo * .06, Hc]);
          const zk = pol.map(([x, z]) => [x, Hc - (Hc - z) * k]);
          placa(M, zk, 'y', yy + s * .2, .8, cc); void w; } }
      else {
        // Planalto/STF: aleta fina no plano perpendicular à fachada; toca o chão num ponto e "abre" para fora no meio
        const ab = m.col_abre || (tipo === 'stf' ? 3.6 : 6);
        for (let i = 0; i <= n; i++) { const x = x0 + 2 + i * (L - 4) / n, pol = [], N2 = 10;
          for (let j = 0; j <= N2; j++) { const u = j / N2, z = Hc * u; pol.push([yy + s * (ab * Math.sin(Math.PI * u) ** .8 + .3), Hc - (Hc - z) * k]); }
          for (let j = N2; j >= 0; j--) { const u = j / N2, z = Hc * u; pol.push([yy + s * (ab * .45 * Math.sin(Math.PI * u) ** .8 * (1 - u * .3)), Hc - (Hc - z) * k]); }
          placa(M, pol, 'x', x, m.col_esp || 1.0, cc); } }
    }
    // rampa do Planalto (parlatório): rampa da frente até o 2º piso
    if (m.rampa) { const rw = 8, za = (m.base || 1.2) + pe, ya = y0 - 40;
      M.quad([-rw / 2 - 18, ya, .1], [rw / 2 - 18, ya, .1], [rw / 2 - 18, y0 + rec - .5, za * k], [-rw / 2 - 18, y0 + rec - .5, za * k], cc, [-18, ya, -5]);
      for (const s2 of [-1, 1]) M.quad([s2 * rw / 2 - 18, ya, .1], [s2 * rw / 2 - 18, y0 + rec - .5, za * k], [s2 * rw / 2 - 18, y0 + rec - .5, za * k + 1], [s2 * rw / 2 - 18, ya, 1], cc, [-18, (ya + y0) / 2, za / 2]); }
  }
  return { M, alt, sombra: hp };
};

// CATEDRAL DE BRASÍLIA: 16 colunas de concreto em hiperboloide (pé largo, cintura, coroa aberta), vitral entre elas,
// espelho d'água em volta, campanário ao lado. m: raio (base), alt, n (colunas), campanario (true)
ARQ.catedral_bsb = (m, F, cor) => {
  const M = new Malha(), R = m.raio || 30, Hh = m.alt || 42, n = m.n || 16, cc = Q.marmore;
  // perfil do eixo da coluna: r(u), z(u)
  const cint = m.cintura || .14, topo = m.topo || .36, zc = m.z_cintura || .76;
  const rEm = u => u < zc ? lerp(R, R * cint, Math.sin(u / zc * Math.PI / 2) ** 1.25) : lerp(R * cint, R * topo, ((u - zc) / (1 - zc)) ** 1.6);
  const wEm = u => .9 + 2.4 * Math.sin(Math.min(1, u / .8) * Math.PI) ** .8 + (u > .85 ? (1 - u) * 4 : 0);   // largura radial (bumerangue)
  if (F.laje > 0 && !m.so_vitral) { const k = F.laje;
    revol(M, [[R + 22, .12], [R + 22, 0]], 0, 0, 48, Q.agua); disco(M, 0, 0, R + 22, .12, 48, Q.agua);  // espelho d'água
    disco(M, 0, 0, R + 1.5, .5 * k + .13, 48, Q.conc2); revol(M, [[R + 1.5, .13], [R + 1.5, .5 * k + .13]], 0, 0, 48, Q.conc2); }
  const kc = m.so_vitral ? 1 : F.paredes;
  if (kc > .02) {
    const N = 14, uMax = kc;
    if (!m.so_vitral)
    for (let i = 0; i < n; i++) { const a = i / n * TAU, ca = Math.cos(a), sa = Math.sin(a), tx = -sa, ty = ca, esp = 1.3;
      // polígono (r, z) da coluna: borda externa e interna em volta do eixo
      const ext = [], int = [];
      for (let j = 0; j <= N; j++) { const u = j / N * uMax, r = rEm(u), w = wEm(u); ext.push([r + w * .55, u * Hh]); int.push([r - w * .45, u * Hh]); }
      const pol = ext.concat(int.reverse());
      const P3 = (r, z, d) => [r * ca + tx * d, r * sa + ty * d, z];
      let mr = 0, mz = 0; for (const [r, z] of pol) { mr += r; mz += z; } mr /= pol.length; mz /= pol.length;
      const ref = P3(mr, mz, 0);
      for (let j = 0; j < pol.length; j++) { const p0 = pol[j], p1 = pol[(j + 1) % pol.length];
        M.quad(P3(p0[0], p0[1], -esp / 2), P3(p1[0], p1[1], -esp / 2), P3(p1[0], p1[1], esp / 2), P3(p0[0], p0[1], esp / 2), cc, ref); }
      const c0 = P3(mr, mz, -esp / 2), c1 = P3(mr, mz, esp / 2);
      for (let j = 0; j < pol.length; j++) { const p0 = pol[j], p1 = pol[(j + 1) % pol.length];
        M.tri(c0, P3(p0[0], p0[1], -esp / 2), P3(p1[0], p1[1], -esp / 2), cc, P3(mr, mz, 5));
        M.tri(c1, P3(p0[0], p0[1], esp / 2), P3(p1[0], p1[1], esp / 2), cc, P3(mr, mz, -5)); } }
    // vitral entre as colunas (superfície no eixo, um pouco para dentro), sobe junto
    if (m.vitral !== false && (m.so_vitral ? F.paredes > 0 : F.telhado > 0)) { const kv = m.so_vitral ? F.paredes : F.telhado, perf = []; for (let j = 0; j <= 12; j++) { const u = .03 + j / 12 * .9 * kv; perf.push([rEm(u) - .3, u * Hh]); }
      revol(M, perf, 0, 0, n * 2, Q.vitral, false, Q.vitral2); }
  }
  // campanário: 4 hastes finas de ~20 m + sinos
  if (m.campanario !== false && !m.so_vitral && F.coroa > 0) { const k = F.coroa, bx = R + 14, by = -R * .6, hc = 20 * k;
    for (const [dx, dy] of [[-1.2, -1.2], [1.2, -1.2], [1.2, 1.2], [-1.2, 1.2]]) M.caixa(bx + dx - .25, bx + dx + .25, by + dy - .25, by + dy + .25, 0, hc, cc);
    M.caixa(bx - 1.6, bx + 1.6, by - 1.6, by + 1.6, hc - .5, hc, cc);
    for (let i = 0; i < 4; i++) disco(M, bx, by, .8, hc * (.45 + i * .12), 10, Q.bronze); }
  return { M, alt: Hh * kc, sombra: 0 };
};

// BLOCO DE MINISTÉRIO (Esplanada): lâmina comprida de vidro, empenas cegas nas pontas, pilotis.
ARQ.ministerio = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 102, C = m.comp || 17, pisos = m.pisos || 10, pe = m.pe || 3.5, pil = m.pilotis ?? 3.5;
  const x0 = -L / 2, x1 = L / 2, y0 = -C / 2, y1 = C / 2, cc = Q.conc, H = pil + pisos * pe;
  if (F.laje > 0) { const k = F.laje; for (let x = x0 + 4; x < x1 - 2; x += 8) for (const y of [y0 + 3, y1 - 3]) M.caixa(x - .5, x + .5, y - .5, y + .5, 0, pil * k, Q.conc2); }
  const hp = (H - pil) * F.paredes + pil;
  if (F.paredes > .02) {
    M.caixa(x0 + 1, x1 - 1, y0, y1, pil, hp, { lado: Q.vidroVerde, topo: Q.conc2, fundo: Q.concSombra });
    for (const face of ['S', 'N']) fachadaVidro(M, face, x0 + 1, x1 - 1, y0, y1, pil, hp, pe, Q.vidroVerde, Q.conc2, 3);
    M.caixa(x0, x0 + 1.2, y0 - .2, y1 + .2, pil, hp, cc); M.caixa(x1 - 1.2, x1, y0 - .2, y1 + .2, pil, hp, cc);   // empenas
  }
  let alt = hp;
  if (F.telhado > 0 && hp >= H - .01) { M.caixa(x0, x1, y0 - .2, y1 + .2, H, H + .8 * F.telhado, cc); alt = H + .8; }
  return { M, alt, sombra: hp };
};

// TEATRO NACIONAL: pirâmide truncada (tronco) com faces inclinadas
ARQ.teatro_piramide = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 100, C = m.comp || 70, H = (m.alt || 40) * F.paredes, bt = m.topo || .25;
  if (H < .2) return { M, alt: 0, sombra: 0 };
  const k = F.paredes, lt = L * lerp(1, bt, k), ct = C * lerp(1, .55, k);
  const b = [[-L / 2, -C / 2], [L / 2, -C / 2], [L / 2, C / 2], [-L / 2, C / 2]], t = [[-lt / 2, -ct / 2], [lt / 2, -ct / 2], [lt / 2, ct / 2], [-lt / 2, ct / 2]];
  for (let i = 0; i < 4; i++) { const j = (i + 1) % 4; M.quad([...b[i], 0], [...b[j], 0], [...t[j], H], [...t[i], H], i % 2 ? Q.conc2 : Q.conc, [0, 0, H / 2]); }
  M.poli(t.map(p => [...p, H]), Q.conc2, [0, 0, 0]);
  return { M, alt: H, sombra: H };
};


// ITAMARATY (Palácio dos Arcos): caixa de vidro recuada sob laje, cercada de arcos plenos esbeltos (15 pilares por face), espelho d'água
ARQ.itamaraty = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 84, H = m.alt || 17.6, n = m.arcos || 14, x0 = -L / 2, x1 = L / 2, cc = Q.marmore, rec = 6;
  if (F.laje > 0) espelho(M, x0 - 16 * F.laje, x1 + 16 * F.laje, x0 - 16 * F.laje, x1 + 16 * F.laje, .12);
  const hp = H * F.paredes; if (hp < .2) return { M, alt: 0, sombra: 0 };
  M.caixa(x0 + rec, x1 - rec, x0 + rec, x1 - rec, 0, Math.min(hp, H - 1.5), { lado: Q.vidro, topo: Q.vidro });
  for (let p = 1; p < 4; p++) { const z = p * (H - 1.5) / 4; if (z < hp) M.caixa(x0 + rec - .4, x1 - rec + .4, x0 + rec - .4, x1 - rec + .4, z - .4, z, cc); }
  const passo = L / n, w = 1.1, r = passo / 2 - w / 2;
  for (const face of ['S', 'N', 'E', 'W']) for (let i = 0; i < n; i++) {
    const u0 = x0 + i * passo, uc = u0 + passo / 2, zA = H - 1.2 - r, pol = [];   // vão do arco: pilar esq + arco + pilar dir (polígono em U invertido, cheio por fora)
    pol.push([u0, 0], [u0 + w / 2, 0], [u0 + w / 2, zA]);
    for (let j = 1; j < 12; j++) { const a = Math.PI - j / 12 * Math.PI; pol.push([uc + r * Math.cos(a), zA + r * Math.sin(a)]); }
    pol.push([u0 + passo - w / 2, zA], [u0 + passo - w / 2, 0], [u0 + passo, 0], [u0 + passo, H], [u0, H]);
    const pk = pol.map(([u, z]) => [u, Math.min(z, hp)]);
    if (face === 'S' || face === 'N') placa(M, pk, 'y', face === 'S' ? x0 : x1, .9, cc);
    else placa(M, pk, 'x', face === 'W' ? x0 : x1, .9, cc); }
  if (F.telhado > 0 && hp >= H - .01) M.caixa(x0, x1, x0, x1, H - 1.2, H, { lado: cc, topo: Q.conc2 });
  return { M, alt: hp, sombra: 0 };
};

// TORRE DE TV: base triangular de concreto sobre 3 pilares + torre metálica treliçada que afina, mirante a 75 m
ARQ.torre_tv = (m, F, cor) => {
  const M = new Malha(), H = (m.alt || 224) * F.paredes, cc = Q.conc2, aco = hex('#8E979E');
  if (H < .5) return { M, alt: 0, sombra: 0 };
  const tri = (r, z) => [0, 1, 2].map(i => { const a = Math.PI / 2 + i * TAU / 3; return [r * Math.cos(a), r * Math.sin(a), z]; });
  const b0 = tri(22, 0), b1 = tri(22, Math.min(H, 25));
  for (let i = 0; i < 3; i++) M.barra([b0[i][0] * .4, b0[i][1] * .4, 0], b1[i], 3.2, 3.2, cc);
  if (H > 18) { const zb = 18, zt = Math.min(H, 25); M.prisma(tri(24, 0).map(p => [p[0], p[1]]), zb, zt, Q.vidro2, cc, cc); }
  const ztop = Math.max(25, H);
  if (H > 25) { let prev = tri(12, 25);
    for (let z = 25 + 12; z <= ztop + .01; z += 12) { const r = lerp(12, 2.5, (z - 25) / (224 - 25)), cur = tri(r, Math.min(z, ztop));
      for (let i = 0; i < 3; i++) { M.barra(prev[i], cur[i], 2.2, 2.2, aco); M.barra(prev[i], cur[(i + 1) % 3], .9, .9, aco); M.barra(cur[i], cur[(i + 1) % 3], 1.0, 1.0, aco); }
      prev = cur; if (z >= ztop) break; }
    if (H > 75) M.prisma([[-13, -9], [13, -9], [13, 9], [-13, 9]], 71, 79, Q.vidro2, cc, cc); }
  return { M, alt: H, sombra: 0 };
};

// CATETINHO: casa comprida de tábuas sobre pilotis (térreo aberto), telhado de uma água
ARQ.catetinho = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 34, C = m.comp || 10, mad = hex('#9C6B43'), mad2 = hex('#7A5133'), x0 = -L / 2, x1 = L / 2, y0 = -C / 2, y1 = C / 2;
  if (F.laje > 0) for (let x = x0 + 1; x <= x1 - 1; x += 4) for (const y of [y0 + .5, y1 - .5]) M.caixa(x - .2, x + .2, y - .2, y + .2, 0, 2.8 * F.laje, mad2);
  const hp = 2.8 + 3.2 * F.paredes; if (F.paredes > .02) { M.caixa(x0, x1, y0, y1, 2.8, hp, { lado: mad, topo: mad2 });
    for (let x = x0 + 1.5; x < x1 - 1; x += 2.6) if (hp > 4.6) M.caixa(x - .55, x + .55, y0 - .06, y0, 3.8, 5.2, P.vidro); }
  if (F.telhado > 0) M.quad([x0 - .6, y0 - 1, 6.2], [x1 + .6, y0 - 1, 6.2], [x1 + .6, y1 + .6, 6.2 + 1.4 * F.telhado], [x0 - .6, y1 + .6, 6.2 + 1.4 * F.telhado], P.zinco, [0, 0, 0]);
  return { M, alt: 7.6, sombra: hp };
};

// ============================================================ RIO e SALVADOR
// PALÁCIO ECLÉTICO: corpo de 2–3 pavimentos com platibanda, pórtico de colunas e cúpula opcional (Tiradentes, Rio Branco, Catete, Theatro, Monroe)
// m: larg, comp, andares, pe, parede, cor (moldura), cupula: {r, h, cor:'verde'|'prata'|'cobre', tambor}, portico: {n, larg}, torres_canto
ARQ.palacio = (m, F, cor) => {
  const M = new Malha(), L = m.larg || 60, C = m.comp || 40, an = m.andares || 3, pe = m.pe || 5, H = an * pe, plat = m.platibanda ?? 1.6;
  const dest = cor.moldura === P.amb;   // destaque: o prédio mantém as cores; só uma faixa amarela no alto (o halo e a chamada fazem o resto)
  const x0 = -L / 2, x1 = L / 2, y0 = -C / 2, y1 = C / 2, cp = cor.parede || P.claro;
  const cm = dest ? (m.cor ? hex(m.cor) : P.branco) : (cor.moldura || P.branco);
  const { corpo, vao, sacada } = pecas;
  if (F.laje > 0) { M.caixa(x0 - .5, x1 + .5, y0 - .5, y1 + .5, 0, .6 * F.laje, P.pedra);
    if (m.escadaria !== false) for (let i = 0; i < 6; i++) M.caixa(-L * .18 + i * .2, L * .18 - i * .2, y0 - 5 + i * .8, y0 + .1, 0, (.2 + .2 * i) * F.laje, P.pedra); }
  const hp = H * F.paredes; if (hp <= .05) return { M, alt: .6, sombra: 0 };
  corpo(M, x0, x1, y0, y1, 0, hp, { parede: cp, moldura: cm, soco: 1.2, cunhal: .9, cornija: 0, corSoco: P.soco });
  for (let a = 1; a < an; a++) if (a * pe + .1 <= hp) M.caixa(x0 - .2, x1 + .2, y0 - .2, y1 + .2, a * pe - .35, a * pe, cm);
  // avanço central (corpo saliente) na frente
  const av = m.avanco ?? Math.min(L * .3, 24);
  if (av > 0) M.caixa(-av / 2, av / 2, y0 - 2.2, y0, 0, hp, { lado: cp, topo: esc(cp, .9) });
  const yF = av > 0 ? y0 - 2.2 : y0;
  // janelas em todas as faces (passo ~3,4 m), em arco no térreo
  for (const face of ['S', 'N', 'E', 'W']) { const Lf = (face === 'S' || face === 'N') ? L : C, c0 = (face === 'S' || face === 'N') ? x0 : y0;
    const nJ = Math.max(2, Math.floor((Lf - 3) / 3.4)), u0 = c0 + (Lf - (nJ - 1) * 3.4) / 2;
    for (let i = 0; i < nJ; i++) { const u = u0 + i * 3.4; if (face === 'S' && Math.abs(u) < av / 2 + 1) continue;
      for (let a = 0; a < an; a++) { const v0 = a * pe + (a ? 1.0 : 1.2), h = Math.min(pe - 1.7, a ? 2.9 : 2.8); if (v0 + h + .2 <= hp)
        vao(M, face, x0, x1, y0, y1, u, v0, 1.4, h, { moldura: cm, folha: P.vidro, forma: a === 0 ? 'arco' : 'reta', peitoril: true }); } } }
  // janelas do avanço
  if (av > 0) for (let i = -1; i <= 1; i++) for (let a = 0; a < an; a++) { const v0 = a * pe + 1.1, h = Math.min(pe - 1.6, 3.2);
    if (v0 + h + .2 <= hp) { vao(M, 'S', -av / 2, av / 2, y0 - 2.2, y0, i * av / 3.2, v0, 1.8, h, { moldura: cm, folha: a === 0 && i === 0 ? P.madeira : P.vidro, forma: 'arco' });
      if (a > 0 && i === 0) sacada(M, 'S', -av / 2, av / 2, y0 - 2.2, y0, 0, v0, 1.8, cm); } }
  // pórtico de colunas na frente do avanço
  if (m.portico && F.paredes > .4) { const n = m.portico.n || 6, pl = m.portico.larg || av, hc = Math.min(hp, (m.portico.alt || 2 * pe)), yp = yF - 3.2;
    for (let i = 0; i < n; i++) { const x = -pl / 2 + .8 + i * (pl - 1.6) / (n - 1); M.prisma(poliRegL(x, yp, .65, 10), 0, hc, P.branco, P.branco, null);
      M.caixa(x - .8, x + .8, yp - .8, yp + .8, hc - .5, hc, cm); }
    M.caixa(-pl / 2, pl / 2, yp - 1, yF, hc, hc + 1.2, { lado: cm, topo: esc(cp, .9) });
    if (m.portico.frontao !== false) { const zt = hc + 1.2; M.tri([-pl / 2, yp - 1, zt], [pl / 2, yp - 1, zt], [0, yp - 1, zt + pl * .16], cm, [0, yF + 5, zt]);
      M.tri([-pl / 2, yF, zt], [pl / 2, yF, zt], [0, yF, zt + pl * .16], cm, [0, yp - 6, zt]);
      M.quad([-pl / 2, yp - 1, zt], [0, yp - 1, zt + pl * .16], [0, yF, zt + pl * .16], [-pl / 2, yF, zt], P.telha, [0, (yp + yF) / 2, zt - 3]);
      M.quad([pl / 2, yp - 1, zt], [0, yp - 1, zt + pl * .16], [0, yF, zt + pl * .16], [pl / 2, yF, zt], P.telha, [0, (yp + yF) / 2, zt - 3]); } }
  let alt = hp;
  if (F.telhado > 0) { const k = F.telhado, e = .2;
    M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, H, H + .5, cm);
    M.caixa(x0, x1, y0, y1, H + .5, H + .5 + plat * k, { lado: cp, topo: cm, fundo: cp });
    M.caixa(x0 - e, x1 + e, y0 - e, y1 + e, H + .5 + plat * k - .3, H + .5 + plat * k, cm);
    if (m.telhado_visivel) { const r = pecas.telhado4(M, x0 + .6, x1 - .6, y0 + .6, y1 - .6, H + .5, 24, 0, { telha: P.telha, telha2: P.telha2, testeira: P.testeira, sofito: P.sofito, cumeeira: P.cumeeira }, (1 - k) * 4); alt = H + .5 + r.alt; }
    else { M.caixa(x0 + .4, x1 - .4, y0 + .4, y1 - .4, H, H + .3, P.ardosia); alt = H + .5 + plat; }
    if (av > 0) { M.caixa(-av / 2, av / 2, y0 - 2.4, y0, H + .5 + plat * k, H + .5 + plat * k + 1.8 * k, { lado: cp, topo: cm }); } }
  if (dest && F.telhado > 0) M.caixa(x0 - .35, x1 + .35, y0 - .35, y1 + .35, H + .1, H + .75, P.amb);
  // coroa: cúpula central, pináculos/estátuas nos cantos, torreões de canto
  if (F.coroa > 0) { const k = F.coroa, zt = H + .5 + plat;
    if (m.cupula) { const cu = m.cupula, r = cu.r || 8, hb = (cu.tambor ?? 4) * k, hc = (cu.h || r) * k, cx = cu.dx || 0, cy = cu.dy ?? 0;
      const c1 = cu.cor === 'verde' ? hex('#5E8F7A') : cu.cor === 'cobre' ? hex('#4F8A78') : cu.cor === 'bronze' ? hex('#6F5A3A') : cu.cor === 'dourado' ? hex('#C9A227') : cu.cor === 'cinza' ? hex('#8C8F8C') : P.prata, c2 = cu.cor2 ? hex(cu.cor2) : esc(c1, .86);
      M.prisma(poliRegL(cx, cy, r * 1.04, 20), zt, zt + hb, cp, cm, null);
      for (let i = 0; i < 10; i++) { const a = i / 10 * TAU; M.caixa(cx + r * 1.05 * Math.cos(a) - .4, cx + r * 1.05 * Math.cos(a) + .4, cy + r * 1.05 * Math.sin(a) - .4, cy + r * 1.05 * Math.sin(a) + .4, zt, zt + hb, cm); }
      pecas.cupula(M, cx, cy, zt + hb, r, hc, c1, c2);
      M.prisma(poliRegL(cx, cy, r * .18, 8), zt + hb + hc * .97, zt + hb + hc + 2.5 * k, cm, cm, null);
      if (cu.estatua) { M.prisma(poliRegL(cx, cy, .5, 8), zt + hb + hc + 2.5 * k, zt + hb + hc + 6 * k, Q.bronze, Q.bronze, null); }
      alt = Math.max(alt, zt + hb + hc + 3); }
    if (m.torres_canto) for (const [x, y] of [[x0, y0], [x1, y0]]) { const tw = m.torres_canto.larg || 7, th = (m.torres_canto.alt || 6) * k, cx = x === x0 ? x0 + tw / 2 : x1 - tw / 2;
      M.caixa(cx - tw / 2, cx + tw / 2, y0, y0 + tw, zt - plat, zt + th, { lado: cp, topo: cm });
      M.piramide(ret(cx - tw / 2, cx + tw / 2, y0, y0 + tw), zt + th, [cx, y0 + tw / 2, zt + th + tw * .5 * k], P.ardosia); }
    if (m.estatuas_canto) for (const [x, y] of [[x0 + 1, y0 + 1], [x1 - 1, y0 + 1]]) { M.caixa(x - .9, x + .9, y - .9, y + .9, zt, zt + 1.2 * k, cm); M.prisma(poliRegL(x, y, .55, 8), zt + 1.2 * k, zt + 4 * k, Q.bronze, Q.bronze, null); }
  }
  return { M, alt, sombra: hp };
};
const poliRegL = (cx, cy, r, n) => { const o = []; for (let i = 0; i < n; i++) { const a = i / n * TAU; o.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return o; };

// FORTE REDONDO (São Marcelo): cilindro de pedra com parapeito e canhoneiras, torre central
ARQ.forte_redondo = (m, F, cor) => {
  const M = new Malha(), R = m.raio || 23, H = (m.alt || 9) * F.paredes, NL = m.lados || 40;
  const pedra = m.parede ? hex(m.parede) : hex('#A39A88'), pedra2 = esc(pedra, .86);
  if (H < .1) return { M, alt: 0, sombra: 0 };
  revol(M, [[R + 1.2, 0], [R, H]], 0, 0, NL, pedra); disco(M, 0, 0, R, H, NL, pedra2);
  if (F.telhado > 0) { const k = F.telhado; revol(M, [[R, H], [R, H + 1.4 * k]], 0, 0, NL, pedra, false, pedra2);
    for (let i = 0; i < 16; i++) { const a = (i + .5) / 16 * TAU; M.caixa(R * Math.cos(a) - .6, R * Math.cos(a) + .6, R * Math.sin(a) - .6, R * Math.sin(a) + .6, H + 1.4 * k, H + 1.4 * k + .01, P.vidro); } }
  if (F.coroa > 0 && m.torreao !== false) { const k = F.coroa, r2 = R * (m.torreao_r || .42); revol(M, [[r2, H], [r2, H + 6 * k]], 0, 0, 28, pedra); disco(M, 0, 0, r2, H + 6 * k, 28, pedra2);
    revol(M, [[r2, H + 6 * k], [r2, H + 7 * k]], 0, 0, 28, pedra2); }
  return { M, alt: H + 7, sombra: 0 };
};


// FAROL: torre troncônica com faixas, galeria e lanterna envidraçada (Farol da Barra)
ARQ.farol = (m, F, cor) => {
  const M = new Malha(), H = (m.alt || 22) * F.paredes, r0 = m.raio || 3.4, b1 = hex('#F2F0EA'), b2 = hex('#2A2A2E');
  if (H < .2) return { M, alt: 0, sombra: 0 };
  const nf = m.faixas || 0, perf = [];
  for (let i = 0; i <= 8; i++) { const z = H * i / 8; perf.push([lerp(r0, r0 * .72, i / 8), z]); }
  for (let i = 0; i < 8; i++) revol(M, [perf[i], perf[i + 1]], 0, 0, 16, nf && (i % 2) ? b2 : b1);
  if (F.coroa > 0 && H >= (m.alt || 22) - .01) { const k = F.coroa, rt = r0 * .72;
    disco(M, 0, 0, rt + .9, H + .3, 16, b2); revol(M, [[rt + .9, H], [rt + .9, H + .3]], 0, 0, 16, b2);
    revol(M, [[rt * .8, H + .3], [rt * .8, H + .3 + 2.6 * k]], 0, 0, 12, Q.vidro2);
    revol(M, [[rt * .85, H + .3 + 2.6 * k], [0.2, H + .3 + 3.8 * k]], 0, 0, 12, b2); }
  return { M, alt: H + 4, sombra: 0 };
};

// ELEVADOR (Lacerda): torre alta e estreita encostada na escarpa + passarela até o alto; art déco (faixas verticais)
ARQ.elevador = (m, F, cor) => {
  const M = new Malha(), w = m.larg || 12, d = m.comp || 10, H = (m.alt || 72) * F.paredes, cc = hex('#E9E2CF'), lin = hex('#C9BFA6');
  if (H < .2) return { M, alt: 0, sombra: 0 };
  M.caixa(-w / 2, w / 2, -d / 2, d / 2, 0, H, { lado: cc, topo: lin });
  for (let x = -w / 2 + 1.5; x < w / 2 - 1; x += 2.2) M.caixa(x - .25, x + .25, -d / 2 - .3, -d / 2, 1, H - 1, lin);
  if (F.telhado > 0 && H >= (m.alt || 72) - .1) { const k = F.telhado, pl = (m.passarela || 30) * k, z = m.alt || 72;
    M.caixa(-w / 2 - 1, w / 2 + 1, -d / 2 - 1, d / 2 + 1, z, z + 6 * k, { lado: cc, topo: lin });
    M.caixa(-3, 3, d / 2, d / 2 + pl, z - 4, z, { lado: cc, topo: lin }); }
  return { M, alt: H + 6, sombra: H };
};

window.MARCOS.CAPITAIS = { revol, placa, Q };
})();
