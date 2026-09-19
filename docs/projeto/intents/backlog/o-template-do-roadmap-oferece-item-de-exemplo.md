# O template do roadmap entrega item de exemplo sob um cabeçalho que diz "decidido"

Processo — entrevista: a definir · implementação: a definir

> **Encerra quando** o `skills/setup/templates/roadmap.md` não tiver mais linha de exemplo dentro
> de `## Próximas` (`sed -n '/^## Próximas/,/^## /p' skills/setup/templates/roadmap.md | grep -c '^- \[ \]'`
> → `0`) — ou quando a entrevista concluir que o exemplo se paga, e este arquivo for para
> `specs/concluidas/` com o motivo.

## Problema

O template oferece duas linhas prontas sob `## Próximas`, cabeçalho cuja própria legenda diz
**"Decidido, ainda sem arquivo"**:

```
- [ ] Repositório, branch de trabalho e CI mínimo
- [ ] `PRD.md` preenchido
```

Quem recebe a cópia não tem como distinguir exemplo de decisão: o formato é idêntico ao de um item
real, e o cabeçalho afirma que o que está ali foi decidido. As outras seções do mesmo arquivo
marcam o exemplo com reticências (`> - ...` no Backlog), que é o contraste que falta aqui.

**Aconteceu neste repositório.** O `docs/projeto/ROADMAP.md` e o template nasceram no mesmo commit
(`git log --oneline --diff-filter=A -1 -- docs/projeto/ROADMAP.md skills/setup/templates/roadmap.md`
→ `a6276e7`), e os dois itens daqui eram, palavra por palavra, os dois de lá. A linha
`Repositório, branch de trabalho e CI mínimo` sobreviveu quatro versões como item decidido sem
nunca ter sido decidida — repositório e branch já existiam desde agosto —, e só caiu quando a
entrevista de [nenhum teste acusa link morto](../../specs/concluidas/nenhum-teste-acusa-link-morto.md)
foi atrás da origem dela. A outra linha (`PRD.md preenchido`) coincide com uma pendência real
daqui, o que torna o defeito ainda menos visível: metade do exemplo virou verdade por acaso.

## O que decidir na entrevista

- **Tirar, ou marcar como exemplo?** Seção vazia não ensina o formato do item; exemplo marcado
  (reticências, como no Backlog) ensina sem se passar por decisão. O custo de tirar é que a
  primeira linha que o usuário escrever não terá modelo ao lado.
- **Os outros templates têm o mesmo defeito?** `prd.md`, `claude-md.md`, `preferencias.md` e
  `readme.md` misturam legenda e conteúdo de exemplo; a pergunta é se em algum deles o exemplo
  também é indistinguível de decisão do projeto
  (`ls skills/setup/templates/`). O do PRD usa `>` para a legenda, que é o contraste que o roadmap
  não tem no `## Próximas`.
- **Isso vira regra do `.claude/rules/templates.md`?** Já existe uma regra de templates neste
  repositório; se a conclusão for "exemplo dentro de template carrega marca de exemplo", o lugar
  dela é lá, não numa correção pontual de um arquivo.

## Origem

Achado da entrevista de *nenhum teste acusa link morto*, em 2026-09-19, ao procurar de onde vinha
a linha de CI do roadmap. A spec registrou o achado e deixou explícito que corrigir o template
estava **fora do escopo** dela; o fechamento da demanda abriu este item.
