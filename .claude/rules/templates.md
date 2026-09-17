---
paths:
  - "skills/setup/templates/**"
---

# Templates do setup

**Template não traz valor de configuração escrito por extenso.** O que outro passo da skill deve
preencher vai no marcador `\<...\>`, a mesma convenção do `\<NOME\>`.

A skill que copia o template manda, no mesmo parágrafo, "**não reescrever o template por conta
própria** — o que estiver marcado como a preencher fica marcado". Valor final e sem marcador é lido
como texto definitivo, e o passo que deveria trocá-lo não troca.

Na `0.17.0` isso quase saiu assim: a linha `**Mídia do registro:**` nasceu no `claude-md.md` com o
valor do modo arquivo escrito por extenso, cem linhas depois da pergunta que decide o valor. Setup
em modo issue criaria os labels, deixaria `docs/projeto/` só com o `PRD.md` — e copiaria a linha
dizendo "arquivos". Daí em diante toda skill leria a mídia errada, e só se descobriria na primeira
demanda. Achado por revisão de código, não pelo uso.

A conferência é ler o template inteiro procurando linha de configuração com valor decidido: se um
passo da skill pergunta o valor, o template não pode já tê-lo.
