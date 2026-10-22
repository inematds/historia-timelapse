# CONTINUAR — publicar a fase 3 refeita de Itaguaí no lives26

Ordem do Nei (22/10/2026): "refaca a fase3 o avatar so entrando depois do globo e coloque ele na diretia acima do inema.club".
Antes ele disse: "pode publicar direto" e "publcia no lives26".

Já feito (não refazer):
- `cidades/itaguai/final/itaguai-avatar.mp4` refeito (avatar à direita, x1640 y575 220 px; no globo só a voz), −14,3 LUFS, quadros conferidos.
- 540p já foi ao bot v3.
- A versão antiga (X4u-dDnNc64) já foi removida do canal.

Falta:
1. Publicar: `cd ~/projetos/yt-pubx && ./yt-pubx publicar ~/projetos/historia-timelapse/cidades/itaguai/final/itaguai-avatar.mp4 --canal aventuras --plano ~/.local/share/yt-pubx/trabalhos/20261022-063312-itaguai-avatar-mp4/plano.json`
   (em 22/10 19:05 deu `uploadLimitExceeded`; se der de novo, gravar FALHOU e parar.)
2. Mandar o link ao inemaytbot (curl sendMessage; token `TELEGRAM_NOTIFY_BOT_TOKEN` de `~/projetos/yt-pub-livesx-master/config/.env`, chat em `~/.config/aventurasinemavideo/telegram_chat`), texto: "Publicado no lives26 (Aventuras INEMA): Itaguaí em 3D — versão com apresentador (refeita) <url>". Nada ao v3 (já foi).
3. Atualizar o link da fase 3 em `cidades/itaguai/FASES.md` e no README se citar X4u-dDnNc64; commit (autor inematds) + push.
4. Gravar `CONTINUAR.resultado` com "FEITO: <url>" ou "FALHOU: <motivo>".

Travas: não apagar nada no YouTube nem no Telegram; não mexer em outras cidades.
