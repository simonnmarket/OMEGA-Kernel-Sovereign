# AIC-PARECER-MIG1-001

**Parecer Técnico Independente — TASK-0021 MIG-1 Charter**

| Campo | Valor |
|-------|-------|
| **ID** | AIC-PARECER-MIG1-001 |
| **Data** | 2026-06-24 |
| **Emitido por** | AIC (Executor Técnico — `OMEGA-Kernel-Sovereign`) |
| **Destinatários** | PSA · CFO · Conselho |
| **Responde a** | PSA-SYNC-IN-AIC-001 · CFO-DIRECTIVE-20260624-AIC-REVIEW-001 |
| **Documento revisado** | TASK-0021-MIG1-CHARTER.md (PSA workspace) |
| **Repositório analisado** | `main` @ `af8f3c8` |

---

## VEREDITO

# FAVORÁVEL COM RESSALVAS

O Charter é **tecnicamente sólido na intenção** e **alinhado ao Plano Mestre** na sequência MIG-1 → BUG-001/BUG-003. A implementação é **factível** no estado atual do V6 (scaffold + CI + governança).

**Não recomendo autorização de implementação** até correção das **ressalvas obrigatórias** listadas na Seção 8 — especialmente divergências documentais PSA↔V6 e contradições internas do Charter (CA-10 vs entregáveis).

---

## 1. VIABILIDADE TÉCNICA

**Avaliação: FAVORÁVEL**

Com base no estado do repositório V6 em `af8f3c8`:

| Elemento | Estado | Implicação |
|----------|--------|------------|
| `indicator_engine/` | ❌ Não existe | Greenfield — sem dívida legacy no repo |
| `contracts/` | ✅ Diretório existe (README only) | Contrato deve ser criado **antes** do código (CFO-02) |
| CI (ruff + pytest) | ✅ Ativo | Suporta CA-07 |
| Dependências runtime | ⚠️ Vazio (`pyproject.toml`) | Requer decisão sobre libs numéricas (ver R-05) |
| GATE-0 GOVERNANÇA | ✅ Fechado (DEC-16 / CFO-RAT-20260624-002) | Pré-condição MIG-1 satisfeita |

**Conclusão:** Construir um Indicator Engine soberano com contrato tipado, testes e telemetria básica é **tecnicamente factível** sem alterar runtime/strategy/execution/deployment.

**Limitação:** O parecer certifica viabilidade **lógica/arquitetural** (Nível 1–2). Não há execução de trading ou integração broker validada nesta fase.

---

## 2. DEPENDÊNCIAS OCULTAS

**Avaliação: RESSALVA — 6 dependências não explicitadas no Charter**

| ID | Dependência | Severidade | Detalhe |
|----|-------------|------------|---------|
| D-01 | **Contrato de entrada `MarketData`** | Alta | `calculate(market_data)` exige schema mínimo (OHLCV, timestamps). MIG-2 não existe, mas o **tipo de entrada** deve ser definido em `contracts/` na MIG-1 — sem acoplar implementação MIG-2 |
| D-02 | **Biblioteca numérica** | Alta | RSI/EMA/ATR/MACD requerem `numpy`, `pandas` ou implementação pura Python. `pyproject.toml` não declara dependências; adicionar lib exige Task/ratificação |
| D-03 | **Definição estratégica V6** | Média | Chaves canônicas (`ema_fast`, `ema_slow`, períodos) devem ser validadas contra estratégia V6 — ainda não especificada no repo |
| D-04 | **Telemetria** | Média | CA-08 exige logs com timestamp + ID. Não existe módulo `telemetry/` implementado. Charter deve definir se `logging` stdlib + schema JSON basta na MIG-1 ou se exige stub de telemetria |
| D-05 | **ADR-004 / ADR-006 no espelho V6** | Média | Charter cita ADR-004 e ADR-006 como "Aprovadas". No repo V6, `governance/adr/README.md` lista ambas como **🟡 Pendente (V6)**. ADR-010 (Aceito) já cobre os requisitos — alinhar referências |
| D-06 | **DEC-18 vs DEC-16** | Baixa (governança) | Charter referencia DEC-18 (GATE-0 fechado). Repo V6 registra **DEC-16**. PSA deve unificar ID |

