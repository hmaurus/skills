# A prosa do README parece escrita por IA

Processo — entrevista: criar-spec · implementação: aicf-direto

**Roda antes de** [a abertura do README não tem marca](../concluidas/a-abertura-do-readme-nao-tem-marca.md), que
acrescenta banner e move o `hero.svg`. As duas mexem nos mesmos dois arquivos, e fazer o banner
primeiro obrigaria a refazer o ajuste de texto depois.

## Problema

O usuário lê o `README.md` e diz que o conteúdo técnico e a estrutura estão bons, mas o estilo
atrapalha. O texto está elaborado demais, com frases de efeito, metáforas e oposições, e por isso
parece gerado por IA em vez de escrito por um desenvolvedor.

As construções que ele listou, com exemplos do arquivo:

| Construção | Exemplo no `README.md` |
| --- | --- |
| Frase curta usada como slogan | "Porque não é a mesma pergunta." |
| Metáfora desnecessária | "o plano vive na sessão e morre com ela" |
| Palavra abstrata onde cabe descrição | "elas param no esforço" |
| "não é X, é Y" | "por esforço, não por produto" |
| Conclusão dramática no fim do parágrafo | "não sobra índice para envelhecer" |
| Frase que condensa três ou quatro ideias | "Três coisas ficam de fora, e nenhuma das duas declara que são problema de outra pessoa — elas param no esforço" |
| Travessão constante para criar aparte | 18 dentro de frase (`grep -v '^- \|^<summary\|^# \|^\|' README.md \| grep -o '—' \| wc -l`); os outros 18 são separador de item de lista, que fica |

Há também repetição da tese. A ideia de que o aicf é uma camada de governança acima dos métodos de
implementação aparece pelo menos quatro vezes, com formulações diferentes
(`grep -c 'camada' README.md`).

## Solução

- [x] **Reescrever a prosa dos dois READMEs** seguindo a ordem de prioridade que o usuário deu:
      clareza, objetividade, precisão técnica, facilidade de leitura e, só depois, estilo. O tom de
      referência é "Este projeto resolve X. Ele funciona assim. Estes são os arquivos criados. Este
      comando faz Y." Pode continuar informal; não pode ficar seco nem burocrático.

- [x] **Eliminar as sete construções da tabela acima**, sem trocar uma frase de efeito por outra.
      Onde a frase condensa várias ideias, separar. Onde há palavra abstrata, descrever o que
      acontece.

- [x] **Dizer a tese uma vez.** Depois que a camada de governança estiver explicada na abertura, as
      reformulações ao longo do documento saem.

- [x] **Encolher os `<details>`.** Os quatro somam mais de 40% do arquivo
      (`awk '/^<details>/,/^<\/details>/' README.md | wc -l`, contra `wc -l < README.md`). O usuário
      liberou cortar conteúdo, não só reescrever. Cada um se mantém, encolhe ou sai pelo critério de
      responder uma pergunta que o leitor realmente faz.

- [x] **`README.en.md` recebe o mesmo tratamento**, seção por seção. O texto em inglês tem o mesmo
      estilo e os mesmos problemas.

- [x] **Nenhuma informação técnica se perde.** Os fatos conferidos em fonte primária continuam no
      arquivo: `.out-of-scope/` do Matt, o `wayfinder`, os 72 comandos do GSD Core, o `uv` do BMAD,
      o link do ADR 0001 e as opções de tracker do setup do Matt.

- [x] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código.

## Arquivos e interfaces

- `README.md` — o arquivo inteiro.
- `README.en.md` — o arquivo inteiro.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump e entrada.

## Fora de escopo

- **O `CLAUDE.md` e o texto das skills.** Têm o mesmo estilo, mas o leitor é um agente, e densidade
  ali pode ser proposital. Fica para uma demanda própria, se o usuário quiser.
- **Mudar o título, acrescentar banner ou mover o `hero.svg`.** É a demanda
  [a abertura do README não tem marca](../concluidas/a-abertura-do-readme-nao-tem-marca.md), que roda depois.
- **Traduzir o `hero.svg`.** Também da demanda seguinte.
- **Mudar a estrutura de seções.** A ordem das seções `## ` está boa, segundo o usuário. Só o que
  está dentro delas muda.
- **Reescrever o `CHANGELOG.md` antigo.** É registro histórico, e não é lido por quem chega.

## Verificação

1. Nenhuma das frases citadas como exemplo sobra:
   `grep -cF 'Porque não é a mesma pergunta' README.md` → 0, e o mesmo para
   `'param no esforço'`, `'chega perto'`, `'morre com ela'`, `'troca velocidade por rastro'`,
   `'envelhecer'`, `'não como fila'`, `'A seção que mais se paga'`.
2. O travessão de aparte some, e o de item de lista fica:
   `grep -v '^- \|^<summary\|^# \|^|' README.md | grep -o '—' | wc -l` devolve 0, contra 18 antes
   (o mesmo comando em `git show HEAD:README.md`).
3. A tese aparece uma vez na abertura: `grep -c 'camada' README.md` devolve 2 ou menos.
4. Os fatos conferidos continuam lá: `grep -c 'out-of-scope' README.md` → 1,
   `grep -c 'wayfinder' README.md` → 2, `grep -c 'gsd-\*' README.md` → 1,
   `grep -c 'uv' README.md` → 1, e `./scripts/check.sh` confirma que o link do ADR 0001 resolve.
   O `converge` do spec-kit nunca esteve no README (está no `CHANGELOG.md` da `0.25.0`) e não entra
   agora.
5. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois, e as seções `## ` são as
   mesmas de antes: `diff <(grep '^## ' README.md) <(git show HEAD:README.md | grep '^## ')` não
   mostra diferença.
6. O arquivo encolheu em palavras: `wc -w < README.md` contra
   `git show HEAD:README.md | wc -w`. A contagem de linhas sobe, porque parágrafo com quatro ideias
   vira três parágrafos.
7. `./scripts/check.sh` termina em `Tudo verde.`.
8. O usuário lê os dois arquivos e diz se o estilo está certo. Passo manual, e é o que encerra a
   demanda.

## Relatório de implementação (2026-09-23)

**Status** — concluído. O usuário leu os dois arquivos e aprovou o estilo, que era a Verificação 8.

**Arquivos alterados**

- `README.md` — reescrito inteiro. Estrutura de seções intacta.
- `README.en.md` — o mesmo, em inglês.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.26.0`, no commit de código.

**Commits**

- `a45d897` `docs(readme): reescreve a prosa dos dois READMEs em tom direto`
- o commit deste fechamento

**Validação**

| Medida | `README.md` | `README.en.md` |
| --- | --- | --- |
| Travessão de aparte | 18 → 0 | 20 → 0 |
| Palavras | 2336 → 2152 | 2468 → 2224 |
| Repetição da tese | 4 → 1 | 4 → 1 |

O travessão de aparte se mede com
`grep -v '^- \|^<summary\|^# \|^|' <arquivo> | grep -o '—' | wc -l`, contra o mesmo comando em
`git show v0.25.0:<arquivo>`. As palavras, com `wc -w`. A repetição, com `grep -c 'camada'` e
`grep -c 'layer'`.

As oito frases citadas como exemplo saíram: `grep -cF` devolve 0 para cada uma. As seções `## ` são
as mesmas da `v0.25.0`
(`diff <(grep '^## ' README.md) <(git show v0.25.0:README.md | grep '^## ')` sem saída), e
`grep -c '^## '` devolve 6 nos dois arquivos. `./scripts/check.sh` termina em `Tudo verde.`, com
`129 links conferidos, 0 quebrados`.

Revisão de código por subagente não foi pedida. A mudança é prosa, e a revisão que importava foi a
do usuário, que é o leitor do arquivo.

**Escopo efetivo**

- **A entrevista começou por outra demanda.** A sessão estava entrevistando o banner do README
  quando o usuário mandou a crítica de estilo. O banner virou a spec
  [a abertura do README não tem marca](../concluidas/a-abertura-do-readme-nao-tem-marca.md), que roda depois
  desta, e esta demanda nasceu da crítica.
- **A calibragem de tom virou passo da entrevista.** Em vez de reescrever 176 linhas e descobrir no
  fim que o tom estava errado, a seção "Por que este, e não o Superpowers..." foi reescrita primeiro
  e mostrada sozinha. O usuário aprovou, e só então o resto do documento foi feito.
- **Duas verificações da spec mediam a coisa errada, e foram corrigidas durante a implementação.**
  A contagem de travessão pegava também o separador de item de lista, que é convenção de markdown e
  fica; passou a excluir linhas de lista, `<summary>`, título e tabela. E a lista de fatos a
  preservar incluía o `converge` do spec-kit, que nunca esteve no `README.md` — ele está no
  `CHANGELOG.md` da `0.25.0`. As duas foram achadas rodando os comandos.
- **Nenhum `<details>` foi cortado**, embora o usuário tenha liberado cortar conteúdo. O candidato
  era "Por que o PRD não passa pelo ciclo da demanda", mas nenhum ADR registra essa decisão
  (`grep -ln 'PRD' docs/adr/*.md` acha só dois, e nenhum é sobre isso), então cortá-lo perderia a
  informação. Os quatro `<details>` encolheram.

**Promoção de conhecimento**

- **A memória de estilo do agente foi reescrita.** Ela dizia só "não usar frase de efeito". Agora
  lista as sete construções que o usuário quer eliminar, a ordem de prioridade que ele deu
  (clareza, objetividade, precisão técnica, facilidade de leitura, e só então estilo) e o tom de
  referência. Memória é do agente; o que o repositório precisa saber já está aqui e no `CHANGELOG`.
- **Nada foi para o `CLAUDE.md`.** A regra de estilo vale para texto voltado a leitor humano, e o
  `CLAUDE.md` é lido por agente. Ele já manda "precisão, não metáfora" na seção de comunicação.
- **Uma demanda nova**, a do banner, gravada em `specs/` durante a mesma sessão.

**Lições**

- **Calibrar o tom numa seção antes de reescrever o arquivo inteiro.** O custo de errar em 176
  linhas é refazer 176 linhas. O custo de errar em 20 é refazer 20.
- **A crítica valia também para o que eu tinha escrito no dia anterior.** "Onde sobra registro, ele
  é do esforço que estava aberto, não do produto", da demanda
  [a primeira tela do README esconde o argumento](../concluidas/a-primeira-tela-do-readme-esconde-o-argumento.md),
  é o mesmo "não é X, é Y" que esta demanda tirou do resto do arquivo.
