#!/usr/bin/env python3
"""Agrega data/**/*.yaml em build/historias.json para o Typst."""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "build"
OUT_FILE = OUT_DIR / "historias.json"
TEMPLATE = "_template.yaml"
ID_RE = re.compile(r"^MK-(\d{3})$")


def id_sort_key(historia: dict) -> tuple:
    match = ID_RE.match(str(historia.get("id", "")))
    if not match:
        return (10**9, str(historia.get("id", "")))
    return (int(match.group(1)),)


def descobrir() -> list[Path]:
    return sorted(
        p for p in DATA_DIR.rglob("*.yaml") if p.name != TEMPLATE
    )


def carregar(arquivo: Path) -> dict:
    with open(arquivo, encoding="utf-8") as f:
        conteudo = yaml.safe_load(f)
    if not isinstance(conteudo, list) or len(conteudo) != 1:
        raise ValueError(f"{arquivo}: esperado lista com 1 história")
    h = conteudo[0]
    if not isinstance(h, dict):
        raise ValueError(f"{arquivo}: história inválida")
    return {
        "id": h.get("id", ""),
        "titulo": str(h.get("titulo", "")).strip(),
        "categoria": str(h.get("categoria", "")).strip(),
        "enigma": str(h.get("enigma", "")).strip(),
        "solucao": str(h.get("solucao", "")).strip(),
        "conceitos": h.get("conceitos") or [],
        "autoria": h.get("autoria") or [],
        "referencias": h.get("referencias") or [],
    }


def main() -> None:
    arquivos = descobrir()
    historias = [carregar(p) for p in arquivos]
    historias.sort(key=id_sort_key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(historias, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"✓ {len(historias)} história(s) → {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
