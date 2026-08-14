#!/usr/bin/env python3
"""Validador estrutural das histórias em data/."""

import sys
import yaml
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Optional

DATA_DIR = Path("data")
TEMPLATE_FILE = "_template.yaml"

CATEGORIAS_PERMITIDAS = {
    "processos",
    "threads",
    "memoria",
    "sincronizacao",
    "deadlocks",
    "escalonamento",
    "fundamentos",
    "virtualizacao",
    "sistemas-de-arquivos",
    "io",
    "seguranca",
}


def descobrir_arquivos_historias() -> List[Path]:
    if not DATA_DIR.exists():
        print(f"❌ Diretório {DATA_DIR} não encontrado!")
        sys.exit(1)

    return sorted(
        p for p in DATA_DIR.rglob("*.yaml") if p.name != TEMPLATE_FILE
    )


def validar_arquivo(arquivo: Path) -> Tuple[Optional[dict], List[str]]:
    erros = []

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return None, [f"YAML inválido: {e}"]
    except Exception as e:
        return None, [f"Erro ao ler arquivo: {e}"]

    if not isinstance(conteudo, list) or len(conteudo) != 1:
        return None, ["Deve conter lista com exatamente 1 item"]

    historia = conteudo[0]
    if not isinstance(historia, dict):
        return None, ["Item deve ser dicionário"]

    id_valor = historia.get("id", "")
    if not id_valor:
        erros.append("ID ausente")
    else:
        partes = str(id_valor).split("-")
        if len(partes) != 2 or partes[0] != "MK" or not partes[1].isdigit():
            erros.append(f"ID '{id_valor}' deve estar no formato MK-NNN")
        if arquivo.name != f"{id_valor}.yaml":
            erros.append(f"Nome arquivo {arquivo.name} ≠ ID {id_valor}.yaml")

    titulo = historia.get("titulo", "")
    if not titulo or not str(titulo).strip():
        erros.append("Título ausente")

    categoria = historia.get("categoria", "")
    if not categoria:
        erros.append("Categoria ausente")
    elif categoria not in CATEGORIAS_PERMITIDAS:
        erros.append(f"Categoria '{categoria}' inválida")
    elif arquivo.parent.name != categoria:
        erros.append(f"Pasta '{arquivo.parent.name}' ≠ categoria '{categoria}'")

    for campo in ("enigma", "solucao"):
        valor = historia.get(campo, "")
        if not valor or not str(valor).strip():
            erros.append(f"Campo '{campo}' ausente")

    conceitos = historia.get("conceitos")
    if not isinstance(conceitos, list) or not conceitos:
        erros.append("conceitos deve ser uma lista não vazia")
    else:
        for i, c in enumerate(conceitos):
            if not isinstance(c, str) or not c.strip():
                erros.append(f"conceito {i + 1} inválido")

    autoria = historia.get("autoria")
    if not isinstance(autoria, list):
        erros.append("autoria deve ser uma lista")
    else:
        for i, autor in enumerate(autoria):
            if not isinstance(autor, dict) or not str(autor.get("nome", "")).strip():
                erros.append(f"autor {i + 1} deve ter 'nome'")

    refs = historia.get("referencias")
    if not isinstance(refs, list):
        erros.append("referencias deve ser uma lista")
    else:
        for i, ref in enumerate(refs):
            if not isinstance(ref, dict):
                erros.append(f"referência {i + 1} deve ser um dicionário")

    return historia, erros


def main():
    print("🔍 Validando histórias...\n")
    arquivos = descobrir_arquivos_historias()
    print(f"✓ Descobertos {len(arquivos)} arquivo(s)\n")

    historias_validas = {}
    todos_erros = []
    ids_vistos = {}

    for arquivo in arquivos:
        historia, erros = validar_arquivo(arquivo)
        if erros:
            todos_erros.extend((str(arquivo), e) for e in erros)
            continue

        historias_validas[arquivo] = historia
        id_valor = historia.get("id", "")
        if id_valor in ids_vistos:
            todos_erros.append(
                (str(arquivo), f"ID '{id_valor}' duplicado (já existe em {ids_vistos[id_valor]})")
            )
        else:
            ids_vistos[id_valor] = str(arquivo)

    print("=" * 80)
    print("📋 RELATÓRIO DE VALIDAÇÃO")
    print("=" * 80)
    print("")
    print(f"📊 Total analisado: {len(arquivos)}")
    print(f"   ✓ Válidas: {len(historias_validas)}")
    print(f"   ✗ Com erros: {len(arquivos) - len(historias_validas)}")
    print("")

    if todos_erros:
        print("❌ ERROS ENCONTRADOS")
        print("─" * 80)
        for arquivo, erro in todos_erros:
            print(f"  • {arquivo}")
            print(f"    → {erro}")
        print("")

    if historias_validas:
        print("📂 DISTRIBUIÇÃO POR CATEGORIA")
        print("─" * 80)
        distribuicao = defaultdict(int)
        for historia in historias_validas.values():
            distribuicao[historia.get("categoria", "?")] += 1
        for categoria in sorted(distribuicao):
            print(f"  • {categoria:25s}: {distribuicao[categoria]:2d} histórias")
        print("")

    print("=" * 80)
    if todos_erros:
        print("❌ VALIDAÇÃO FALHOU")
        print(f"   {len(todos_erros)} erro(s) encontrado(s)")
        sys.exit(1)

    print(f"✅ VALIDAÇÃO PASSOU - {len(historias_validas)} histórias conformes")
    sys.exit(0)


if __name__ == "__main__":
    main()
