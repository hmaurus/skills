# 0005 — A documentação humana é um arquivo só

Data: 2026-09-18 · Status: aceita · Versão: `0.18.0`

## Decisão

**Não existe `MANUAL.md` nem `TUTORIAL.md` neste repositório.** A documentação que um humano lê é o
`README.md`, e o que é para quem já usa fica dentro dele, dobrado em `<details>` — nunca movido
para outro arquivo.

O detalhe profundo tem dois donos, e nenhum deles é um arquivo novo:

- **O manual em runtime é `/aicf:workflow-demanda`** — ciclo, caminhos de cada fase, convenções de
  governança e a mídia do registro. É a fonte da verdade, e é dela que o `/aicf:setup` compõe a
  despedida em linguagem comum, em vez de guardar texto próprio.
- **Cada skill se explica quando carrega**, e o `README.md` linka as que o leitor vai digitar.

## Por quê

O `MANUAL.md` que o intent desta demanda propunha teria o conteúdo do `/aicf:workflow-demanda`
(154 linhas, `wc -l < skills/workflow-demanda/SKILL.md`) escrito outra vez para humano. Dois
mecanismos guardando o mesmo estado é o gatilho de revisão do lema deste projeto, e cópia que
ninguém é obrigado a reler envelhece — foi o que custou [o índice envelhece sem
avisar](../projeto/concluidas/o-indice-envelhece-sem-avisar.md), e a rede que existia contra
isso saiu do método em [o `CHECKLIST.md` sai do
método](../projeto/concluidas/o-checklist-sai-do-metodo.md).

As duas coleções que este repositório cita resolvem a mesma pergunta do mesmo jeito. O repositório
do Matt Pocock cabe num `README.md` de 231 linhas, organizado por modo de falha do leitor, com o
avançado em `<details>` e o detalhe profundo nas próprias skills. O Superpowers também tem um
arquivo só, e separa apenas por variante de ambiente (`docs/README.kimi.md`,
`docs/README.opencode.md`). O `spec-kit` do GitHub é o contraexemplo, e separa por volume: um site
inteiro em GitHub Pages, com `installation`, `quickstart`, `guides/`, `reference/` e `concepts/`.
São seis skills aqui.

E o percurso guiado que falta a quem chega não é arquivo nenhum: é o próprio `/aicf:setup`, que a
partir da `0.18.0` se apresenta antes da primeira pergunta e apresenta o método ao terminar.

## Consequências

- **O `README.md` não pode crescer.** O que entrar tem que caber, e o que for para quem já usa
  dobra. A régua é o texto visível:
  `awk '/^<details/{d=1} /^<\/details>/{d=0;next} !d' README.md | wc -l` — 105 na `0.18.0`, contra
  115 antes dela.
- **Quem avalia o plugin sem instalar fica com menos detalhe** do que teria com um manual. Foi
  aceito: o `README.md` precisa fazer alguém decidir instalar, não substituir o uso.
- **Mudança de conceito custa duas edições**, porque o `README.en.md` acompanha o `README.md`
  inteiro, seção por seção. Também aceito, na entrevista desta demanda.
- **Reverter** significa criar o arquivo e decidir o que sai do `README.md` e do
  `/aicf:workflow-demanda` para dentro dele — o custo não é criar, é manter os três sincronizados,
  que é justamente o que esta decisão evita.
