# Mistérios do Kernel

Material didático em formato de enigmas para aprender e revisar conceitos de Sistemas Operacionais a partir de situações-problema.

Guia de uso: [docs/manual.md](docs/manual.md). Contribuições: [CONTRIBUTING.md](CONTRIBUTING.md).

As histórias ficam em `data/`: um YAML por história, agrupadas por categoria, com IDs `MK-NNN`. O conjunto é dinâmico. Adicionar um YAML válido é o suficiente para a história entrar no próximo PDF.

## Estrutura

- `data/` — histórias
- `assets/mascara.png` — moldura das cartas
- `src/` — gerador Typst
- `scripts/` — validação e agregação
- `mockup/` — referência visual (não entra no build)


## Dependências

- Python 3, com `PyYAML` (`pip install pyyaml`)
- [Typst](https://github.com/typst/typst) (CLI)

Instalação do Typst (escolha uma):

```bash
# https://github.com/typst/typst/releases
# ou, se disponível no sistema:
snap install typst
# ou
cargo install --locked typst-cli
```

Confirme com `typst --version`.

## Validação e build

```bash
make validate   # scripts/validate.py
make build      # valida, agrega YAML → JSON e gera o PDF
make clean      # remove build/
```

`make build` executa, nesta ordem, e para na primeira falha:

1. `python3 scripts/validate.py`
2. `python3 scripts/build_data.py` → `build/historias.json`
3. `typst compile` → `build/misterios-do-kernel.pdf`

## Arquivos gerados

| Arquivo | Conteúdo |
|---------|----------|
| `build/historias.json` | Histórias agregadas, ordenadas por ID |
| `build/misterios-do-kernel.pdf` | Cartas frente e verso (70 × 100 mm) |

Cada história ocupa duas páginas: frente (enigma) e verso (solução). A pasta `build/` não vai para o Git.

No GitHub, depois de um push ou PR em `main`, o PDF fica em **Actions** → o run que passou → **Artifacts** → `misterios-do-kernel`.

## Nova história

```bash
cp data/_template.yaml data/processos/MK-038.yaml
# edite o arquivo, depois:
make validate
make build
```

Não é necessário listar a história no Typst. Detalhes em [CONTRIBUTING.md](CONTRIBUTING.md).

O PDF é um baseline visual simples (fundo claro, hierarquia de carta). Ainda **não garante alinhamento duplex** para gráfica. O tamanho da carta está só em `src/config.typ`.
