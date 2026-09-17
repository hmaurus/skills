# A governança deste repositório passa a viver em issues, e assume ser pública

Processo — entrevista: a definir · implementação: a definir

## Problema

As intents e specs deste repositório são arquivos `.md` em `docs/projeto/`. O repositório é
**público** — então elas já são públicas, mas por acidente, não por decisão. Duas consequências:

**1. Ninguém de fora consegue contribuir com governança.** Sugerir mudança num `.md` exige fork,
branch e PR. Abrir uma issue são dois cliques. Se aluno e usuário devem poder propor demanda e
sugerir ajuste — e devem —, o `.md` é a barreira, não o meio. Hoje a governança é escrita só pelo
mantenedor por construção, não por escolha.

**2. O índice deixou de ser argumento.** Este item dizia que o `CHECKLIST.md` era mantido à mão e
que as issues gerariam a lista sozinhas. O índice derivado saiu do método inteiro em
[o `CHECKLIST.md` sai do método](../specs/concluidas/o-checklist-sai-do-metodo.md): hoje a pasta é
a única fonte, e `head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/specs/concluidas/*.md | sed 's/^# //'` gera a lista dos dois lados. Não há mais índice
manual a trocar por índice gerado, e o que sobra a favor das issues é o item 1 — a contribuição de
fora —, que é o diferencial declarado deste repositório e sempre foi o argumento forte.

## Depende de outra demanda

Este repositório **vende** o workflow aicf. Se a governança dele divergir do que as skills
prescrevem, ele para de comer a própria comida — e a divergência vira exceção não documentada em
vez de recurso.

Por isso esta demanda **não é customização local**: ela consome a opção criada por
[escolher entre arquivos e issues](../specs/concluidas/escolher-entre-arquivos-e-issues.md), e só
deve ser implementada depois dela. Adotar issues aqui antes de a skill suportar issues seria
justamente o que a demanda diz querer evitar.

**Desbloqueada em 2026-09-17**, com a `0.17.0` — a opção existe (`grep -m1 'Mídia do registro'
CLAUDE.md` traz a linha, hoje com o valor `arquivos`). Duas das perguntas abaixo já têm resposta
gravada e viram confirmação em vez de decisão aberta: **intent e spec são a mesma issue com o label
mudando** (sim, `aicf:backlog`/`aicf:intent`/`aicf:spec`, exclusivos entre si) e **o relatório vai em
comentário na issue fechada**, sem modo misto. A entrevista ainda decide o que é próprio daqui:
migrar ou não as demandas já concluídas, e o que fazer com o `ROADMAP.md` atual.

## O que decidir na entrevista

- **Intent e spec são a mesma issue, com o label mudando?** É o modelo do Matt Pocock
  (`triage-labels.md`: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
  `wontfix`), e mapeia quase 1:1 nas pastas de hoje: `intents/backlog/` → `needs-triage`;
  `intents/` → triada e decidida, sem entrevista; `specs/` → `ready-for-agent`;
  `specs/concluidas/` → issue fechada. Alternativa: dois tipos de issue, o que duplica o artefato.
- **Onde fica o relatório de fechamento?** Hoje ele mora no arquivo da demanda, que fica no
  repositório para sempre. Como comentário de issue fechada ele é menos achável, e some do
  `git clone`. É o conflito direto com o lema *"quem precisa saber é o repositório"*.
- **O que acontece com o que já está em `specs/concluidas/`?** Migrar, deixar como arquivo morto,
  ou conviver.
- **O `ROADMAP.md` sobrevive?** É o que sobrou: a lista do que ainda não tem arquivo. Com issues,
  `Próximas` e `Backlog` viram labels — ou o arquivo fica, e a governança passa a morar em duas
  mídias.

## Regra que nasce daqui, e vale em qualquer mídia

**Exemplo vindo de projeto privado entra anonimizado.** Vale igual em issue e em `.md`, e por isso
não é argumento contra a migração — é regra de escrita, não de mídia. Está na seção `## Registro`
do `CLAUDE.md` desde
[anonimizar as referências ao projeto privado](../specs/concluidas/anonimizar-as-referencias-ao-projeto-privado.md),
a demanda que limpou os três documentos que ainda nomeavam o projeto de origem.

Assumir que a governança é pública **por decisão** torna essa regra mais necessária, não menos:
o que hoje é descuido isolado vira política.
