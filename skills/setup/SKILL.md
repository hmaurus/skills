---
name: setup
description: Cria a base de governança de um projeto novo — docs/projeto/ com PRD e checklist, as pastas de demandas e o CLAUDE.md raiz. Rodar uma vez, no começo do projeto.
disable-model-invocation: true
---

# Setup da governança do projeto

Monta a estrutura que o restante do método assume. Roda uma vez, num projeto novo ou num que
ainda não tem `docs/projeto/`.

**Nunca sobrescrever arquivo existente.** Se algum dos alvos já existe, mostrar quais e
perguntar antes: pular, ou mostrar o diff e deixar o usuário decidir arquivo por arquivo.

## Antes de criar

Perguntar duas coisas, em pergunta aberta:

1. **Nome do projeto** — se o diretório já tem nome óbvio, propor esse e confirmar.
2. **O que é, em uma ou duas frases** — o suficiente para o `CLAUDE.md` não nascer vazio.

Não entrevistar além disso. Visão, público e modelo entram no PRD depois, com calma — o setup
só prepara o lugar onde eles vão morar.

## O que criar

```
CLAUDE.md                       # raiz, se ainda não existir
docs/projeto/
├── PRD.md
├── CHECKLIST.md
└── demandas/
    ├── concluidas/.gitkeep
    └── backlog/.gitkeep
```

Os três templates estão em `templates/` dentro desta skill:

| Template            | Vai para              |
| ------------------- | --------------------- |
| `templates/claude-md.md` | `CLAUDE.md` (raiz)    |
| `templates/prd.md`       | `docs/projeto/PRD.md` |
| `templates/checklist.md` | `docs/projeto/CHECKLIST.md` |

Copiar o conteúdo trocando `<NOME>` pelo nome do projeto e preenchendo a descrição no lugar
indicado. **Não reescrever o template por conta própria** — o que estiver marcado como a
preencher fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser.

Se o projeto já tem `CLAUDE.md` na raiz, não substituir: mostrar a seção "Processos de
desenvolvimento" do template e propor acrescentá-la ao arquivo existente.

## Ao terminar

1. Listar o que foi criado.
2. Dizer que o ciclo completo está em `/aicf:workflow-demanda`, e que a primeira demanda pode
   começar por `/aicf:criar-spec`.
3. Sugerir preencher o `PRD.md` como primeira coisa — é dele que sai o checklist inicial.
