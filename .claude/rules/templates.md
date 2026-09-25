---
paths:
  - "skills/setup/templates/**"
---

# Templates do setup

**Template não afirma o que o projeto não decidiu.** O projeto recebe a cópia e lê cada linha como
dele; o que o template escreveu em forma de decisão vira decisão sem ninguém ter decidido. Duas
formas, cada uma com um caso já pago:

- **Valor de configuração** que outro passo da skill deve preencher vai no marcador `\<...\>`, a
  mesma convenção do `\<NOME\>`.
- **Conteúdo de exemplo** vai marcado como exemplo — `> - ...`, como no Backlog do `roadmap.md` —
  ou não vai.

A skill que copia o template manda, no mesmo parágrafo, "**não reescrever o template por conta
própria** — o que estiver marcado como a preencher fica marcado". Valor final e sem marcador é lido
como texto definitivo, e o passo que deveria trocá-lo não troca.

Na `0.17.0` isso quase saiu assim: a linha `**Mídia do registro:**` nasceu no `claude-md.md` com o
valor do modo arquivo escrito por extenso, cem linhas depois da pergunta que decide o valor. Setup
em modo issue criaria os labels, deixaria `docs/projeto/` só com o `PRD.md` — e copiaria a linha
dizendo "arquivos". Daí em diante toda skill leria a mídia errada, e só se descobriria na primeira
demanda. Achado por revisão de código, não pelo uso.

O exemplo sem marca foi pago de verdade. O `roadmap.md` trazia dois itens prontos sob `## Próximas`,
cuja legenda diz "Decidido, ainda sem arquivo", e o `ROADMAP.md` deste repositório nasceu com os
mesmos dois: um deles ficou quatro versões como decisão que ninguém tomou. Saíram na `0.29.2`, e a
seção ficou só com a legenda — a primeira linha real quem escreve é o `/aicf:criar-prd`.

A conferência é ler o template inteiro procurando **linha de configuração com valor decidido** — se
um passo da skill pergunta o valor, o template não pode já tê-lo — e **item em seção que o cabeçalho
declara decidida**.
