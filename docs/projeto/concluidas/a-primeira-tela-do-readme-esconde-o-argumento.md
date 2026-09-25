# A primeira tela do README esconde o argumento

Processo — entrevista: criar-spec · implementação: aicf-direto

Roda **depois de** [a comparação com os vizinhos erra e ignora o GSD](../concluidas/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md): as duas mexem no `README.md`, e aquela corrige fatos que esta cita. Ambas concluídas em 2026-09-20, junto com
[o bullet do planejamento macro](../concluidas/o-wayfinder-do-matt-faz-o-planejamento-macro.md).

**A linha 7 mudou depois de `cc28b60`.** Aquela última demanda trocou "Elas começam numa ideia já
formulada" por "num pedido já recortado", porque o `wayfinder` do Matt começa antes da ideia estar
formulada (`git diff cc28b60..v0.21.0 -- README.md | grep 'pedido já recortado'`). O texto novo
proposto abaixo **substitui o bloco inteiro** e não repete a afirmação, então o ajuste é descartado
junto sem perda — não é preciso preservá-lo. As âncoras desta spec seguem válidas: o bloco continua
nas linhas 5 a 9, e `grep -n '^## O problema' README.md` continua devolvendo 43.

## Problema

Quem recebe o link do repositório de um colega lê a primeira tela em dez segundos. Hoje ela é o
título, o link para o inglês, a frase "Vinte specs bem escritas não respondem onde o projeto está" e
dois parágrafos de 124 palavras (`git show cc28b60:README.md | sed -n 5,9p | wc -w`) que gastam o
primeiro explicando o que as outras coleções fazem antes de dizer o que o aicf faz. Não há imagem.

As três dores que o aicf resolve, que são o argumento, só aparecem na linha 43
(`grep -n '^## O problema' README.md`), depois da instalação e do diagrama do ciclo. E o diferencial
que a [pesquisa de 2026-09-19](../../referencias/governanca-nos-frameworks-vizinhos.md) mostrou ser
único entre sete frameworks, governança que não é dona da implementação, está num `<details>` no fim
da página.

Um leitor que conhece Superpowers ou Matt Pocock precisa ver em uma tela: o que esses não fazem, o
que o aicf faz, e que ele não precisa trocar nada para usar.

## Solução

- [x] **A primeira tela vira imagem, três dores e uma frase de posição.** As linhas 5 a 9 do
      `README.md` (em `cc28b60`) dão lugar a este texto, sem frase de efeito, cada dor como afirmação
      completa:

      ```markdown
      ![A camada de governança do aicf sobre os caminhos de implementação](docs/assets/hero.svg)

      Superpowers, Matt Pocock, spec-kit: cuidam de **uma demanda por vez**, e cuidam bem. Três perguntas nenhum deles responde:

      - **Onde o projeto está?** Specs descrevem cada mudança, uma por uma. Nenhuma diz o que o produto é, para quem serve e o que ficou de fora por decisão.
      - **Por que decidimos não fazer aquilo?** A decisão e o motivo ficaram na conversa com o agente, e a conversa não é salva. Semanas depois a mesma discussão volta.
      - **O que saiu de fato?** Spec e plano foram escritos antes de executar. O que mudou no caminho só fica registrado se alguém escrever no fim.

      O aicf é a camada de cima: PRD, roadmap, demanda versionada e o relatório do que foi feito. Seis skills, por cima do caminho de implementação que você já usa, sem trocar nada.
      ```

      A afirmação sobre as três coleções tem o comando que a confere no relatório em
      `docs/referencias/` (tabela-resumo, critério 1).
- [x] **O diagrama nasce em `docs/assets/hero.svg`**, desenhado à mão, não gerado. Uma faixa
      larga em cima com "Governança" e, em texto menor, "PRD · roadmap · demanda · fechamento"; embaixo,
      três caixas lado a lado, "aicf", "Superpowers", "Matt Pocock", e uma linha de cada uma subindo
      até a faixa. Legenda curta abaixo das caixas: "entrevista e implementação, por qualquer caminho".
      Restrições: fundo próprio (retângulo arredondado em tom médio), para ler igual no tema claro e
      escuro do GitHub; fonte de sistema (`system-ui, sans-serif`), sem fonte externa; sem `<script>`,
      sem `<foreignObject>`; largura de 1200, altura de 400, `viewBox` definido para escalar em
      celular; texto em português. A pasta `docs/assets/` nasce com ele.
- [x] **A seção "O problema que isso resolve" encolhe.** Cada uma das três subseções fica só com o
      parágrafo que diz qual skill resolve e como; o parágrafo da dor sai, porque agora está no topo.
      Os títulos das subseções passam a casar com as três perguntas do topo.
