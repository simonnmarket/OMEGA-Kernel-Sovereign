"""Testes de governanca soberana.

Garantem que os artefatos obrigatorios (GATE-0, FASE 1.5, segregacao de
ambiente) permanecem presentes no repositorio. Falham o CI se alguem remover
um pilar de soberania.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_gate0_declaration_exists() -> None:
    assert (ROOT / "governance" / "DECLARACAO_SOBERANIA_GATE0.md").is_file()


def test_knowledge_registries_exist() -> None:
    base = ROOT / "governance" / "knowledge_extraction"
    required = (
        "KNOWLEDGE_MASTER_INDEX.md",
        "BUG_REGISTRY.csv",
        "FIX_REGISTRY.csv",
        "DECISION_REGISTRY.csv",
        "RUNTIME_REGISTRY.csv",
    )
    for name in required:
        assert (base / name).is_file(), f"artefato FASE 1.5 ausente: {name}"


def test_environment_segregation_dirs_exist() -> None:
    for env in ("dev", "test", "demo", "exec"):
        assert (ROOT / "runtime" / env).is_dir(), f"ambiente ausente: runtime/{env}"


def test_migration_allowlist_exists() -> None:
    assert (ROOT / "governance" / "MIGRATION_ALLOWLIST.md").is_file()
