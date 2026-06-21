# DECLARAÇÃO FORMAL DE SOBERANIA — GATE-0

**ID:** GATE-0-DECL-V6 · **Repositório:** OMEGA-KERNEL-SOVEREIGN · **Status:** ⬜ PENDENTE DE RATIFICAÇÃO

> Emenda CFO-03 (OBRIGATÓRIA). Sem as 4 respostas abaixo formalmente assinadas, o V6
> **não pode iniciar a migração** — caso contrário "V6 nasce contaminado".

---

## As 4 perguntas soberanas

### 1. Qual é o **runtime soberano**?
- **Definição canônica:** _(a preencher)_ — diretório/módulo único que constitui o runtime oficial.
- **Localização:** `runtime/<env>/` conforme `OMEGA_ENV`.
- **Proibição:** nenhum outro runtime executável pode coexistir.

### 2. Qual é o **launcher soberano**?
- **Definição canônica:** _(a preencher)_ — **um único** ponto de entrada em `deployment/`.
- **Gating:** exige `OMEGA_ENV ∈ {dev,test,demo,exec}` explícito; sem override silencioso.
- **Proibição:** múltiplos launchers / scripts `*_final_fix*` paralelos.

### 3. Qual é o **fluxo soberano**?
- **Definição canônica:** `dados → indicadores → estratégia → risco → execução → telemetria`.
- **Regra:** nenhum desvio, atalho ou caminho concorrente. Falha em qualquer etapa ⇒ `HOLD`.
- **Proibição:** fallback sintético, SL/TP fixos ocultos, decisões fora do fluxo.

### 4. Qual é o **ambiente soberano**?
- **Definição canônica:** `OMEGA_ENV` declarado explicitamente em cada execução.
- **Regra:** configs isoladas por ambiente; precedência **não** pode ser `env > arquivo` sem gating.
- **Proibição:** flags/overrides não rastreados (anti-FND-08).

---

## Ratificação

| Papel | Nome | Assinatura | Data |
|-------|------|-----------|------|
| CEO | | ⬜ | |
| CTO / Tech Lead | | ⬜ | |
| CFO | | ⬜ | |
| CQO | | ⬜ | |
| COO | | ⬜ | |

**GATE-0 só é considerado APROVADO quando as 4 respostas estiverem preenchidas e assinadas acima.**

---

## Vínculo de governança
- Fonte de verdade: **Taskade** (Conselho → Taskade → Especificação → ...).
- Este documento é o **espelho local** da decisão; divergência ⇒ Taskade prevalece.
