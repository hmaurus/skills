# O Matt renomeou o glossário para `GLOSSARY.md`, e o aicf ainda declara `CONTEXT.md`

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (troca de nome em lugares já enumerados, sem decisão de abordagem)

## Problema

O aicf manda gravar o glossário do domínio em `CONTEXT.md`: o template do `CLAUDE.md` que o
`/aicf:setup` cola, o passo 3 do `/aicf:fechar-demanda`, a `ajuda`, a `criar-prd` e a
`criar-spec`. Desde a `1.3.0` (PR [#1120](https://github.com/mattpocock/skills/pull/1120)), as
skills do Matt Pocock procuram só `GLOSSARY.md`/`GLOSSARY-MAP.md`. Num projeto com as duas
coleções, o `domain-modeling`, chamado pelo `grill-with-docs`, não enxerga o `CONTEXT.md` e cria um
`GLOSSARY.md` ao lado, e o projeto fica com dois glossários. Foi o que apareceu num projeto privado
que consome estas skills, em 2026-10-06, com o Matt `1.3.1` instalado.

A troca é do Matt e está fixa no texto das skills dele. O `docs/agents/domain.md` não redireciona:
só o próprio setup do Matt cita esse arquivo. Conferido no clone da tag `v1.3.1` (`24fe0ef`):

```bash
git clone -q --depth 1 --branch v1.3.1 https://github.com/mattpocock/skills matt && cd matt
grep -rl 'CONTEXT.md' skills | wc -l             # 0
grep -rl 'GLOSSARY.md' skills | wc -l            # 16
grep -rl 'docs/agents/domain.md' skills          # só setup-matt-pocock-skills/SKILL.md
```

O `README.md` (linha 151) e o `README.en.md` (linha 153) afirmam que o `domain-modeling` "grava o
vocabulário do projeto num `CONTEXT.md`", o que já é falso para o Matt atual.

## Solução

O aicf passa a declarar **`GLOSSARY.md`**, o mesmo nome do Matt. O nome diz o que o arquivo é;
"contexto" vem do *bounded context* do DDD, e quem chega não reconhece o termo.

- Toda menção de `CONTEXT.md` como o glossário do projeto, nas skills, no template, no `CLAUDE.md`
  deste repositório, nos dois READMEs e no PRD, troca para `GLOSSARY.md`.
- Este repositório migra o próprio glossário: `git mv CONTEXT.md GLOSSARY.md`.
- **Quem já tem o setup feito migra pela nota da release.** O `/aicf:setup` roda uma vez e nunca
  sobrescreve arquivo existente (`skills/setup/SKILL.md`, linhas 9–13), e nenhuma skill ganha
  lógica de migração nem aceita os dois nomes. As notas da `v0.36.0` dizem o que fazer:
  `git mv CONTEXT.md GLOSSARY.md` e trocar o nome na linha **Glossário do domínio** do
  `CLAUDE.md` do projeto.
- **Versão `0.36.0` (minor):** muda o arquivo que um projeto novo recebe e o nome que as skills
  mandam gravar, e quem já tem o setup precisa agir para continuar alinhado com o Matt.

## Arquivos e interfaces

| Arquivo | O que muda |
| --- | --- |
| `skills/setup/templates/claude-md.md:17` | linha **Glossário do domínio** |
| `skills/fechar-demanda/SKILL.md:55` | linha "Termo ambíguo do domínio" da tabela do passo 3 |
| `skills/ajuda/SKILL.md:90` | "PRD, ADR e `CONTEXT.md`" |
| `skills/criar-prd/SKILL.md:86` | onde o `domain-modeling` grava o glossário |
| `skills/criar-spec/SKILL.md:45` | "vocabulário do domínio do projeto" |
| `.claude/CLAUDE.md:21` | linha **Glossário do domínio** deste repositório |
| `README.md:151`, `README.en.md:153` | o que o `domain-modeling` grava |
| `docs/projeto/PRD.md:47`, `:56` | destinos da promoção de conhecimento |
| `CONTEXT.md` → `GLOSSARY.md` | `git mv`, conteúdo intacto |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.36.0` e a entrada do topo |

Os números de linha são os de `064ee85`. O inventário se refaz com
`grep -rn 'CONTEXT.md' --include='*.md' skills/ .claude/CLAUDE.md README.md README.en.md docs/projeto/PRD.md`,
que devolve 10 linhas antes da mudança.

## Fora de escopo

- **Monorepo** (`GLOSSARY-MAP.md`, ADR por contexto em `src/<contexto>/docs/adr/`). Era o assunto
  original do item de backlog que deu origem a este. Continua de fora até existir o primeiro
  monorepo com as duas coleções instaladas, que era o gatilho de reabertura do item.
- **Migração automática nos projetos existentes.** Detectar `CONTEXT.md` numa segunda rodada do
  `/aicf:setup` contradiz o "roda uma vez" dele; propor o `git mv` no `/aicf:fechar-demanda` deixa
  um caminho de migração morando para sempre numa skill; aceitar os dois nomes deixa dois
  mecanismos convivendo, o que o lema do projeto aponta como gatilho de revisão. A nota da release
  resolve a migração com um comando e uma linha editada.
- **Registros históricos.** `CHANGELOG.md`, `docs/projeto/concluidas/` e
  `docs/referencias/governanca-nos-frameworks-vizinhos.md` citam `CONTEXT.md` como era na época ou
  no sha pinado. Continuam corretos para aquele momento e não mudam.
- **Template declarar o nome conforme o Matt esteja instalado.** Projetos diferentes teriam nomes
  diferentes para a mesma coisa.

## Verificação

1. O nome antigo sai de onde as skills e os docs vivos o declaram:
   `grep -rn 'CONTEXT.md' --include='*.md' skills/ .claude/CLAUDE.md README.md README.en.md docs/projeto/PRD.md | wc -l`
   devolve 10 em `064ee85` e 0 depois.
2. O nome novo entra nos mesmos lugares:
   `grep -rln 'GLOSSARY.md' --include='*.md' skills/ .claude/CLAUDE.md README.md README.en.md docs/projeto/PRD.md | wc -l`
   devolve 0 em `064ee85` e 9 depois (sete arquivos de skill e de doc mais os dois READMEs; o
   `PRD.md` conta uma vez).
3. O glossário deste repositório mudou de nome sem mudar de conteúdo:
   `test -f GLOSSARY.md && ! test -e CONTEXT.md && git diff -M --stat 064ee85 HEAD -- CONTEXT.md GLOSSARY.md`
   mostra um rename com 0 linhas alteradas.
4. Ponta a ponta, o glossário do aicf é o arquivo que o Matt instalado procura:
   `grep -c 'GLOSSARY.md' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/domain-modeling/SKILL.md`
   devolve 10, e `grep -c 'CONTEXT.md'` no mesmo arquivo devolve 0; o template do setup passa a
   declarar o mesmo nome (passo 2).
5. `./scripts/check.sh` termina em `Tudo verde.`.
6. As notas da release `v0.36.0` trazem o `git mv CONTEXT.md GLOSSARY.md` e a troca da linha no
   `CLAUDE.md`: `gh release view v0.36.0 --json body -q .body | grep -c 'git mv CONTEXT.md GLOSSARY.md'`
   devolve 1.

**Verificação de comportamento em aberto:** o template só chega a um projeto pelo `/aicf:setup`,
que o agente não invoca. Encerra no primeiro setup real depois da `0.36.0`, com o `CLAUDE.md`
gerado dizendo `GLOSSARY.md`, ou no projeto privado de origem, quando a migração da nota da release
for aplicada e o `grill-with-docs` gravar um termo no `GLOSSARY.md` existente em vez de criar um
segundo arquivo.

## Origem

Levantado durante a entrevista de
[o usuário escolhe se a governança mora em arquivos ou em issues](../concluidas/escolher-entre-arquivos-e-issues.md),
como duplicação de layout ("o layout dos domain docs está declarado duas vezes"), e reaberto em
2026-10-06 pela troca de nome do Matt.
