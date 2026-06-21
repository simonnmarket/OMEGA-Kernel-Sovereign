# OMEGA-KERNEL-SOVEREIGN

**OMEGA Kernel Sovereign — Institutional Trading System with Multi-Strategy Global Orchestrator and Adaptive Risk Management**

> Repositório soberano (V6). Reconstrução controlada do OMEGA OS após decisão do Conselho de
> congelar o V5.5 como evidência forense (`OMEGA_V55_FROZEN`) e impedir a recontaminação estrutural
> observada entre FMED-02 e FMED-05B.

---

## Princípios não-negociáveis (soberania)

1. **Um único runtime soberano.** Proibido manter motores/launchers paralelos.
2. **Sem dados sintéticos no fluxo de decisão.** Falha de dados ⇒ `HOLD` (nunca fallback fabricado).
3. **Ordem alinhada ao sinal.** SL/TP derivam do sinal, não de valores fixos ocultos.
4. **Um único launcher** com *gating* explícito de ambiente (`OMEGA_ENV`).
5. **Telemetria com IDs rastreáveis ponta a ponta** (lineage decisão → execução).
6. **Contratos antes de código** (CFO-02): `contracts/` → interfaces → testes → implementação.

## Segregação de ambiente (obrigatória)

`OMEGA_ENV ∈ {dev, test, demo, exec}` — sem override silencioso. Cada ambiente tem runtime,
logs e auditoria isolados em `runtime/<env>/`.

## Governança (resumo)

| Gate | Significado |
|------|-------------|
| GATE-0 | Declaração formal de soberania assinada (`governance/DECLARACAO_SOBERANIA_GATE0.md`) |
| GATE-1 | V5.5 congelado, somente leitura, snapshot registrado |
| GATE-1.5 | 5 registries de conhecimento preenchidos (`governance/knowledge_extraction/`) |
| GATE-2 | V6 sobe em `dev` com 1 runtime e telemetria com IDs, zero código legacy |
| GATE-3 | Componente migrado com contrato + interface + teste verde + aprovação Taskade |
| GATE-DEMO | Execução DEMO só após GATE-3 de MIG-1..5 |

**Fluxo oficial único (Taskade = fonte única de verdade):**

```
Conselho → Taskade → Especificação → Implementação → Teste → Merge → Deploy
```

Qualquer alteração fora desse fluxo: **STATUS = NÃO OFICIAL**.

## Proteção Git (CFO-04)

- Proibido: `push` direto em `main`, commit sem Task ID, merge sem validação automática.
- Obrigatório: Pull Request, teste automático (CI), aprovação documental.
- Convenção de commit: `[TASK-xxxx] mensagem`.

## Estrutura

```
OMEGA-KERNEL-SOVEREIGN/
├── docs/            # documentação técnica
├── governance/      # GATE-0, extração de conhecimento (espelho do Taskade)
├── architecture/    # topologia canônica do runtime soberano
├── contracts/       # contratos/interfaces ANTES da implementação
├── runtime/         # dev | test | demo | exec (isolados)
├── strategy/        # estratégias
├── execution/       # order manager único (SL/TP = sinal)
├── telemetry/       # logging/auditoria com IDs
├── tests/           # testes
├── audit/           # trilhas de auditoria
├── deployment/      # 1 launcher soberano (gating OMEGA_ENV)
└── archive/         # nunca usado como base de desenvolvimento
```

## Status atual

- **FASE 0:** repositório inicializado (estrutura limpa). Nenhum componente do legacy migrado.
- **Próximo:** preencher GATE-0 e os 5 registries da FASE 1.5 antes de qualquer migração.