- [x] **O `README.en.md` acompanha, seção por seção**, com a mesma imagem e o texto traduzido
      (`grep -c '^## ' README.md README.en.md` devolve o mesmo número).
- [x] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código, como manda a seção Publicação
      do `CLAUDE.md`.

## Arquivos e interfaces

- `README.md` — linhas 5 a 9 e a seção "O problema que isso resolve" (linhas 43 a 61 em `cc28b60`).
- `README.en.md` — os trechos equivalentes.
- `docs/assets/hero.svg` — novo.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump e entrada.

## Fora de escopo

- **Imagem gerada por IA como banner.** A entrevista decidiu tentar primeiro o SVG desenhado, que
  explica a arquitetura e entra no git como texto. Encerra quando o SVG estiver no README e o
  usuário disser se basta; se não bastar, vira demanda nova com o prompt que já foi rascunhado
  nesta sessão.
- **GSD e BMAD na primeira tela.** Eles têm a mesma camada, colada ao motor de execução deles; a
  explicação cabe na seção "Por que este", que a outra spec amplia. No topo ficam só os nomes que o
  leitor provavelmente já usa.
- **Badges, estrelas, contagem de downloads.** Não há métrica que mude a decisão de quem lê.
- **Trocar o mermaid do ciclo pelo SVG.** São figuras de coisas diferentes: o SVG mostra as camadas,
  o mermaid mostra as fases. Ficam os dois.
- **Reescrever o restante do README.** Da instalação para baixo só muda o que o encolhimento pede.

## Verificação

1. `sed -n 1,20p README.md` mostra, nesta ordem: título, link para o inglês, a imagem, a frase com
   os três nomes, as três dores em bullet e a frase de posição, tudo antes de `## Instalação`.
2. `grep -c 'docs/assets/hero.svg' README.md README.en.md` devolve 1 em cada, e
   `grep -c '<script\|<foreignObject\|@import\|http' docs/assets/hero.svg` devolve 0.
3. `grep -n '^### ' README.md | sed -n 1,3p` mostra as três subseções com os títulos das três
   perguntas, e nenhuma delas repete o texto do bullet do topo
   (`grep -c 'a conversa não é salva' README.md` → 1).
4. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois.
5. Abrir o repositório no GitHub no tema claro e no escuro: a imagem e o texto dela se leem nos
   dois. Esse passo é manual, e é o que encerra a demanda.
6. `./scripts/check.sh` termina em `Tudo verde.`.


## Relatório de implementação (2026-09-22)

**Status** — concluído. Em 2026-09-23 as duas condições que dependiam do usuário fecharam:

- **Verificação 5** (abrir o repositório no GitHub nos dois temas): o usuário confirmou que a
  imagem e o texto dela se leem nos dois. Antes do push, o equivalente local já tinha rodado: o
  `hero.svg` renderizado por Chrome headless sobre `#ffffff` e sobre `#0d1117`, lendo igual nos
  dois por causa do fundo próprio.
- **Fora de escopo, "Imagem gerada por IA como banner"**: o SVG não bastou, e virou demanda nova,
  como esta previa. A demanda foi
  [a abertura do README não tem marca](a-abertura-do-readme-nao-tem-marca.md), entregue na `0.27.0`.
  Nela o banner gerado por IA entrou **acima** do título e o `hero.svg` desceu para a seção "O
  problema que isso resolve" — os dois ficaram, em lugares diferentes.

**Arquivos alterados**

- `README.md` — o bloco das linhas 5 a 9 virou imagem, frase de posição e três bullets; a seção "O
  problema que isso resolve" perdeu o parágrafo da dor em cada subseção e os títulos viraram as três
  perguntas, na ordem dos bullets.
- `README.en.md` — os mesmos dois trechos, traduzidos. O aviso "Written in Portuguese" segue logo
  abaixo do bloco novo.
