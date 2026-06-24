# ADR-009 — Launcher Soberano

- **Status:** ✅ Aceito (ratificado no GATE-0, Ata do Conselho 2026-06-22)
- **Origem:** GATE-0-DECL-V6 · TASK-0012
- **Supersede:** ADR-002 (Launcher Legacy)
- **Resolve:** BUG-004 (FND-08, env vars de teste sem gating / injeção massiva de flags) — vetor de launcher

## Contexto
O V5.5 tinha **múltiplos launchers** (`run_omega_24x7.ps1`, `omega_paper_loop_24x7.py`,
`launch_24h_clean.py`) com **injeção massiva de flags de ambiente**, permitindo que flags de
teste/dev vazassem para execução (BUG-004/FND-08). O padrão de variantes (`*_final_fix*`) também
contribuiu para a contaminação.

## Decisão
Existe **um único launcher soberano**: `deployment/omega_run.py`.

- **Fail-closed:** exige `OMEGA_ENV` **explícito** (ex.: `python deployment/omega_run.py --env demo`).
  Sem ambiente declarado, **recusa iniciar**.
- **Proibições:** múltiplos launchers, scripts `*_24x7.ps1`, variantes `*_final_fix*`, e injeção
  massiva de flags fora do mecanismo de configuração auditado (ADR-011).

## Consequências
- **(+)** Ponto de entrada único e auditável; impossível "ligar o sistema pelo caminho errado".
- **(+)** O nome `run` deixa claro o papel de orquestrador, sem sufixos obscuros.
- **(−)** Qualquer necessidade operacional nova deve passar por config auditada, não por flag ad-hoc.
- **Nota:** a soberania é garantida pela **regra fail-closed**, não pelo nome do arquivo.
