# As referências ao projeto privado saem dos documentos commitados

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

Este repositório é público. Três documentos já commitados nomeavam pelo nome um repositório
**privado** do mantenedor, usado como caso de origem — e um deles expunha também o domínio de que
o projeto trata e o caminho de um ADR interno de lá.

Nenhum trazia dado sensível de negócio, mas todos revelavam que o repositório existe e como ele se
chama. A exposição era descuido isolado, não decisão: os documentos nasceram enquanto o caso ainda
estava fresco, e o nome entrou junto com a lição.

**A lição de cada documento independe de qual projeto a produziu.** As referências eram rasas —
nomeavam o repositório e um caminho —, então anonimizar não custa nada ao argumento de nenhum
deles.

Esta demanda saiu de um item da intent
[a governança deste repositório passa a viver em issues](../../intents/governanca-em-issues-neste-repo.md),
onde era pré-requisito de uma migração maior. É independente dela: vale com arquivos ou com
issues, e não espera a decisão sobre a mídia.

## Solução

Substituir cada citação nominal pela forma anônima já usada em
[o índice envelhece sem avisar](o-indice-envelhece-sem-avisar.md) e no
[ADR 0002](../../../adr/0002-conferencia-do-indice-por-inclusao.md) — *"num projeto privado que
consome estas skills"* —, preservando o que sustenta o argumento de cada documento.

| Arquivo | O que sai |
| --- | --- |
| `docs/projeto/specs/concluidas/orquestrar-o-framework-escolhido.md` | nome do repo, duas vezes |
| `docs/adr/0001-fronteira-de-fase.md` | nome do repo |
| `docs/projeto/specs/concluidas/excecao-de-idioma-no-dominio.md` | nome do repo, o domínio, o caminho de um ADR interno |

**O ADR é imutável, e a edição foi direta mesmo assim.** Anonimizar um nome próprio não altera
contexto, decisão, alternativas nem consequências — nada que um leitor futuro precise reconstruir
muda. Nota de revisão no fim seria a alternativa, mas nenhum ADR deste repositório tem esse padrão
hoje: o único registro de mudança em uso é o `Supersede` na linha de cabeçalho do
[0003](../../../adr/0003-um-item-um-lugar.md), que não se aplica a uma troca de nome.

## Fora de escopo

- **O resto da intent de origem.** A migração para issues depende de
  [escolher entre arquivos e issues](../escolher-entre-arquivos-e-issues.md) e continua aberta.
- **Os números de volume de trabalho** em `orquestrar-o-framework-escolhido.md` (16 tarefas,
  40 commits, 141 testes) e o detalhe de estado local não versionado. Sem o nome do repositório
  eles não identificam projeto nenhum, e são o que dá dimensão à falha que a spec relata —
  apagá-los custaria ao argumento, que é o teste desta demanda.
- **`hmaurus/skills`**, que aparece em `README.md`, `README.en.md`, `plugin.json` e nas duas
  specs: é este repositório, público por decisão.

## Verificação

```bash
# o nome do repositório privado não aparece em lugar nenhum (só o autor sabe o nome;
# substituir <repo-privado> e conferir que volta vazio)
grep -rn '<repo-privado>' --exclude-dir=.git .

# a forma anônima está nos três documentos — 4 linhas
grep -c 'projeto privado' docs/adr/0001-fronteira-de-fase.md \
  docs/projeto/specs/concluidas/excecao-de-idioma-no-dominio.md \
  docs/projeto/specs/concluidas/orquestrar-o-framework-escolhido.md   # 1, 2, 1

# a regra promovida está no CLAUDE.md
grep -n 'Exemplo vindo de projeto privado' CLAUDE.md

# a seção já não é pendência da intent de origem
grep -c 'Item obrigatório' docs/projeto/intents/governanca-em-issues-neste-repo.md   # 0
```

## Relatório de implementação (2026-09-15)

**Status:** concluído. Não há CI nem PR neste repositório; a validação foi local (abaixo).