- `docs/assets/hero.svg` — novo, desenhado à mão, com o cabeçalho de contrato que o passo 3 do
  fechamento gerou. A pasta `docs/assets/` nasceu com ele.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.25.0`, no commit de código.

**Commits**

- `7fcb5dc` `docs(readme): a primeira tela carrega o argumento, com diagrama e as três perguntas`
- o commit deste fechamento

**Validação**

- `./scripts/check.sh` → `Tudo verde.`, com `120 links conferidos, 0 quebrados`, os dois
  `✔ Validation passed` e `0.25.0 é a entrada do topo do changelog`. Não há suíte de testes neste
  repositório; o check é a verificação inteira.
- Verificações 1, 3, 4 e 6 da spec rodadas com a saída conferida. A 3 devolve as três subseções nas
  linhas 49, 53 e 57, e `grep -c 'a conversa não é salva' README.md` devolve 1. A 4 devolve 6 e 6.
- Verificação 2 partida em dois comandos, pelo motivo em "Escopo efetivo".
- Revisão de código por subagente não foi pedida: a mudança é prosa mais um asset, e o asset foi
  conferido pelo render. Se o usuário quiser um par de olhos frescos no texto do topo, cabe agora.

**Escopo efetivo**

- **A Verificação 2 da spec era impossível de satisfazer.** Ela pedia
  `grep -c '<script\|<foreignObject\|@import\|http' docs/assets/hero.svg` → 0, mas todo SVG que o
  navegador desenha carrega `xmlns="http://www.w3.org/2000/svg"`; sem o atributo a imagem fica em
  branco. Virou dois checks: os proibidos literais em 0, e
  `grep -o 'https\?://[^"]*' docs/assets/hero.svg | sort -u` devolvendo só o namespace.
- **Dois dos três bullets do topo foram reescritos antes de entrar no arquivo**, com a decisão do
  usuário. O rascunho da spec dizia que o motivo de uma recusa "não fica escrito em lugar nenhum" e
  que o que mudou no caminho "só fica registrado se alguém escrever no fim" — as duas frases erram
  sobre ferramenta de terceiro, e a tabela-resumo do relatório de pesquisa já dizia isso: o Matt é
  "NÃO (com nota)" no critério 1 por causa do `.out-of-scope/`, e o spec-kit é **PARCIAL** no
  critério 4, não NÃO. O argumento do aicf não mudou; a redação apertou para o que a tabela sustenta
  sem nota — registro **por esforço, não por produto**, e spec e plano que ninguém atualiza.
- **Os três repositórios vizinhos foram clonados e os comandos rodados** antes de as frases irem
  para o arquivo, nos shas de
  [governanca-nos-frameworks-vizinhos.md](../../referencias/governanca-nos-frameworks-vizinhos.md).
  `github/spec-kit` tinha andado para `fdb0850`; `git checkout d4229c0` recuperou o estado
  pesquisado. As duas frases decisivas saíram literais do clone: `.out-of-scope/` guarda "persistent
  records of rejected feature requests", e o `converge` tem escrito
  "MUST NOT: modify `spec.md` or `plan.md` in any way".

**Promoção de conhecimento**

- **Um cabeçalho de contrato no `docs/assets/hero.svg`**, porque o `./scripts/check.sh` não olha
  para dentro do SVG e quem editar o arquivo daqui a seis meses não tem como saber que o `xmlns` é
  obrigatório nem por que o fundo existe.
- **Nada foi para o `CLAUDE.md`.** A lição desta demanda — uma Verificação de spec que ninguém
  rodou prometia o impossível — é a quarta ocorrência de uma regra que já está lá, "Comando que um
  doc escreve se roda antes de o doc fechar", cujo texto já cita a Verificação de uma spec pelo
  nome. Acrescentar a ocorrência alongaria um arquivo lido inteiro em toda sessão sem mudar o que o
  agente faz.
- **Um ajuste inline na intent [governanca-em-issues-neste-repo](../specs/governanca-em-issues-neste-repo.md).**
  O `git mv` desta demanda mexeu num número que ela afirma, e medir mostrou que os dois já estavam
  defasados desde 2026-09-18: 27 e 14 são hoje 69 e 13, pinados em `7fcb5dc` em vez de numa data.
  No mesmo parágrafo, *"nenhum teste acusa link de markdown morto neste repositório"* deixou de ser
  verdade com a [nenhum-teste-acusa-link-morto](../concluidas/nenhum-teste-acusa-link-morto.md): o
  `./scripts/check.sh` confere links relativos. A frase virou o que a rede de fato dá — ela acusa o
  que quebrou, não reescreve o que sobrou, e o custo de migração continua de pé.
- **Nenhuma demanda nova, nenhuma obsoleta**, fora a condição de "Imagem gerada por IA como banner"
  acima, que segue como o fora-de-escopo que a spec já escreveu.

**Lições**

- **A Verificação de uma spec pode proibir o que o formato exige.** Aqui o `grep` por `http` num SVG
  batia no namespace obrigatório — rodar o comando na hora de escrever a spec teria mostrado, porque
  um SVG de teste com o atributo devolve 1 e sem ele não abre. A defesa não é uma regra nova, é a que
  já existe: rodar antes de fechar o doc.
- **Documentação que cita o comando do check pode quebrar o check.** A primeira versão do cabeçalho
  do `hero.svg` soletrava os três tokens proibidos, e o `grep` passou a devolver 2 — o arquivo
  acusava a si mesmo. Custou um comando descobrir, porque o comando foi rodado.
- **Clonar o repositório do vizinho custa poucos minutos e muda a frase.** Duas das três frases do
  topo teriam saído mais fracas sem isso.
