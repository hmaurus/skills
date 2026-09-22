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
[o `CHECKLIST.md` sai do método](../concluidas/o-checklist-sai-do-metodo.md): hoje a pasta é
a única fonte, e `head -qn1 docs/projeto/intents/*.md docs/projeto/specs/*.md docs/projeto/concluidas/*.md | sed 's/^# //'` gera a lista dos dois lados. Não há mais índice
manual a trocar por índice gerado, e o que sobra a favor das issues é o item 1 — a contribuição de
fora —, que é o diferencial declarado deste repositório e sempre foi o argumento forte.

## Depende de outra demanda

Este repositório **vende** o workflow aicf. Se a governança dele divergir do que as skills
prescrevem, ele para de comer a própria comida — e a divergência vira exceção não documentada em
vez de recurso.

Por isso esta demanda **não é customização local**: ela consome a opção criada por
[escolher entre arquivos e issues](../concluidas/escolher-entre-arquivos-e-issues.md), e só
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
  `wontfix`), e mapeia quase 1:1 nas pastas de hoje: `backlog/` → `needs-triage`;
  `intents/` → triada e decidida, sem entrevista; `specs/` → `ready-for-agent`;
  `concluidas/` → issue fechada. Alternativa: dois tipos de issue, o que duplica o artefato.
- **Onde fica o relatório de fechamento?** Hoje ele mora no arquivo da demanda, que fica no
  repositório para sempre. Como comentário de issue fechada ele é menos achável, e some do
  `git clone`. É o conflito direto com o lema *"quem precisa saber é o repositório"*.
- **O que acontece com o que já está em `concluidas/`?** Migrar, deixar como arquivo morto,
  ou conviver.
- **O `ROADMAP.md` sobrevive?** É o que sobrou: a lista do que ainda não tem arquivo. Com issues,
  `Próximas` e `Backlog` viram labels — ou o arquivo fica, e a governança passa a morar em duas
  mídias.

## O que [o README reorganizado](../concluidas/a-entrada-de-quem-chega.md) trouxe para cá

Levantado em 2026-09-18, ao implementar aquela demanda. Dois fatos, e o primeiro põe número numa
pergunta que já estava na lista. **Os dois comandos abaixo contam a si mesmos** — este arquivo é uma
das demandas —, então remedir depois de editá-lo dá um número maior, e é o comando que vale.

**A teia de links entre demandas é um custo de migração que ninguém tinha medido.** As demandas
deste repositório se citam: *"precede X"*, *"encolhe o arquivo que Y vai ter que"*, *"entregue na
`0.14.0`"*. Em `7fcb5dc` são **69 links relativos entre elas**
(`grep -rno '\](\.\./[^)]*\.md\|\]([a-z0-9-]*\.md)' docs/projeto/intents/*.md docs/projeto/backlog/*.md docs/projeto/concluidas/*.md | wc -l`)
mais **13 apontando de fora para dentro** — do `CHANGELOG.md`, dos ADRs e das próprias skills
(`grep -rn 'docs/projeto/\(intents\|specs\)' --include='*.md' CLAUDE.md README.md README.en.md CHANGELOG.md docs/adr/ skills/ | wc -l`).
Os números de 2026-09-18, 27 e 14, ficaram para trás porque a teia cresce a cada demanda: é o
comando que vale, não o número.
Migrar as concluídas para issue quebra os 82 de uma vez, e trocar cada um por `#<n>` é trabalho
manual. A rede existe desde a
[nenhum-teste-acusa-link-morto](../concluidas/nenhum-teste-acusa-link-morto.md): o
`./scripts/check.sh` confere link relativo de markdown que aponta para arquivo inexistente, e
imprime `N links conferidos, 0 quebrados`. Ela acusa o que quebrou, não reescreve o que sobrou.

O fechamento de 2026-09-18 já reproduziu a classe do problema em pequena escala — um `git mv` quebrou três links
e eles só foram achados porque o passo 2 do ritual manda procurá-los. Isso pesa a favor de
**conviver** em vez de migrar, e a pergunta "o que acontece com `concluidas/`" passa a ter
um custo escrito em vez de uma intuição.

**O repositório virou exemplo vivo do modo arquivo, e isso é novo.** O `README.md` reescrito
apresenta a árvore de `docs/projeto/` como a explicação principal de onde as coisas ficam, com as
issues logo abaixo como a outra opção. Quem clona este repositório para ver o método funcionando
encontra exatamente o que o README descreveu primeiro. Migrando, o repositório passa a demonstrar
o modo issue enquanto documenta os dois — não é impedimento, e pode até ser melhor (o modo issue
tem menos gente usando, então vê-lo rodando vale mais), mas é decisão consciente e não subproduto.
A entrevista decide qual dos dois o repositório deve demonstrar, e se o README precisa dizer qual
modo está vendo quem chega.

## Regra que nasce daqui, e vale em qualquer mídia

**Exemplo vindo de projeto privado entra anonimizado.** Vale igual em issue e em `.md`, e por isso
não é argumento contra a migração — é regra de escrita, não de mídia. Está na seção `## Registro`
do `CLAUDE.md` desde
[anonimizar as referências ao projeto privado](../concluidas/anonimizar-as-referencias-ao-projeto-privado.md),
a demanda que limpou os três documentos que ainda nomeavam o projeto de origem.

Assumir que a governança é pública **por decisão** torna essa regra mais necessária, não menos:
o que hoje é descuido isolado vira política.
