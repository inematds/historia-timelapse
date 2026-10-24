| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-10-24 | Mitsuba: pontos pretos (NaN) nos prédios com cor por vértice (`mesh_attribute`) | cor via paleta bitmap 1024x1 + texcoords | infra |
| 2026-10-24 | Mitsuba: imagem só com céu (cidade a 40 km; `far_clip` padrão 10 km) e prédios pretos (material de um lado só) | `far_clip: 1e6` e BSDF `twosided` | infra |
| 2026-10-24 | POA (Mitsuba v1): fim com 4 s de preto e HUD por cima, rótulo do muro tapado, áudio −18 LUFS (revisor nota 6) | `fim` com título + `esconde_hud`, rótulo z=140, `loudnorm -14` no mux | prompt |
| 2026-10-24 | setas/rótulos do Planalto (1.100 m) sumiam do quadro | `z` de rótulo e chamada é em metros crus (o motor multiplica por EXZ); seta fixa na tela (`setas_tela`) para lugar fora do mapa | prompt |
| 2026-10-24 | obelisco de 1922 invisível no topo do morro | mediana do chão enterrava o marco na encosta: `z` = topo; câmera mirando o marco (olhando ao sul, alvo ao sul dele) | prompt |
| 2026-10-22 | capitais: `codex exec` da capa ficou parado em "Reading additional input from stdin" | rodar com `< /dev/null` | infra |
| 2026-10-22 | capitais: `pkill -f "codex exec …"` matou o próprio comando (padrão na linha dele) | não usar pkill com padrão que aparece no próprio comando | prompt |
| 2026-10-22 | capitais: download do Geofabrik a 82 KB/s (horas) | recorte por estado do openstreetmap.fr (bahia 132 MB, DF 62 MB) | infra |
| 2026-10-22 | capitais/Brasília: bairros do OSM no nível 10 são setores, 41 de 42 sem data | regiões administrativas do DF estão no admin_level 8 (`nivel_bairro: "8"`) | infra |
| 2026-10-21 | Florianópolis: terreno sumiu a partir de ~2:45 no render de 6 min (memória do navegador esgotada, "Array buffer allocation failed") | props fixos criados uma vez + render em trechos de 60 s com parada no 1º erro | infra |
| 2026-10-21 | OSM com só 17 mil prédios em Florianópolis (cidade rala) | juntar Microsoft Global ML Building Footprints onde o OSM não tem prédio | infra |
| 2026-10-21 | mar de Florianópolis saiu como terra (OSM guarda costa como linha) | mar = altitude 0 do Copernicus ligada à borda | infra |
