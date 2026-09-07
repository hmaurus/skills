# Exceção de idioma quando o domínio perde na tradução

Processo — entrevista: conversa na sessão do `mh-fin` (2026-09-06), onde a regra nasceu e foi
aplicada · implementação: aicf-direto.

## Problema

A seção `## Idioma` de `skills/setup/templates/preferencias.md` diz "código em inglês" sem
exceção. É o padrão certo para a maioria dos projetos, mas o público do aicf é dev brasileiro, e
domínio regulado brasileiro — fiscal, contábil, jurídico, bancário — é comum nesse público.

Nesses domínios os termos não têm equivalente honesto em inglês. "Competência" não é *accrual
basis*, que é jargão contábil anglo com outro recorte; "conta corrente" não é *checking account*;
"estorno" cobre o que em inglês são *refund*, *chargeback* e *reversal*. Nomear em inglês cria
uma camada de tradução entre a conversa e o código — e quando o projeto tem um `CONTEXT.md` em
português, essa camada é exatamente o que o glossário existe para evitar.

Hoje quem enfrenta isso decide por gosto, projeto a projeto, sem critério escrito. E decide de
novo no projeto seguinte.

O caso concreto que originou a demanda está em `hmaurus/mh-fin`:
`docs/adr/0001-identificadores-em-portugues.md`.

## Solução

Um parágrafo novo na seção `## Idioma` do template, que dá **o teste** — não a permissão.

A diferença importa: sem teste, "pode ser em português" vira licença para misturar por gosto.
Com teste, é uma pergunta refazível a cada projeto, e a maioria das respostas continua sendo
inglês.

Texto a acrescentar, depois do parágrafo que já existe sobre acentuação:

> **Exceção, quando o domínio perde na tradução.** Se o vocabulário do projeto é de um domínio
> regulado brasileiro — fiscal, contábil, jurídico, bancário —, nomear em inglês cria uma camada
> de tradução entre a conversa e o código: "competência" não é _accrual basis_, e "estorno" cobre
> o que em inglês são três coisas diferentes. Nesses casos o domínio é nomeado em português —
> entidades, tabelas, colunas, funções de regra de negócio, subcomandos de CLI —, **sem acento
> nem cedilha em identificador** (`transacao`, nunca `transação`: acento em nome de coluna
> estraga `grep` e quebra em terminal com encoding errado). Convenção de ecossistema segue em
> inglês sempre: `feat`/`fix`, scripts do `package.json`, variáveis de ambiente, `src`/`dist`.
> A decisão fica num ADR do projeto, com a fronteira entre o que é domínio e o que é ofício.

## Arquivos e interfaces

**A fonte editável é este repositório** (`hmaurus/skills`), não
`~/.claude/plugins/cache/aicodingflow/aicf/<versão>/`, que é cópia gerada e é sobrescrita no
próximo update.

| Arquivo                                    | Mudança                                        |
| ------------------------------------------ | ---------------------------------------------- |
| `skills/setup/templates/preferencias.md`   | O parágrafo acima, na seção `## Idioma`         |
| `.claude-plugin/plugin.json`               | `version`: `0.13.3` → `0.13.4`                  |
| `CHANGELOG.md`                             | Entrada `## 0.13.4 — <data>` no topo            |

A entrada do changelog segue a voz das anteriores: diz o que mudou e **por que a regra anterior
não bastava**, não só o que foi acrescentado.

## Fora de escopo

- **Perguntar sobre idioma na entrevista do `setup`.** O `setup` já faz três perguntas de
  ferramenta; uma quarta, sobre uma exceção que a maioria dos projetos não usa, cobra atenção de
  todo mundo para servir a poucos. Quem precisar encontra a regra no template que acabou de
  receber. Reabrir se aparecer relato de gente aplicando a exceção sem o ADR.
- **`templates/claude-md.md`.** A regra de idioma mora nos padrões de engenharia
  (`preferencias.md`), que é onde o usuário escolhe se ficam no global ou no projeto. Repetir no
  `CLAUDE.md` do template criaria duas fontes para a mesma regra.
- **Skill nova de modelagem de domínio.** O aicf não entra nesse terreno; `domain-modeling` do
  Matt Pocock já faz, e o `implementar-spec` já sabe oferecer as coleções instaladas.
- **Governança completa neste repositório.** Esta demanda cria `docs/projeto/specs/` porque
  precisava de um lugar para esta spec. PRD, checklist e `intents/` não vêm junto — se fizerem
  falta, `/aicf:setup` roda aqui depois, como demanda própria.

## Verificação

```bash
grep -n "Exceção, quando o domínio" skills/setup/templates/preferencias.md
grep -n '"version"' .claude-plugin/plugin.json      # tem que dizer 0.13.4
head -5 CHANGELOG.md                                 # entrada 0.13.4 no topo
grep -rn "0\.13\.3" --include="*.json" .             # tem que vir vazio
```

O teste que fecha o ciclo é rodar `/aicf:setup` num projeto novo e conferir que a seção
`## Idioma` que chega ao `CLAUDE.md` (ou ao global) já vem com a exceção e com a regra de não
usar acento em identificador.

Vale ler o parágrafo em voz alta antes de fechar: se ele soar como permissão em vez de teste, a
redação falhou — a maioria dos projetos deve continuar em inglês depois de aplicar a regra.

## Relatório de implementação (2026-09-06)

**Status:** concluído. Não há CI nem PR neste repositório; a validação foi local (abaixo).

**Arquivos alterados**

- `skills/setup/templates/preferencias.md` — o parágrafo da exceção entra na seção `## Idioma`, depois do parágrafo sobre acentuação, com o texto que a spec fixou.
- `.claude-plugin/plugin.json` — `version` de `0.13.3` para `0.13.4`.
- `CHANGELOG.md` — entrada `## 0.13.4 — 2026-09-06` no topo, na voz das anteriores: por que a regra sem ressalva não bastava, e por que o parágrafo é teste e não permissão.

**Commits**

- `435075b` — `feat(setup): 0.13.4 — exceção de idioma quando o domínio regulado perde na tradução`

**Validação**

Os quatro comandos da seção `## Verificação` da spec, todos com a saída esperada: o `grep` do parágrafo acha a linha 7 do template, `"version"` diz `0.13.4`, `head -5 CHANGELOG.md` mostra a entrada `0.13.4` no topo e o `grep -rn "0\.13\.3" --include="*.json" .` volta vazio.

**O check do projeto não existe.** O repositório não tem `package.json` nem `CLAUDE.md`, então não há script de lint/format/typecheck nem suíte de testes para rodar — o passo fica registrado como ausente em vez de sumir em silêncio. Também não houve revisão de código: a mudança é texto de template mais changelog e bump, abaixo do limiar que a skill de fechamento estabelece.

**Escopo efetivo.** Igual ao previsto — três arquivos, nenhum item da lista de fora de escopo tocado. O teste de leitura em voz alta que a spec pede foi feito: o parágrafo abre condicional ("Se o vocabulário do projeto é de um domínio regulado brasileiro") e fecha exigindo um ADR com a fronteira entre domínio e ofício, então lê como pergunta a responder, não como licença.

**Pendente, e é o teste que fecha o ciclo:** rodar `/aicf:setup` num projeto novo e conferir que a seção `## Idioma` que chega ao `CLAUDE.md` (ou ao global) já traz a exceção e a regra de não usar acento em identificador. Só dá para fazer depois que a versão `0.13.4` chegar ao cache do plugin, o que não acontece nesta sessão.
