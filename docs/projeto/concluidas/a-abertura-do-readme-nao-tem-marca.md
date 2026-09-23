# A abertura do README não tem marca

Processo — entrevista: criar-spec · implementação: aicf-direto

**Roda depois de** [a revisão da escrita do README](../concluidas/a-prosa-do-readme-parece-escrita-por-ia.md), que reescreve o
texto dos dois arquivos. As duas mexem na abertura; fazer o banner antes obrigaria a refazer o
ajuste de texto depois.

## Problema

O `README.md` abre com o título em markdown e o diagrama `hero.svg`. Não há marca visual. Quem
chega pelo link não vê de quem é o projeto nem a que ele pertence.

Os três repositórios que o usuário citou como referência fazem diferente, e os três põem uma imagem
de identidade acima do título:

| Repositório | Arquivo | Tamanho | O que é |
| --- | --- | --- | --- |
| Fission-AI/openspec | `assets/openspec_bg.png` | 1128×191 | Faixa preta com o nome e a tagline. O README não tem nenhum `# ` |
| eyaltoledano/claude-task-master | `images/logo.png` | 800×201 | Logotipo horizontal sobre fundo preto, centralizado |
| mattpocock/skills | Cloudinary | 738×388, exibido a 369 | Logo, tagline e foto do autor. Duas versões, trocadas por `prefers-color-scheme` |

Conferir: `curl -sL https://raw.githubusercontent.com/<repo>/HEAD/README.md | head -14` nos três, e
`identify -format '%wx%h %b' <arquivo>` nas imagens.

O título atual também destoa. `# aicf — governança de projeto para desenvolver com agentes` usa
travessão, que nenhum dos três usa, e mistura o nome do comando com a descrição.

## Solução

- [x] **Um banner de 1200×190 abre os dois READMEs**, acima do `# `. Ele tem fundo próprio escuro,
      como o do openspec e o do task-master, para ler no tema claro e no escuro do GitHub sem
      precisar de duas versões por tema.

      Conteúdo do banner: o logo do AI Coding Flow, o nome `AI CODING FLOW` e a linha
      `Skills em português para engenharia de software com IA`. A cor da marca é `#F95C28`,
      amostrada do logo oficial
      (`curl -sL https://aicodingflow.com/images/aicodingflow-logos/aicodingflow-logo-icone-wide.png -o /tmp/l.png && convert /tmp/l.png -resize 50x50! -colors 5 -format %c histogram:info: | sort -rn | head -2`).

- [x] **A arte é gerada por IA e o logo é composto depois.** O gerador produz o fundo e a textura;
      o logo oficial, o nome e a linha de texto entram por cima, nítidos. Gerador de imagem não
      reproduz logo fiel nem tipografia legível. Usar a skill `mhtec:criar-imagem-ia-livre` para a
      parte gerada.

- [x] **O título vira `# AI Coding Flow Skills`**, nos dois arquivos, sem travessão. A string `aicf`
      sai do título e continua visível na seção Instalação (`/plugin install aicf@aicodingflow`) e
      em todos os nomes de comando.

- [x] **O `hero.svg` desce para a seção "O problema que isso resolve"**, no tamanho atual de
      1200×400, logo abaixo do `## `. Ele ilustra as três perguntas que abrem a seção. A primeira
      tela fica com uma imagem só.

- [x] **Nenhum parágrafo novo de texto.** A linha que abre o argumento já cita Superpowers, Matt
      Pocock e spec-kit, e a frase de posição logo abaixo dos bullets já diz o que o aicf faz. O
      único dado novo que o usuário quis na abertura, "em português", passa a ser dito pelo banner e
      pelo `alt` dele.

- [x] **Quatro arquivos de imagem**, com a mesma convenção de nome dos READMEs:
      `docs/assets/banner.png`, `banner.en.png`, `hero.svg` (já existe) e `hero.en.svg`. O
      `hero.en.svg` é o mesmo desenho com o texto traduzido. Cada PNG fica em 200 KB ou menos.

- [x] **Versão e `CHANGELOG.md` sobem juntos**, no commit de código.

## Arquivos e interfaces

