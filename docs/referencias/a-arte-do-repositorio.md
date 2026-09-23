# A arte do repositório

O que existe de imagem no `docs/assets/`, de onde vem a identidade visual, e como refazer ou editar
cada peça. Serve a quem for mexer num banner, num diagrama, ou acrescentar arte nova.

## As quatro peças

| Arquivo | Formato | Tamanho | Onde aparece |
| --- | --- | --- | --- |
| `banner.png` | PNG | 1200×190, 109 KB | topo do `README.md` |
| `banner.en.png` | PNG | 1200×190, 111 KB | topo do `README.en.md` |
| `hero.svg` | SVG | 1200×400, ~2 KB | seção "O problema que isso resolve" do `README.md` |
| `hero.en.svg` | SVG | 1200×400, ~2 KB | a mesma seção do `README.en.md` |

Conferir: `for f in docs/assets/*; do echo "$f $(identify -format '%wx%h' $f 2>/dev/null) $(wc -c < $f)"; done`

Os dois `hero` são desenhados à mão em SVG, e o contrato deles está num comentário no topo de cada
arquivo. Os dois `banner` são PNG compostos, e a receita está abaixo.

**Tudo tem fundo escuro próprio.** É o que faz a imagem ler igual no tema claro e no escuro do
GitHub sem precisar de duas versões por tema, que é o caminho que o
[Matt Pocock](https://github.com/mattpocock/skills) usa e que aqui não foi preciso. Antes de aceitar
qualquer arte nova, renderizar sobre `#ffffff` e sobre `#0d1117` e olhar as duas.

## A identidade

O logo oficial do AI Coding Flow fica no site, não neste repositório:

```bash
curl -sL https://aicodingflow.com/images/aicodingflow-logos/aicodingflow-logo-icone-wide.png -o /tmp/logo.png
```

Ele é um prompt de terminal desenhado: o `>`, uma onda, e o `_`. Vem em laranja sobre fundo branco,
1015×629. A cor da marca é **`#F95C28`**, amostrada do próprio arquivo:

```bash
convert /tmp/logo.png -resize 50x50! -colors 5 -format %c histogram:info: | sort -rn | head -2
```

Para compor sobre fundo escuro, o branco tem que sair:

```bash
convert /tmp/logo.png -fuzz 12% -transparent white -trim +repage /tmp/logo-t.png
```

## A receita do banner

**A IA gera só o fundo. O logo e o texto entram por cima.** Gerador de imagem deforma tipografia e
borra logo de marca; nenhum dos dois modelos é confiável nisso. A divisão em duas etapas acertou na
primeira rodada.

**1. O fundo**, com a skill `mhtec:criar-imagem-ia-livre` (Gemini Nano Banana Pro). Passar o logo
como `--reference` muda o resultado: a onda laranja que saiu ecoa a onda do logo, e isso não estava
no texto do prompt.

```bash
node --env-file=/home/mh/dev/aicodingflow/.env \
  /home/mh/dev/aicodingflow/src/templates/generate-hero.mjs \
  --prompt "Abstract wide background texture for a software project banner. Deep charcoal near-black surface, subtle fine grain. On the right third, a smooth flowing ribbon of vivid orange (#F95C28) sweeping like a wave, with soft gradient and gentle glow, fading into the dark. The left two thirds stay almost empty and very dark, clean negative space. Minimal, modern, technical mood. Absolutely no text, no letters, no words, no logo, no symbols, no icons." \
  --output ./.tmp/banner-bg.jpg --aspect 21:9 --size 2K --reference ./.tmp/logo-ref.png
```

**2. O recorte.** O `21:9` sai em 3168×1344, e a faixa é 6,3:1. Recortar uma fatia horizontal e
redimensionar. **Gerar três alturas e olhar antes de escolher** — a curva da onda muda muito de uma
para outra, e a do meio foi a que ficou boa:

```bash
for y in 300 500 700; do convert .tmp/banner-bg.jpg -crop 3168x502+0+$y +repage -resize 1200x190! .tmp/crop-$y.png; done
convert .tmp/crop-300.png .tmp/crop-500.png .tmp/crop-700.png -append .tmp/crops.png
```

**3. A composição**, com DejaVu Sans, que é a fonte que existe na máquina
(`convert -list font | grep -i dejavu`):

```bash
convert .tmp/crop-500.png \
  \( .tmp/logo-t.png -resize x74 \) -gravity NorthWest -geometry +60+58 -composite \
  -font DejaVu-Sans-Bold -pointsize 33 -kerning 3 -fill '#ffffff' \
  -annotate +215+90 'AI CODING FLOW' \
  -font DejaVu-Sans -pointsize 19 -kerning 0 -fill '#b9c1cc' \
  -annotate +215+126 '<a linha de descrição>' \
  .tmp/banner-v1.png
```

**4. A compressão.** O PNG cru sai em 315 KB. **Usar `pngquant`, não `-colors` do ImageMagick:**

```bash
pngquant --quality=70-95 --speed 1 --force --output .tmp/banner-pq.png .tmp/banner-v1.png
```

O `convert -colors 192` chega a 56 KB contra 109 KB do `pngquant`, mas faz banding visível no
gradiente escuro. Os dois foram gerados e comparados lado a lado; o menor era o pior. Gerar as duas
saídas e olhar, em vez de escolher pelo número.

## Armadilhas já pagas

- **Um SVG sem `xmlns` não desenha.** A Verificação de uma spec pediu zero ocorrências de `http` no
  `hero.svg`, mas `xmlns="http://www.w3.org/2000/svg"` é obrigatório: sem ele o navegador mostra
  a imagem em branco. O check virou dois comandos, e está no cabeçalho do arquivo.
- **Documentar o check pode quebrar o check.** A primeira versão do comentário no topo do
  `hero.svg` soletrava os tokens que o `grep` procura, e o arquivo passou a acusar a si mesmo. O
  comentário descreve as restrições em prosa, sem os literais.
- **O script do Gemini não recorta; o da OpenAI sim.** O `generate-hero.mjs` grava os bytes como
  vieram. O `gen-article-image-openai.mjs` recorta para 1920×1080 se `--width`/`--height` não forem
  passados. Se a arte vier a ser gerada pela OpenAI, passar os dois.
- **`.tmp/` é descartável e está no `.gitignore`.** É onde a skill de geração trabalha. Só o
  arquivo aprovado vai para `docs/assets/`.
