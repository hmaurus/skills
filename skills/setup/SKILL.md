---
name: setup
description: Cria a base de governança de um projeto novo — docs/projeto/ com PRD e checklist, as pastas de demandas e o CLAUDE.md raiz — e, se o usuário quiser, os padrões de engenharia. Rodar uma vez, no começo do projeto.
disable-model-invocation: true
---

# Setup da governança do projeto

Monta a estrutura que o restante do método assume. Roda uma vez, num projeto novo ou num que
ainda não tem `docs/projeto/`.

**Nunca sobrescrever arquivo existente.** Se algum dos alvos já existe, mostrar quais e
perguntar antes: pular, ou mostrar o diff e deixar o usuário decidir arquivo por arquivo.

## Antes de criar

Perguntar, em pergunta aberta:

1. **Nome do projeto** — se o diretório já tem nome óbvio, propor esse e confirmar.
2. **O que é, em uma ou duas frases** — o suficiente para o `CLAUDE.md` não nascer vazio.

Não entrevistar além disso. Visão, público e modelo entram no PRD depois, com calma — o setup
só prepara o lugar onde eles vão morar.

Depois, com `AskUserQuestion`, perguntar **onde ficam os padrões de engenharia** (idioma,
KISS/YAGNI, validação antes do commit, testes, acessibilidade, tratamento de credencial):

- **No global** (`~/.claude/CLAUDE.md`) — valem para todos os projetos da máquina. Escolha
  natural para quem trabalha sozinho em vários repositórios com o mesmo padrão.
- **No projeto** (`CLAUDE.md` da raiz) — ficam versionados e viajam com o repositório. Escolha
  natural para trabalho em equipe, ou quando este projeto tem padrão próprio.
- **Nenhum dos dois** — o usuário já tem os seus.

## Ferramentas que o projeto usa

Depois das perguntas acima, levantar **o que o usuário já usa**, para o `CLAUDE.md` registrar e
o agente não perguntar de novo a cada sessão.

O catálogo está em [`references/ferramentas.md`](references/ferramentas.md) — ler antes de
perguntar. **Não despejar a lista.** O fluxo é:

1. Perguntar categoria por categoria, começando pelas quatro que o catálogo marca como "sempre
   perguntar": gerenciador de senhas, hospedagem e deploy, banco de dados, CI.
2. Quem já usa alguma coisa, só diz o nome — registrar e passar para a próxima.
3. Quem não sabe do que se trata: explicar para que a categoria serve, em duas frases, e só
   então oferecer as opções do catálogo com a diferença entre elas.
4. As demais categorias (autenticação, pagamento, email, observabilidade, analytics, mídia) só
   entram se a descrição do projeto indicar que fazem falta.

**Não instalar nem configurar nada**, e não insistir em quem respondeu "nenhum" — a resposta
"ainda não uso" é registro válido e evita que o agente presuma que existe.

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

Os templates estão em `templates/` dentro desta skill:

| Template                 | Vai para                                        |
| ------------------------ | ----------------------------------------------- |
| `templates/claude-md.md` | `CLAUDE.md` (raiz)                              |
| `templates/prd.md`       | `docs/projeto/PRD.md`                           |
| `templates/checklist.md` | `docs/projeto/CHECKLIST.md`                     |
| `templates/preferencias.md` | conforme a resposta acima — ver abaixo       |

O que o usuário respondeu sobre ferramentas vira a seção `## Stack e serviços` do `CLAUDE.md`,
no formato que o fim do catálogo mostra: uma linha por ferramenta em uso, com o **nome da
variável de ambiente, nunca o valor**. Categoria não usada não vira linha.

Copiar o conteúdo trocando `<NOME>` pelo nome do projeto e preenchendo a descrição no lugar
indicado. **Não reescrever o template por conta própria** — o que estiver marcado como a
preencher fica marcado; é o usuário que preenche, na primeira demanda ou quando quiser.

Se o projeto já tem `CLAUDE.md` na raiz, não substituir: mostrar a seção "Processos de
desenvolvimento" do template e propor acrescentá-la ao arquivo existente.

## Os padrões de engenharia

`templates/preferencias.md` é um corpo de seções (`## Idioma`, `## Implementação`, …) feito
para ser colado dentro de um `CLAUDE.md`, não para virar arquivo próprio.

**Se o usuário escolheu o global:**

1. Ler `~/.claude/CLAUDE.md`. Se não existe, criar com o conteúdo do template.
2. Se existe, **não sobrescrever e não anexar direto**: mostrar quais seções do template ainda
   não têm equivalente lá e propor acrescentar só essas. Aquele arquivo vale para todos os
   projetos da máquina — inclusive os que não usam este método. Mexer nele sem confirmação
   é fora de escopo desta skill.

**Se o usuário escolheu o projeto:** colar as seções no `CLAUDE.md` da raiz, depois de
"Processos de desenvolvimento".

Em qualquer caso, avisar sobre a única regra do template que muda o comportamento do usuário,
não só o do agente: **credencial não entra no chat** — o valor vai para o `.env` e o agente
recebe apenas o nome da variável.

## Ao terminar

1. Listar o que foi criado e onde.
2. Dizer que o ciclo completo está em `/aicf:workflow-demanda`, e que a primeira demanda pode
   começar por `/aicf:criar-spec`.
3. Sugerir preencher o `PRD.md` como primeira coisa — é dele que sai o checklist inicial.
