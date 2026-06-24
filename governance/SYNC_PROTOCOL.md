# Protocolo Oficial de Sincronização Manual

**ID:** CFO-DIR-20260623-01 (adaptado PSA) · **Versão:** 2.0 · **Status:** RATIFICADO · **Data:** 2026-06-24

## Objetivo

Estabelecer protocolo auditável e permanente de sincronização entre:

- Conselho
- **PSA** (`OMEGA-PSA-AUDIT-WORKSPACE`)
- **AIC** (`OMEGA-Kernel-Sovereign`)

Garante continuidade operacional, rastreabilidade e preservação do conhecimento institucional.

## Princípio de soberania

```
Conselho
    ↓
PSA (autoridade documental)
    ↓
AIC (executor técnico)
    ↓
GitHub V6 → Validação → Operação
```

**Em divergência:** (1) Conselho prevalece; (2) PSA registra decisão ratificada; (3) AIC executa.

## Papéis oficiais

| Papel | Repositório | Escreve | Domínio |
|-------|-------------|:-------:|---------|
| **PSA** | `OMEGA-PSA-AUDIT-WORKSPACE` | ✅ | Auditoria, documentação, evidências, memória institucional |
| **AIC** | `OMEGA-Kernel-Sovereign` | ✅ | Código, CI/CD, implementação, governança técnica-as-code |
| **Conselho** | — | — | Ratificação de decisões, ADRs, Gates, MIGs |

**Regras:**
- Sem escrita cruzada entre repositórios.
- Leitura cruzada permitida e recomendada.
- PSA **não** executa commits no repo V6.
- AIC **não** cria governança nem redefine ADRs sem ratificação.

## Pacote SYNC-IN (PSA → AIC)

```
SYNC-IN | YYYY-MM-DD
REF: <referência>
DECISÕES: <DECs e ADRs ratificados>
TASKS: <TASK-ID : STATUS>
PRÓXIMO TASK LIVRE: <TASK-XXXX>
EXECUTAR AGORA: <escopo>
RESTRIÇÕES: <limitações>
```

## Pacote SYNC-OUT (AIC → PSA)

```
SYNC-OUT | YYYY-MM-DD
TASK: <TASK-ID>
AÇÃO: <atividade executada>
COMMIT/PR: <hash ou PR>
ARQUIVOS: <lista>
CI: <verde/vermelho>
STATUS: <concluído/bloqueado>
ATUALIZAR NO PSA-WORKSPACE: <atualizações>
```

## Memória permanente

| Artefato | Local | Função |
|----------|-------|--------|
| `SYNC_PROTOCOL.md` | repo V6 (`governance/`) | Normativo — regras e templates |
| `SYNC_LOG.md` | repo V6 (`governance/`) | Auditoria — histórico SYNC-IN/OUT |
| Documentos oficiais | `OMEGA-PSA-AUDIT-WORKSPACE` | Fonte documental canônica |

## Restrições

Este protocolo **não autoriza** alteração operacional sem Gates/MIGs aprovados:

- `runtime/`, `strategy/`, `execution/`, `deployment/`, `telemetry/`, `contracts/`, `tests/`

## Taskade

**Removido da governança ativa** (2026-06-24). PSA substitui integralmente como autoridade documental.
