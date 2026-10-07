# Revisão da implementação — O Matt renomeou o glossário

Data: 2026-10-06. Parecer consultivo sobre
[a demanda concluída](../../projeto/concluidas/o-matt-renomeou-o-glossario.md).
Base: `064ee85`; entrega revisada: `4a9ac45`. Diff: `git diff 064ee85...4a9ac45`.
Commits: `639e9cc` (spec), `fcff2da` (código e versão) e `4a9ac45` (fechamento).
Nenhum arquivo da implementação foi alterado.

## Standards

Nenhuma violação acionável encontrada. Consultados o `AGENTS.md` e o
`.claude/CLAUDE.md`. O eixo foi revisado por subagente independente.

A solução mantém um único nome de glossário, sem compatibilidade dupla ou lógica de
migração. Versão e entrada do changelog acompanham o código em `fcff2da`; o fechamento
fica separado. A tag `v0.36.0` aponta para `4a9ac45`, confirmado com
`git rev-parse 'v0.36.0^{commit}'`. As notas da release explicam a mudança e a migração
para quem usa o plugin, sem reproduzir o registro interno do changelog.

As referências históricas a `CONTEXT.md` foram preservadas. Nas duas demandas antigas
tocadas pelo fechamento, mudam apenas os ponteiros para o arquivo arquivado e a descrição
de seu estado. O caso do projeto privado aparece anonimizado na nova spec.

## Spec

Nenhum achado acionável encontrado. As dez linhas inventariadas nos nove arquivos de
skill, template e documentação passam a declarar `GLOSSARY.md`. O glossário do
repositório foi renomeado com conteúdo intacto. A versão é `0.36.0`, com entrada no
topo do changelog. O eixo foi revisado por outro subagente independente.

A release contém tanto `git mv CONTEXT.md GLOSSARY.md` quanto a instrução de trocar
o nome na linha **Glossário do domínio** do `CLAUDE.md`. Nenhuma skill ganhou migração
automática, aceitação dos dois nomes ou suporte a monorepo. As correções dos links de
arquivamento são parte do fechamento, sem expansão funcional do escopo.

## Validação e limites

Os passos 1–5 foram conferidos em cópias temporárias obtidas por `git archive` dos
commits pinados, sem modificar o checkout. O HEAD local no início da revisão era
`09e33dd`, que acrescenta somente a regra de atuação do Codex ao `.claude/CLAUDE.md`.

| Passo da Verificação | Comando e resultado |
| --- | --- |
| 1 — nome antigo | `grep -rn 'CONTEXT.md' --include='*.md' skills/ .claude/CLAUDE.md README.md README.en.md docs/projeto/PRD.md` contou 10 linhas em `064ee85` e 0 em `4a9ac45`. |
| 2 — nome novo | `grep -rln 'GLOSSARY.md' --include='*.md' skills/ .claude/CLAUDE.md README.md README.en.md docs/projeto/PRD.md` contou 0 arquivos em `064ee85` e 9 em `4a9ac45`. |
| 3 — rename | `test -f GLOSSARY.md && ! test -e CONTEXT.md` passou na entrega; `git diff -M --stat 064ee85 4a9ac45 -- CONTEXT.md GLOSSARY.md` mostrou rename com 0 inserções e 0 remoções. |
| 4 — Matt instalado | Os dois `grep -c` no `~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/domain-modeling/SKILL.md` retornaram 10 para `GLOSSARY.md` e 0 para `CONTEXT.md`. O template declara o mesmo nome. |
| 5 — check | `./scripts/check.sh` em `4a9ac45` terminou em `Tudo verde.`, com saída 0. |
| 6 — release | `gh release view v0.36.0 --json body -q .body` foi lido integralmente; o filtro `grep -c 'git mv CONTEXT.md GLOSSARY.md'` retornou 1. A troca da linha do `CLAUDE.md` também consta no texto. |

O `grep` sem correspondência retorna código 1; nos passos que esperam zero ocorrências,
isso confirma a ausência, sem indicar falha na verificação. Os arquivos consultados existiam.

Saída do check da entrega, com Claude Code `2.1.292`:

```text
162 links conferidos, 0 quebrados
✔ Validation passed — manifestos
✔ Validation passed — skills
0.36.0 é a entrada do topo do changelog
Tudo verde.
```

`git diff --check 064ee85...4a9ac45` passou. O CI citado pelo relatório,
`37557297418`, teve `conclusion: success` em `fcff2da`. O CI do fechamento,
`37557368336`, também teve `conclusion: success` em `4a9ac45`, conferido com
`gh run view 37557368336 --json conclusion,headSha,url`.

A verificação de comportamento continua em aberto, conforme a spec e o relatório:
o titular a encerra no primeiro setup real com a versão nova, conferindo o `CLAUDE.md`
gerado, ou ao aplicar a migração e usar `grill-with-docs`, confirmando que o termo vai
para o `GLOSSARY.md` existente sem criar outro glossário. Não foi invocada skill de
setup nem simulado esse fluxo; a inspeção dos textos prova alinhamento dos nomes,
sem provar o comportamento de uma sessão real.

O fechamento foi aplicado somente ao parecer, respeitando a restrição do Codex.
Não há correção obrigatória nem conhecimento novo a promover fora deste diretório.
Nenhum push foi realizado; o envio do parecer e o CI correspondente ficam com o titular
ou o agente líder. O check do checkout com este parecer foi executado antes do commit.

Resultado: Standards — 0 achados; Spec — 0 achados. Sem correção obrigatória identificada;
permanece a verificação de comportamento prevista na demanda.