---

## 3. ADERÊNCIA AO ADR-012

**Avaliação: FAVORÁVEL COM RESSALVAS**

| Critério ADR-012 | Charter | AIC |
|------------------|---------|-----|
| MIG-1 após GATE-0 | ✅ | Confirmado |
| BUG-001 + BUG-003 | ✅ | Alinhado ao `BUG_REGISTRY.csv` V6 |
| Sequência MIG-1 → MIG-2 | ✅ | Respeitada |
| Sem execução paralela | ✅ | Escopo excluído explícito |
| CFO-03 (foco) | ✅ | Charter não desvia roadmap |

**Divergências detectadas (PSA workspace vs V6 canônico):**

| Documento PSA | Problema |
|---------------|----------|
| `MIGRATION_ALLOWLIST.md` v3.0 | **BUG-003** descrito como "SL/TP fixos" — **incorreto**. Canônico V6: *8 filtros PASS hardcoded* |
| `MIGRATION_ALLOWLIST.md` v3.0 | **BUG-006** descrito como "Key mismatch RSI" — **incorreto**. Canônico V6: *SL/TP não derivam do sinal* → MIG-4 |
| `ADR-012_PLANO_MESTRE.md` | ETAPA 0 ainda marcada "EM PROGRESSO" — **desatualizado** (fechada 2026-06-24) |
| `ADR-012` PSA | Nota sobre ADR-009..011 "reservados" — **colide** com ADR-009..011 GATE-0 aceitos no V6 |

**Recomendação:** PSA deve sincronizar espelhos antes da aprovação final — risco de parada imediata ADR-012 ("Divergência PSA ↔ AIC").

---

## 4. CRITÉRIOS DE ACEITE (CA-01 a CA-10)

**Avaliação: FAVORÁVEL COM RESSALVAS**

| CA | Realista? | Verificável? | Observação AIC |
|----|-----------|--------------|----------------|
| CA-01 | ✅ | ✅ | Correto e essencial |
| CA-02 | ✅ | ✅ | Alinhado BUG-001 / ADR-010 |
| CA-03 | ⚠️ | ✅ | Requer confirmação estratégica dos períodos EMA |
| CA-04 | ⚠️ | ✅ | Idem CA-03 |
| CA-05 | ⚠️ | ⚠️ | **Problemático:** filtros PASS estavam em `shadow_loop` (estratégia/loop legacy), **não** no Indicator Engine. Grep zero em `indicator_engine/` é **trivialmente satisfazível** sem provar mitigação de BUG-003. Reformular: *"Indicator Engine não implementa filtros de validação fake; validação real é responsabilidade MIG-5 ou consumidor"* |
| CA-06 | ✅ | ✅ | Correto — preceder implementação (CFO-02). Ajustar import path: `contracts.indicator_contract` (package ainda não estruturado) |
| CA-07 | ✅ | ✅ | Realista |
| CA-08 | ⚠️ | ⚠️ | Falta definir formato mínimo (campos obrigatórios do log) e destino (`logging` vs `telemetry/`) |
| CA-09 | ✅ | ✅ | Correto — fail-explicit, anti-None silencioso |
| CA-10 | ❌ | ✅ | **Contradiz** Seções 12, 15 e entregáveis (`contracts/`, `tests/`). Deve ser: *"`git diff` limitado a `indicator_engine/`, `contracts/` (indicator only), `tests/test_indicator_engine.py`, `pyproject.toml` (deps indicator se aprovadas)"* |

---

## 5. RISCOS TÉCNICOS

**Avaliação: Charter cobre riscos principais; AIC identifica 7 adicionais**

### Riscos já mapeados no Charter — concordância AIC

| Risco Charter | Concordância |
|---------------|--------------|
| Dependência Market Data (MIG-2) | ✅ Válido — mitigação mock-only-in-tests correta |
| Mudança de chaves quebra downstream | ✅ Válido — contrato + versionamento necessários |
| Escopo creep | ✅ Válido |
| Implementação sem aprovação | ✅ Válido |

### Riscos adicionais identificados pelo AIC

