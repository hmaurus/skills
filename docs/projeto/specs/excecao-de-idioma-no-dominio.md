# Exceção de idioma quando o domínio perde na tradução

Processo — entrevista: conversa na sessão do `mh-fin` (2026-09-06), onde a regra nasceu e foi
aplicada · implementação: a definir · sugestão: caminho aicf direto — o diff cabe numa frase
(um parágrafo no template, bump de versão, entrada no changelog).

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
