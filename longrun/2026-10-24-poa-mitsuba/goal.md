# Goal — Porto Alegre com Mitsuba (24/10/2026)

Pedido do Nei: "vamos fazer portoalegre novamente com ele [Mitsuba], e tentar melhorar detalhes. me avise no v3 e publique nos aventura como prioridade".
OK de publicação: dado explicitamente nesta mensagem (lives26 / Aventuras).

## Abordagem
Render híbrido: Mitsuba (GPU) desenha relevo + prédios (luz, sombra, prédios subindo); o motor atual (deck.gl) desenha o resto como camada transparente (HUD, cartões, globo, efeitos), com relevo/prédios só na profundidade. Compositor: céu → Mitsuba → camada. Modo atrás de flag: render padrão do deck fica idêntico.

## Pronto quando (nível 3+)
1. Alinhamento: `python scripts/mitsuba_quadro.py poa t=<x>` + mistura 50/50 com o quadro deck → contorno dos prédios coincide (diferença de borda ≤ 2 px, conferido em imagem).
2. Regressão: 3 quadros de Floripa no modo padrão antes/depois da mudança no mapa.html → diferença 0 (`compare`/numpy).
3. Vídeo: `cidades/poa/final/poa-mitsuba.mp4` com duração = duração da cena (±0,1 s), 1920x1080 30 fps, áudio do POA, sem quadro preto/vazio (checagem de quadros com média de luz).
4. Avisos v3: quadros-chave enviados antes do render completo; mensagem final com link.
5. Publicado no lives26 (ou erro do YouTube relatado sem insistir).