| ID | Risco | Prob. | Impacto | Mitigação sugerida |
|----|-------|-------|---------|-------------------|
| R-AIC-01 | **Divergência BUG_REGISTRY PSA ↔ V6** | Alta | Crítico | PSA corrige `MIGRATION_ALLOWLIST` v3.0 antes de aprovação |
| R-AIC-02 | **BUG-003 escopo mal definido** | Alta | Alto | Clarificar: MIG-1 não replica filtros PASS; MIG-5 ou strategy consome indicadores validados |
| R-AIC-03 | **CA-05 falso positivo** | Média | Alto | Reformular CA-05 (ver Seção 4) |
| R-AIC-04 | **Dependência numérica não ratificada** | Média | Médio | ADR ou DEC para lib escolhida + pin de versão |
| R-AIC-05 | **Input contract sem MIG-2** | Média | Alto | Definir `MarketDataSnapshot` mínimo em contracts (read-only struct) |
| R-AIC-06 | **Sobreposição MIG-1 / MIG-5** | Baixa | Médio | Charter deve declarar que *validação de sinal* (filtros) ≠ *cálculo de indicador* |
| R-AIC-07 | **Charter descreve BUG-004 incorretamente** | Média | Médio | Seção 3: BUG-004 ≠ "múltiplos launchers" — canônico: *env vars sem gating* (MIG-6) |

---

## 6. PLANO DE ROLLBACK

**Avaliação: FAVORÁVEL**

| Aspecto | Análise |
|---------|---------|
| Mecanismo `git revert` | ✅ Viável — MIG-1 adiciona diretórios novos, revert limpo |
| Isolamento sequencial | ✅ MIG-2+ não iniciadas — sem dependência downstream no código |
| CI pós-rollback | ✅ Verificável |
| Procedimento 5 passos | ✅ Adequado |

**Ressalva menor:** Se `pyproject.toml` ganhar dependências na MIG-1, rollback deve incluir reversão dessas entradas.

---

## 7. ISOLAMENTO DE ESCOPO (MIG-1 vs demais MIGs)

**Avaliação: FAVORÁVEL COM RESSALVA**

| Fronteira | Isolada? | Nota |
|-----------|----------|------|
| MIG-2 Market Data | ✅ | Mock apenas em tests — correto |
| MIG-3 Position | ✅ | Excluído |
| MIG-4 Risk | ✅ | Excluído |
| MIG-5 Signal Validation | ⚠️ | BUG-003/filtros PASS — Charter deve deixar explícito que **filtros não pertencem ao Indicator Engine** |
| MIG-6 Execution | ✅ | Excluído |
| runtime/strategy/execution/deployment | ✅ | Proibidos — alinhado |

**Contradição a resolver:** Seção 5 exclui "Estratégia", mas BUG-003 no legacy era código de loop estratégico. MIG-1 resolve BUG-003 **por não reproduzir o anti-padrão** e por entregar indicadores confiáveis — não por portar/remover filtros do shadow_loop.

---

## 8. RESSALVAS OBRIGATÓRIAS (pré-aprovação implementação)

| # | Ressalva | Responsável |
|---|----------|-------------|
| 1 | Corrigir mapeamento BUG-003/BUG-006 no PSA `MIGRATION_ALLOWLIST.md` | PSA |
| 2 | Unificar DEC-18 → DEC-16 (ou registrar DEC-18 espelhado) | PSA |
| 3 | Atualizar ADR-012 PSA: ETAPA 0 = CONCLUÍDA | PSA |
| 4 | Reformular **CA-05** (anti falso positivo) | PSA + Conselho |
| 5 | Reformular **CA-10** para incluir `contracts/` e `tests/` permitidos | PSA + Conselho |
| 6 | Definir schema mínimo `MarketDataSnapshot` em contracts | AIC (na implementação, pós-aprovação) |
| 7 | Ratificar dependência numérica (numpy/pandas ou pure Python) | CFO + Conselho |
| 8 | Corrigir descrição BUG-004 na Seção 3 do Charter | PSA |
| 9 | Alinhar referências ADR-004/006 → ADR-010 aceito ou promover ADR-004/006 a Aceito no V6 | PSA + Conselho |

---

## 9. SUGESTÕES DE ALTERAÇÃO AO CHARTER

### 9.1 CA-05 (substituir)

