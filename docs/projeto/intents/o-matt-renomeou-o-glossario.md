# O Matt renomeou o glossário para `GLOSSARY.md`, e o aicf ainda declara `CONTEXT.md`

Processo — entrevista: a definir · implementação: a definir

Era o item de backlog "o layout dos domain docs está declarado duas vezes", que dizia que as duas
declarações "concordam hoje por coincidência" no repositório de contexto único e só divergiriam em
monorepo. Deixaram de concordar em qualquer repositório: as skills do Matt Pocock trocaram o nome
do glossário, e o aicf continua mandando escrever em `CONTEXT.md`. O item virou intent, porque
resolver a divergência já está decidido; o que falta decidir é como.

## O que já se sabe

- **A troca é da `1.3.0` do Matt** (PR [#1120](https://github.com/mattpocock/skills/pull/1120)):
  `CONTEXT.md`/`CONTEXT-MAP.md` viraram `GLOSSARY.md`/`GLOSSARY-MAP.md` em `domain-modeling`,
  `grill-with-docs`, `improve-codebase-architecture`, `setup-matt-pocock-skills`, `triage`, `tdd`,
  `diagnosing-bugs`, `ask-matt`, `codebase-design`, `wait-what` e `pr`. O CHANGELOG dele manda quem
  já tinha `CONTEXT.md` fazer `git mv`: "the skills only look for `GLOSSARY.md`/`GLOSSARY-MAP.md`
  going forward". Conferido no clone da tag `v1.3.1` (`24fe0ef`):

  ```bash
  git clone -q --depth 1 --branch v1.3.1 https://github.com/mattpocock/skills matt && cd matt
  grep -rl 'CONTEXT.md' skills | wc -l    # 0
  grep -rl 'GLOSSARY.md' skills | wc -l   # 16
  ```

- **O nome está fixo nas skills; o `docs/agents/domain.md` não redireciona.** Só o próprio setup
  cita esse arquivo — `grep -rl 'docs/agents/domain.md' skills` no mesmo clone devolve
  `skills/engineering/setup-matt-pocock-skills/SKILL.md` e nada mais. Por isso a saída que o item
  de backlog previa — o template do aicf apontar para o `domain.md` quando ele existir — não
  resolve: editar o `domain.md` para dizer `CONTEXT.md` não muda o que o `domain-modeling` lê.
- **O efeito, num repositório com as duas coleções:** o `domain-modeling`, chamado pelo
  `grill-with-docs`, não enxerga o `CONTEXT.md` e cria um `GLOSSARY.md` ao lado. Dois glossários.
  Achado no vilatt em 2026-10-06, antes de rodar o `/setup-matt-pocock-skills` lá: o projeto tem
  `CONTEXT.md` desde o setup do aicf, e o Matt instalado é a `1.3.1`.
- **Onde o aicf declara `CONTEXT.md`** — `grep -rn 'CONTEXT.md' --include='*.md' skills/ CLAUDE.md AGENTS.md README.md README.en.md | grep -v CHANGELOG`
  devolve 9 linhas: o template `skills/setup/templates/claude-md.md`, `ajuda`, `fechar-demanda`,
  `criar-prd` e `criar-spec`, o `CLAUDE.md` e o `AGENTS.md` deste repositório e os dois READMEs.
  Este repositório também tem o próprio `CONTEXT.md` na raiz.
- **Inclinação do usuário: adotar `GLOSSARY.md`.** O nome diz o que o arquivo é; "contexto" é
  jargão de DDD (*bounded context*) que quem chega não reconhece.

## Em aberto para a entrevista

- **Adotar `GLOSSARY.md` ou manter `CONTEXT.md`.** Manter significa aceitar que as skills do Matt
  não enxergam o glossário do aicf. Uma terceira via — o template declarar o nome conforme o Matt
  esteja instalado — deixa projetos com nomes diferentes para a mesma coisa.
- **Os projetos que já receberam o template.** Ele é colado uma vez no setup, então mudar o
  template não muda o `CLAUDE.md` de quem já o tem (o vilatt, por exemplo). Se o `/aicf:setup`
  rodado de novo deve detectar `CONTEXT.md` e oferecer o `git mv`, ou se basta a nota da release.
- **O monorepo**, que era o assunto original do item: o template não conhece `GLOSSARY-MAP.md` nem
  ADR por contexto (`src/<contexto>/docs/adr/`). Se entra junto ou continua de fora até existir o
  primeiro monorepo com as duas coleções, que era o gatilho de reabertura do item.
- **A versão:** um projeto novo passa a nascer com outro nome de arquivo, e quem já tem o setup
  feito não é afetado. Se isso é minor ou patch.

## Origem

Levantado durante a entrevista de
[o usuário escolhe se a governança mora em arquivos ou em issues](../concluidas/escolher-entre-arquivos-e-issues.md),
como duplicação de layout, e reaberto em 2026-10-06 pela troca de nome do Matt.