**Causa raiz da contagem errada.** A intent dizia "Quatro documentos" e a tabela listava três. O
`grep` pelo nome do repositório em todo o repositório achou **cinco linhas em três arquivos** — a
tabela estava certa e o texto errado. Reproduz para sempre com
`git grep -n '<repo-privado>' 52f7a23`, o commit anterior a esta demanda. O texto nunca foi
corrigido porque a contagem em prosa não carregava o comando que a refuta: é o caso exato que a
regra *"afirmação verificável carrega o teste que a refuta"* existe para pegar. A seção saiu
inteira ao fim da demanda, então a correção do número foi absorvida em vez de escrita.

**Arquivos alterados**

- `docs/adr/0001-fronteira-de-fase.md` — no Contexto, o nome do repositório vira "num projeto
  privado que consome estas skills". Edição direta, sem nota, pela decisão registrada na Solução.
- `docs/projeto/specs/concluidas/excecao-de-idioma-no-dominio.md` — a linha `Processo` perde o
  nome da sessão de origem; a frase que apontava para o ADR interno daquele projeto passa a
  descrevê-lo ("um projeto privado de domínio regulado brasileiro, que registrou a escolha num ADR
  próprio de identificadores em português"), sem nome de repo, sem caminho.
- `docs/projeto/specs/concluidas/orquestrar-o-framework-escolhido.md` — as duas citações nominais
  viram "um projeto privado que consome estas skills" e "daquele projeto". Números de volume
  mantidos, pelo motivo em "Fora de escopo".
- `docs/projeto/intents/governanca-em-issues-neste-repo.md` — a seção `## Item obrigatório` sai
  (deixou de ser pendência dela), e a seção seguinte deixa de dizer que a regra "falta hoje",
  apontando para onde ela foi escrita.
- `CLAUDE.md` — a regra promovida, na seção `## Registro` (passo 3).
- `docs/projeto/specs/concluidas/anonimizar-as-referencias-ao-projeto-privado.md` — este arquivo,
  criado já no fechamento.

**Commits**

Um só, com código e fechamento juntos — a exceção que o ritual abre para tarefa pequena. O hash
não cabe no relatório que o próprio commit carrega; `git log --oneline --grep 'anonimiza as
referências'` o acha.

**Validação**

Os quatro comandos da seção `## Verificação`, com a saída esperada: o `grep` pelo nome do
repositório privado volta vazio em todo o repositório (`.git` excluído), a forma anônima aparece
nas quatro linhas previstas, a regra está no `CLAUDE.md` e a intent já não tem a seção.

**Não houve check de projeto nem revisão de código.** O repositório não tem `package.json` — não
há script de lint/format/typecheck nem suíte de testes para rodar, e a seção `## Verificação` do
`CLAUDE.md` continua sem comandos, à espera de código. O passo fica registrado como ausente em vez
de sumir em silêncio. A revisão de código também não se aplica: a mudança é substituição de nome
próprio em texto de documentação, abaixo do limiar que o ritual estabelece.

**Sem entrada no `CHANGELOG.md` e sem bump de versão.** Nenhuma skill foi tocada; o plugin
publicado não muda. É o mesmo tratamento do commit `52f7a23`, também docs-only de governança.

**Escopo efetivo.** Um arquivo além dos três previstos: o `CLAUDE.md`, pela promoção do passo 3.
Fechamento e código foram no mesmo commit — a exceção que o ritual abre para tarefa pequena, e a
demanda nasceu já no fechamento.

**Lição.** Sem regra escrita, a anonimização depende de o autor lembrar — e ele lembrou em uns
documentos e não em outros. O mesmo caso de origem produziu textos nomeados (`0001`,
`excecao-de-idioma`, `orquestrar-o-framework`) e textos anônimos (`0002`,
`o-indice-envelhece-sem-avisar`), sem que nada distinguisse os dois grupos além do momento da
escrita. É o que a promoção do passo 3 resolve: a forma anônima passa a ser o default escrito.
Corrigir depois é mais caro, porque a citação já está no histórico do git — este commit tira dos
arquivos, não do `git log`.

**O que este ritual gerou:** a regra da seção `## Registro` do
[`CLAUDE.md`](../../../../CLAUDE.md), *"Exemplo vindo de projeto privado entra anonimizado"*.
Nenhum ADR, skill ou doc de referência novo; nenhum item do `ROADMAP.md` nasceu ou ficou obsoleto.