- `README.md` — banner, título, e o `hero.svg` movido para a seção do problema.
- `README.en.md` — o mesmo, com `banner.en.png` e `hero.en.svg`.
- `docs/assets/banner.png` e `docs/assets/banner.en.png` — novos.
- `docs/assets/hero.en.svg` — novo. `docs/assets/hero.svg` não muda de conteúdo nem de nome.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump e entrada.

## Fora de escopo

- **Três frases que o usuário rascunhou na entrevista e que não entram.** Cada uma com o motivo:
  - *"os dois maiores frameworks de AI Coding"* — superlativo sobre ferramenta de terceiro, sem
    métrica que o sustente. A pesquisa em
    [governanca-nos-frameworks-vizinhos.md](../../referencias/governanca-nos-frameworks-vizinhos.md)
    comparou sete frameworks e não mediu tamanho.
  - *"as boas práticas recomendadas pela própria Anthropic"* — afirma endosso que não existe. As
    skills são do autor do plugin.
  - *"Governança de IA para Vibe Coding estruturado"* — é frase de efeito, que o usuário pediu para
    evitar em README. Além disso, a primeira linha do README do Matt Pocock é
    *"My agent skills that I use every day to do real engineering - not vibe coding"*
    (`curl -sL https://raw.githubusercontent.com/mattpocock/skills/HEAD/README.md | sed -n 15p`),
    e o nome dele aparece na mesma frase.
- **Mascote ou foto no banner.** O Matt usa a própria foto. Aqui o banner leva só logo e texto.
- **Hospedar as imagens em CDN.** O Matt usa Cloudinary. Aqui as imagens ficam no repositório, que é
  o mesmo argumento que o README usa a favor do modo arquivo: sobrevive ao `git clone` sem rede.
- **Duas versões do banner por tema do GitHub.** O fundo escuro próprio resolve, e é o que openspec
  e task-master fazem. Só vale rever se o fundo escuro ficar ruim no tema claro.
- **Badges.** Decidido na demanda anterior, e segue valendo.
- **Trocar o mermaid do ciclo.** Também da demanda anterior.
- **Redesenhar o `hero.svg` mais baixo.** Fazia sentido no layout com as duas imagens no topo, que
  foi descartado.

## Verificação

1. `sed -n 1,14p README.md` mostra, nesta ordem: o banner, `# AI Coding Flow Skills`, o link para o
   inglês, a frase com os três nomes, os três bullets e a frase de posição, antes de
   `## Instalação`. O mesmo em `README.en.md`.
2. Sem travessão no título: `grep -c '^# .*—' README.md README.en.md` devolve 0 nos dois.
3. Cada README aponta para o seu par de imagens:
   `grep -c 'docs/assets/banner.png' README.md` → 1, `grep -c 'docs/assets/banner.en.png' README.en.md` → 1,
   `grep -c 'docs/assets/hero.svg' README.md` → 1, `grep -c 'docs/assets/hero.en.svg' README.en.md` → 1.
4. O hero está na seção do problema e não na abertura:
   `sed -n '1,/^## Instalação/p' README.md | grep -c hero` → 0, e
   `awk '/^## O problema/,0' README.md | grep -c hero` → 1.
5. Peso dos PNG: `for f in docs/assets/banner*.png; do echo "$f $(wc -c < $f)"; done` — cada um em
   200000 ou menos.
6. O hero em inglês está traduzido: `grep -c 'Governança' docs/assets/hero.en.svg` devolve 0 e
   `grep -c 'Governance' docs/assets/hero.en.svg` devolve 1.
7. As três frases descartadas não entraram:
   `grep -ci 'maiores frameworks\|vibe coding\|recomendadas pela própria Anthropic' README.md README.en.md`
   devolve 0 nos dois.
8. `grep -c '^## ' README.md README.en.md` devolve o mesmo número nos dois.
9. `./scripts/check.sh` termina em `Tudo verde.`.
10. Abrir o repositório no GitHub no tema claro e no escuro. Passo manual, e é o que encerra a
    demanda.

## Relatório de implementação (2026-09-23)

**Status** — concluído. A Verificação 10 (abrir o GitHub nos dois temas) fechou em 2026-09-23: o
usuário abriu a página publicada e confirmou. Antes do push, o equivalente local já tinha rodado,
com o banner renderizado por Chrome headless sobre `#ffffff` e sobre `#0d1117`.

**Arquivos alterados**

