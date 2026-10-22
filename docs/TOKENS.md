# Tokens gastos por vídeo (Claude Code, pela assinatura)

Medido nos logs das sessões (`~/.claude/projects/*/*.jsonl`), somando os subagentes (pesquisa, Fable, revisores).
Total = entrada + cache escrito + cache lido + saída. Quase tudo é **cache lido**: o histórico relido a cada passo, que custa bem menos. O que pesa de verdade é a **saída**, o texto escrito pelo modelo.

| Vídeo | Sessão | Chamadas | Saída | Cache escrito | Cache lido | Total | Medido em |
|---|---|---|---|---|---|---|---|
| Itaguaí — Centro (3 fases, 3 renders, 3 revisões) | historia-timelapse `964222a7` | ~390 | 431.886 | 1,95 M | 96,2 M | **≈ 98,5 M** | 22/10/2026 |
| Porto Alegre (piloto + motor) | wifi `6778e3c7`, 21/10 21:29–23:33 | 300 | 178.125 | 1,14 M | 65,3 M | **≈ 66,7 M** | 22/10/2026 |
| Florianópolis, parte 1 | wifi `6778e3c7`, 21/10 23:33 → 22/10 09:11 | 511 | 321.064 | 1,80 M | 165,1 M | **≈ 167,2 M** | 22/10/2026 |
| Florianópolis fases 2/3 + Itaguaí município | historia-timelapse `6e4b887b`, 22/10 05:46–09:38 | 309 | 234.052 | 0,79 M | 62,6 M | **≈ 63,6 M** | 22/10/2026 |

## Ressalvas
- Porto Alegre e Florianópolis estavam na mesma sessão do projeto wifi. A divisão foi feita pela hora da 1ª menção a Florianópolis (21/10 23:33).
- A sessão `6e4b887b` mistura Florianópolis (fases 2 e 3) com o Itaguaí município.
- Sessões anteriores a 21/10 21:29, se houve, não entram.
- Como medir de novo: `~/projetos/execucao-longa/tools/medir-sessao.py <jsonl>`, ou somar `usage` das mensagens `assistant` sem repetir `message.id`.
