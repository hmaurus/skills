# A governança deste repositório passa a viver em issues, e assume ser pública

Processo — entrevista: a definir · implementação: a definir

## Problema

As intents e specs deste repositório são arquivos `.md` em `docs/projeto/`. O repositório é
**público** — então elas já são públicas, mas por acidente, não por decisão. Duas consequências:

**1. Ninguém de fora consegue contribuir com governança.** Sugerir mudança num `.md` exige fork,
branch e PR. Abrir uma issue são dois cliques. Se aluno e usuário devem poder propor demanda e
sugerir ajuste — e devem —, o `.md` é a barreira, não o meio. Hoje a governança é escrita só pelo
mantenedor por construção, não por escolha.

**2. O índice é mantido à mão.** O `CHECKLIST.md` precisa espelhar o que existe em `intents/`,
`specs/` e `specs/concluidas/` — `docs/adr/` não ganhou espelho, por decisão da `0.15.0`, em que
ADR passou a ser artefato do `/domain-modeling`. A deriva descrita em
[o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md) foi mitigada
na `0.14.0` pelo passo 5, que enumera os três pares — mas **mitigada, não dissolvida**: o passo
depende de o fechamento rodar. Com issues não haveria ritual a rodar, e é aqui que o argumento
precisa de cuidado: a lista de issues é gerada, mas **os labels que a alimentam são mantidos à
mão**, e label errado não tem contra o que ser conferido. O ganho desta demanda não é "resolve a
classe A" nem "torna o mecanismo desnecessário" — é trocar um erro detectável por ritual por um
erro menos provável e invisível. Se isso compensa **neste** repositório, cujo diferencial declarado
é a contribuição de fora, é o que a entrevista decide.

## Depende de outra demanda

Este repositório **vende** o workflow aicf. Se a governança dele divergir do que as skills
prescrevem, ele para de comer a própria comida — e a divergência vira exceção não documentada em
vez de recurso.

Por isso esta demanda **não é customização local**: ela consome a opção criada por
[escolher entre arquivos e issues](escolher-entre-arquivos-e-issues.md), e só deve ser
implementada depois dela. Adotar issues aqui antes de a skill suportar issues seria justamente o
que a demanda diz querer evitar.

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
- **O `CHECKLIST.md` sobrevive?** Ele cobre mais que demandas — tem a seção Fundação. Talvez vire
  só isso.

## Item obrigatório: tirar as referências ao projeto privado

Quatro documentos já commitados citam pelo nome um repositório **privado** do mantenedor, usado
como caso de origem. Nenhum traz dado sensível de negócio, mas todos revelam que o repositório
existe, o nome dele e — num caso — o domínio de que trata:

| Arquivo | O que expõe |
| --- | --- |
| `docs/projeto/specs/concluidas/orquestrar-o-framework-escolhido.md` | nome do repo (duas vezes), volume de trabalho |
| `docs/adr/0001-fronteira-de-fase.md` | nome do repo |
| `docs/projeto/specs/concluidas/excecao-de-idioma-no-dominio.md` | nome do repo, o domínio, e o caminho de um ADR interno |

As referências são rasas — nomeiam o repositório e um caminho. Removê-las não custa nada ao
argumento de nenhum dos documentos: em todos, a lição independe de qual projeto a produziu.

**Cuidado:** `docs/adr/0001-fronteira-de-fase.md` é ADR, e a convenção do projeto diz que ADR é
**imutável**. Anonimizar um nome próprio não reverte decisão nenhuma, mas a entrevista deve
decidir a forma — edição direta, ou nota no fim, como o padrão de nota já usado em outros ADRs.

## Regra que nasce daqui, e vale em qualquer mídia

**Exemplo vindo de projeto privado entra anonimizado.** Vale igual em issue e em `.md`, e por isso
não é argumento contra a migração — é regra de escrita que falta hoje. A intent
[o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md) já nasceu sob ela, e é o
primeiro documento do repositório a segui-la explicitamente.

Assumir que a governança é pública **por decisão** torna essa regra mais necessária, não menos:
o que hoje é descuido isolado vira política.
