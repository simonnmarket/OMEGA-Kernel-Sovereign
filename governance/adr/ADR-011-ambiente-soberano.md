# ADR-011 — Ambiente Soberano

- **Status:** ✅ Aceito (ratificado no GATE-0, Ata do Conselho 2026-06-22)
- **Origem:** GATE-0-DECL-V6 · TASK-0014
- **Supersede:** — (complementa ADR-005, Segregação de ambientes)
- **Resolve:** BUG-004 (FND-08, env vars sem gating), BUG-009 (FND-02, lockfiles órfãos), BUG-010 (FND-03, flags congeladas/expiradas)

## Contexto
No V5.5, flags de teste vazavam para execução por precedência `env > arquivo` sem *gating*
(BUG-004/FND-08), além de lockfiles órfãos (BUG-009) e flags congeladas sem consumidor (BUG-010).
Não havia isolamento real entre ambientes.

## Decisão
O **ambiente soberano** é declarado por `OMEGA_ENV ∈ {dev, test, demo, exec}`, **explícito** e
sem override silencioso.

Regras:
1. Config, runtime, logs e auditoria **isolados por ambiente** em `runtime/<env>/`.
2. Precedência **`arquivo > env`** — ou `env` somente com *gating* auditado e logado.
3. **Guard DEMO×REAL** no Execution Engine (MIG-5): `trade_mode` validado contra `OMEGA_ENV`
   antes de qualquer operação (condição *sine qua non* do CFO).
4. Sem lockfiles/flags órfãos: estado vinculado ao runtime ativo e ao ambiente declarado.

## Consequências
- **(+)** Impossível flag de teste contaminar execução; DEMO e REAL nunca se confundem.
- **(+)** Estado e logs rastreáveis por ambiente.
- **(−)** Exige disciplina de configuração por ambiente (sem atalhos via env solta).
- **Nota:** `OMEGA_ENV` é *cross-cutting*, mas o **guard DEMO×REAL** é ancorado no MIG-5
  (Execution Engine) por critério de segurança (decisão CFO).
