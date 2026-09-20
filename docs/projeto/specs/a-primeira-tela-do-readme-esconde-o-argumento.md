# A primeira tela do README esconde o argumento

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (prosa em dois READMEs e um SVG novo; texto e desenho já estão decididos aqui)

Roda **depois de** [a comparação com os vizinhos erra e ignora o GSD](concluidas/a-comparacao-com-os-vizinhos-erra-e-ignora-o-gsd.md): as duas mexem no `README.md`, e aquela corrige fatos que esta cita. Ambas concluídas em 2026-09-20, junto com
[o bullet do planejamento macro](concluidas/o-wayfinder-do-matt-faz-o-planejamento-macro.md).

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

- [ ] **A primeira tela vira imagem, três dores e uma frase de posição.** As linhas 5 a 9 do
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
- [ ] **O diagrama nasce em `docs/assets/hero.svg`**, desenhado à mão, não gerado. Uma faixa
      larga em cima com "Governança" e, em texto menor, "PRD · roadmap · demanda · fechamento"; embaixo,
      três caixas lado a lado, "aicf", "Superpowers", "Matt Pocock", e uma linha de cada uma subindo
      até a faixa. Legenda curta abaixo das caixas: "entrevista e implementação, por qualquer caminho".
      Restrições: fundo próprio (retângulo arredondado em tom médio), para ler igual no tema claro e
      escuro do GitHub; fonte de sistema (`system-ui, sans-serif`), sem fonte externa; sem `<script>`,
      sem `<foreignObject>`; largura de 1200, altura de 400, `viewBox` definido para escalar em
      celular; texto em português. A pasta `docs/assets/` nasce com ele.
- [ ] **A seção "O problema que isso resolve" encolhe.** Cada uma das três subseções fica só com o
      parágrafo que diz qual skill resolve e como; o parágrafo da dor sai, porque agora está no topo.
      Os títulos das subseções passam a casar com as três perguntas do topo.
- [ ] **O `README.en.md` acompanha, seção por seção**, com a mesma imagem e o texto traduzido
      (`grep -c '^## ' README.md README.en.md` devolve o mesmo número).
- [ ] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código, como manda a seção Publicação
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
