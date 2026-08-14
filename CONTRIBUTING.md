# Contribuindo para Mistérios do Kernel

As histórias em `data/` são o conteúdo atual do projeto e podem ser editadas, reescritas, movidas ou removidas.

## Adicionar ou alterar uma história

```bash
git clone https://github.com/alanveloso/misterios-do-kernel.git
cd misterios-do-kernel
git checkout -b feat/historia-nova
cp data/_template.yaml data/processos/MK-038.yaml
```

- Um YAML por história
- ID `MK-NNN`, único, igual ao nome do arquivo
- Pasta igual à `categoria`
- Próximo número livre (quantidade dinâmica)

```yaml
id: MK-038
titulo: "Título Breve"
categoria: processos
enigma: >
  Descrição narrativa do problema.
solucao: >
  Explicação técnica do conceito.
conceitos:
  - termo1
autoria:
  - nome: "Seu Nome Completo"
referencias: []
```

Categorias: `processos`, `threads`, `memoria`, `sincronizacao`, `deadlocks`, `escalonamento`, `fundamentos`, `virtualizacao`, `sistemas-de-arquivos`, `io`, `seguranca`.

```bash
make validate
make build
git add data/categoria/MK-NNN.yaml
git commit -m "feat(story): add MK-NNN - título"
git push origin feat/historia-nova
```

O workflow do GitHub Actions valida as histórias e compila o PDF no PR. Uma história nova em `data/` entra sozinha no JSON e no PDF.