- `docs/assets/banner.png` e `banner.en.png` — novos, 1200×190, 109 KB e 111 KB.
- `docs/assets/hero.en.svg` — novo, o mesmo desenho com o texto em inglês.
- `README.md` e `README.en.md` — banner no topo, título sem travessão, `hero` movido para a seção
  "O problema que isso resolve".
- `.gitignore` — `.tmp/`, onde a skill de geração de imagem trabalha.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.27.0`, no commit de código.

**Commits**

- `fc4067d` `docs(readme): a abertura ganha banner da marca, e o diagrama desce para a seção`
- o commit deste fechamento

**Validação**

As dez verificações da spec rodaram. Resultados:

| # | Comando | Saída |
| --- | --- | --- |
| 2 | `grep -c '^# .*—' README.md README.en.md` | 0 e 0 |
| 3 | `grep -c` de cada imagem no seu README | 1 em cada um dos quatro |
| 4 | `sed -n '1,/^## Instalação/p' README.md \| grep -c hero` | 0, e 1 dentro da seção |
| 5 | `wc -c < docs/assets/banner*.png` | 109036 e 111202, teto 200000 |
| 6 | `grep -c 'Governança\|Governance' docs/assets/hero.en.svg` | 0 e 2 |
| 7 | `grep -ci` das três frases descartadas | 0 nos dois |
| 8 | `grep -c '^## ' README.md README.en.md` | 6 e 6 |
| 9 | `./scripts/check.sh` | `Tudo verde.`, `133 links conferidos, 0 quebrados` |

A geração do fundo e a composição foram conferidas olhando a imagem, não só o comando: três
recortes do fundo foram renderizados lado a lado antes de escolher, e as duas rotas de compressão
foram comparadas visualmente.

Revisão de código por subagente não foi pedida. A mudança é imagem e prosa de abertura, e a revisão
que importava foi a do usuário, que aprovou o preview.

**Escopo efetivo**

- **A Verificação 1 dizia `sed -n 1,14p` para os dois READMEs, e no inglês o corte é na 17.** O
  `README.en.md` tem o aviso "Written in Portuguese" entre a abertura e a instalação, que o
  português não tem. A ordem dos elementos está certa nos dois; o número veio do arquivo em
  português.
- **O slogan em inglês não é a tradução literal.** "Skills em português para engenharia de software
  com IA" virou "Skills for AI software engineering, written in Portuguese". A ordem literal soa
  estranha em inglês, e esta versão casa com o aviso que fica logo abaixo no `README.en.md`.
- **`pngquant` no lugar da quantização do ImageMagick.** O ImageMagick com 192 cores chegava a
  56 KB, contra 109 KB do `pngquant`, mas fazia banding visível no gradiente escuro. Os dois foram
  gerados e comparados lado a lado antes da escolha.
- **`.gitignore` não estava na spec.** Foi acrescentado porque a skill de geração trabalha em
  `.tmp/`, e o diretório não estava ignorado.

**Promoção de conhecimento**

- **Um doc de referência novo:**
  [a-arte-do-repositorio.md](../../referencias/a-arte-do-repositorio.md), com a identidade visual
  (o logo oficial, a cor, de onde ela foi amostrada), a receita de composição que produziu os dois
  banners e as armadilhas pagas nesta demanda. Sem ele, a próxima pessoa a mexer numa imagem
  refaz a decisão de compressão e a de "IA gera o fundo, o logo entra por cima" do zero.
- **Nada foi para o `CLAUDE.md`.** A regra que valeria — imagem do repositório se confere olhando,
  não só rodando o comando — é caso particular de "comando que um doc escreve se roda antes de o
  doc fechar", que já está lá.

**Lições**

- **Gerador de imagem serve para o fundo, não para a marca.** A composição em duas etapas (IA para
  textura, ImageMagick para logo e texto) saiu certa na primeira rodada. Pedir o banner inteiro num
  prompt teria custado várias tentativas e ainda sairia com letra deformada.
- **Passar o logo como referência muda o resultado.** A onda laranja que o Gemini produziu ecoa a
  onda do logo oficial, e isso não estava no texto do prompt.
- **Compressão menor nem sempre é melhor.** Dois caminhos, 56 KB contra 109 KB, e o menor tinha
  banding. Os dois estavam dentro do teto, então o critério foi olhar.