```
CA-05: Indicator Engine não contém filtros de validação hardcoded tipo PASS;
       validação de sinal é escopo MIG-5. Verificação: code review + ausência
       de branches unconditionally PASS em indicator_engine/.
```

### 9.2 CA-10 (substituir)

```
CA-10: git diff limitado a:
       indicator_engine/, contracts/indicator_contract.py,
       tests/test_indicator_engine.py, pyproject.toml (deps MIG-1 se aprovadas),
       governance/ (somente evidências EV-02/EV-06 se aplicável)
```

### 9.3 Seção 14 — adicionar nota

```
volume: proveniente de MarketDataSnapshot de entrada; Indicator Engine propaga
        no output somente se presente na entrada validada — não calcula volume.
```

### 9.4 Seção 3 — BUG-003 (clarificar)

```
BUG-003 no legacy residia na camada de loop estratégico (shadow_loop), não no
motor de indicadores. MIG-1 mitiga ao (a) nunca emitir indicadores inválidos/None
e (b) não implementar filtros fake. Remoção literal dos 8 PASS do legacy é
evidência forense, não escopo de código a portar.
```

### 9.5 Pré-condição implementação (adicionar)

```
Ordem CFO-02 obrigatória na MIG-1:
  1. contracts/indicator_contract.py
  2. tests/test_indicator_contract.py (falha antes da impl)
  3. indicator_engine/ implementação
  4. tests/test_indicator_engine.py
```

---

## 10. ESTIMATIVA PRELIMINAR DE COMPLEXIDADE

| Fase | Escopo | Complexidade | Estimativa |
|------|--------|--------------|------------|
| Contrato + tipos entrada/saída | `contracts/` | Baixa | 0,5–1 dia |
| Engine core (RSI, EMA, ATR) | `indicator_engine/` | Média | 1–2 dias |
| Testes + edge cases + CA-09 | `tests/` | Média | 1–1,5 dias |
| Telemetria mínima CA-08 | logging estruturado | Baixa | 0,5 dia |
| PR + evidências EV-01..06 | governança | Baixa | 0,5 dia |

**Total preliminar: 3,5–5,5 dias úteis** (1 engenharia, assumindo lib numérica aprovada e estratégia V6 confirma chaves).

**Incerteza:** ±1,5 dia se períodos EMA/RSI exigirem iteração com Conselho ou se pure-Python escolhido por política zero-deps.

---

## 11. TABELA RESUMO — 7 EIXOS SOLICITADOS

| # | Eixo | Veredito parcial |
|---|------|------------------|
| 1 | Viabilidade técnica | ✅ Favorável |
| 2 | Dependências ocultas | ⚠️ 6 identificadas |
| 3 | Aderência ADR-012 | ⚠️ Ressalvas documentais PSA↔V6 |
| 4 | Critérios de aceite | ⚠️ CA-05 e CA-10 requerem revisão |
| 5 | Riscos técnicos | ⚠️ +7 riscos AIC |
| 6 | Rollback | ✅ Favorável |
| 7 | Isolamento escopo | ✅ Favorável (clarificar BUG-003) |

---

## 12. DECLARAÇÃO DE LIMITAÇÕES DO PARECER

- Análise baseada em documentos PSA (GitHub raw) e repo V6 `main` @ `af8f3c8`.
- **Não** inclui execução de código, benchmarks ou acesso ao legado `OMEGA_V55_FROZEN`.
- **Não** autoriza implementação — conforme PSA-SYNC-IN-AIC-001 §5.
- Divergências PSA↔V6 devem ser resolvidas pelo PSA (autoridade documental) antes do Conselho aprovar implementação.

---

## 13. RECOMENDAÇÃO FINAL AIC

1. **Aceitar Charter para deliberação** com ressalvas obrigatórias (Seção 8).
2. **PSA** corrige divergências documentais e CA-05/CA-10.
3. **Conselho** aprova Charter revisado + dependência numérica.
4. **Somente então** emitir autorização de implementação MIG-1 ao AIC.

---

**Emitido por:** AIC — OMEGA Kernel Sovereign V6  
**Data:** 2026-06-24  
**Status:** EMITIDO — AGUARDANDO REGISTRO PSA  
**Implementação MIG-1:** 🔒 BLOQUEADA (inalterado)

---

**FIM DO PARECER**
