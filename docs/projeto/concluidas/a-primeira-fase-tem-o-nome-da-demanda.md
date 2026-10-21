# A primeira fase tem o nome da demanda

Processo — entrevista: grill-with-docs · implementação: aicf-plan

## Problema

O `GLOSSARY.md` define **Demanda** como a unidade de trabalho e, no verbete **Fase**, usa a mesma
palavra para a primeira das quatro fases: "demanda, entrevista, implementação, fechamento". O
README repete no diagrama de "O ciclo" (`D[Demanda<br/>o que se quer, ainda cru]`), e a frase
"toda demanda passa pela fase demanda" não diz nada. Quem lê tende a preencher o vazio com os
estados — "a primeira fase não seria a intent?" —, misturando o que se faz com onde a demanda fica.

Os estados, por sua vez, têm dois conjuntos de nomes. As pastas, os labels e o glossário usam
backlog / intent / spec / concluída; as receitas de `midia/`, a `ajuda`, o `proxima-demanda`, o
`criar-spec` e o `fechar-demanda` chamam os mesmos estados de "Incerto", "Decidido" e "Pronta para
implementar".

Medido antes da mudança, sobre os arquivos vivos
(`V="README.md README.en.md GLOSSARY.md .claude/CLAUDE.md skills docs/projeto/PRD.md"`):

- fase com o nome da demanda:
  `grep -rnE 'demanda → entrevista|\*\*Demanda\*\* —|D\[Demanda|D\[Work item|\*\*Work item\*\* —|^\*\*Demanda\*\* \(' $V | wc -l` → 9;
- estado com o nome do critério:
  `grep -rnE '"pronta para implementar"|^\| (Incert|Decidid|Pronta)|^- \*\*(Incerto|Decidido|Pronta)|estado "decidido"' $V | wc -l` → 17.

## Solução

Duas palavras, duas coisas. **Fase** é o trabalho que se faz: **registro → entrevista →
implementação → fechamento**. **Estado** é onde a demanda fica: **backlog, intent, spec,
concluída** — a pasta em `docs/projeto/`, ou o label da issue. "Incerto" e "decidido" deixam de ser
nome de estado e viram o critério que separa backlog de intent: certeza, não urgência.

| Fase | Estado em que a demanda termina |
| --- | --- |
| Registro | backlog ou intent, pela certeza |
| Entrevista | spec |
| Implementação | continua spec — o código sai, o registro não muda |
| Fechamento | concluída |

O diagrama do README mostra cada fase com o estado em que termina, e a lista abaixo dele segue o
mesmo formato. Em inglês, a fase de registro é **Intake**.

O `GLOSSARY.md` já foi atualizado na entrevista: **Fase** com as quatro novas, **Registro** (a
fase, com "Em inglês, _intake_"), **Estado** e **Concluída** novos, e **Backlog**, **Intent** e
**Spec** redefinidos como estados.

## Arquivos e interfaces

- `GLOSSARY.md` — feito na entrevista; a implementação só confere.
- `README.md` — seção "O ciclo": diagrama e lista. A árvore de pastas (`specs/  # pronta para
  implementar`) e o parágrafo seguinte usam "pronta para implementar" como descrição, não como nome
  de estado, e ficam.
- `README.en.md` — o mesmo, com _Intake_ no lugar de _Work item_ na primeira fase.
- `.claude/CLAUDE.md` e `skills/setup/templates/claude-md.md` — a frase "Uma demanda passa por
  quatro fases: demanda → entrevista → …".
- `docs/projeto/PRD.md` — as duas ocorrências de "demanda → entrevista → implementação →
  fechamento" (linhas 33 e 69).
- `skills/ajuda/SKILL.md` — "O ciclo" (linha 19, a fase **Demanda**, e linha 24, o estado "pronta
  para implementar") e a lista dos quatro estados (linhas 72–74).
- `skills/midia/arquivo.md` e `skills/midia/issues.md` — a tabela "Os quatro estados": a primeira
  coluna passa a ser o nome do estado, e o critério vai para a descrição.
- `skills/proxima-demanda/SKILL.md` — a tabela do passo 1 (linhas 18–20).
- `skills/criar-spec/SKILL.md` (linhas 69 e 80) e `skills/fechar-demanda/SKILL.md` (linha 94) — o
  estado citado entre aspas como "pronta para implementar" passa a ser **spec**.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — bump e entrada, porque a mudança toca skills.

## Histórias

1. Como quem lê o README pela primeira vez, quero que a primeira fase tenha nome próprio, para não
   confundir a etapa com a unidade de trabalho.
2. Como quem lê o README, quero ver em que estado cada fase deixa a demanda, para ligar o ciclo às
   pastas que vou encontrar em `docs/projeto/`.
3. Como quem lê o README em inglês, quero a primeira fase com uma palavra que entendo de primeira
   (_Intake_), sem precisar do vocabulário do aicf.
4. Como agente que roda o `/aicf:criar-spec`, quero que a skill diga que a demanda muda para o
   estado **spec**, para usar o mesmo nome que a pasta e o label.
5. Como agente que roda o `/aicf:proxima-demanda`, quero a tabela de leitura com os nomes dos
   estados, para não traduzir "Decidida" em `intents/` de cabeça.
6. Como agente que registra uma ideia no meio de outra demanda, quero que "incerto" e "decidido"
   apareçam como critério, para decidir entre backlog e intent sem achar que são estados a mais.
7. Como quem cria um projeto novo pelo `/aicf:setup`, quero que o `CLAUDE.md` gerado já liste
   registro → entrevista → implementação → fechamento, para o projeto não nascer com o nome antigo.
8. Como quem implementa uma spec, **não** quero um estado novo de "em andamento": a demanda continua
   em spec durante a implementação.
9. Como quem lê o histórico, **não** quero que ADRs, demandas em `concluidas/` e entradas antigas do
   `CHANGELOG.md` sejam reescritas: elas registram o que valia na época.

## Decisões de implementação

- **A primeira fase se chama Registro**, e continuam quatro fases. Registro é gravar a demanda na
  mídia e decidir o estado pela certeza. Pode ser pulada: a ideia que vai direto à entrevista nasce
  como spec, como a entrevista também pode ser pulada (`entrevista: nenhuma`).
- **"Registro" e "registro de demandas" convivem.** A fase de registro é o que põe a demanda no
  registro de demandas; o verbo e o substantivo falam da mesma coisa.
- **Nomes canônicos dos estados: backlog, intent, spec, concluída.** "Pronta para implementar" pode
  seguir como descrição ("spec pronta para implementar"), nunca como nome do estado.
- **A implementação não muda o estado.** Sem pasta nem label de "em andamento".
- **Sem ADR.** Renomear uma fase é fácil de reverter e não surpreende quem lê depois; esta spec
  guarda o porquê.
- **O histórico não muda:** `docs/adr/`, `docs/projeto/concluidas/`, as entradas antigas do
  `CHANGELOG.md` e `docs/agente-codex/`.

## Testes

Não toca código. O ponto de teste é o `./scripts/check.sh` (links, manifesto, versão no
changelog, tamanho das skills), mais os dois `grep` da Verificação.

## Fora de escopo

- **Três fases, sem o registro** — o argumento era que o registro não tem caminho de terceiro; o
  fechamento também não tem e é fase. Trocaria "quatro" por "três" em meia dúzia de arquivos sem
  ganho de clareza.
- **Triagem como nome da fase** — descreve bem o que a fase faz, mas "triada" já aparece no README
  com outro sentido (issue de fora triada para `docs/projeto/`).
- **_Registration_ em inglês** — manteria a simetria com _registry_, mas lê como cadastro de
  usuário.
- **Diagrama com estados como caixas e fases como setas** — a implementação viraria uma seta de
  spec para spec.
- **Estado "em andamento"** — projeto solo raramente tem duas sessões na mesma demanda; um estado a
  mais é um movimento a mais para lembrar. Se o caso aparecer de verdade, vira outra demanda.

## Verificação

1. Os dois `grep` do Problema, com o mesmo `V`, devolvem **0**.
2. `grep -c 'registro → entrevista → implementação → fechamento' .claude/CLAUDE.md skills/setup/templates/claude-md.md docs/projeto/PRD.md`
   → 1, 1 e 2 (antes da mudança, 0 nos três).
3. `grep -c 'Intake' README.en.md` → 2, o nó do diagrama e o item da lista (antes, 0); e
   `grep -c 'Registro' README.md` → 3, os mesmos dois mais o item "Registro depois da execução" da seção
   "As skills", que já existia (antes, 1).
4. `./scripts/check.sh` termina em `Tudo verde.`.
5. A seção "O ciclo" renderizada no GitHub mostra o diagrama com as quatro fases e o estado de cada
   uma — conferência visual depois do push.

## Relatório de implementação (2026-10-21)

- **Status** — concluído. CI verde no commit de código (run `39537072080`,
  `gh run view 39537072080 --json conclusion --jq .conclusion` → `success`).
- **Arquivos alterados**
  - `GLOSSARY.md` — Fase, Registro, Estado e Concluída; Backlog, Intent e Spec como estados (no
    commit da spec, durante a entrevista).
  - `README.md` e `README.en.md` — "O ciclo": diagrama e lista com o estado em que cada fase deixa
    a demanda; _Intake_ em inglês.
  - `.claude/CLAUDE.md`, `skills/setup/templates/claude-md.md`, `docs/projeto/PRD.md` — a
    sequência registro → entrevista → implementação → fechamento.
  - `skills/midia/arquivo.md`, `skills/midia/issues.md`, `skills/ajuda/SKILL.md`,
    `skills/proxima-demanda/SKILL.md` — tabelas e lista de estados pelo nome, com o critério ao
    lado.
  - `skills/criar-spec/SKILL.md`, `skills/fechar-demanda/SKILL.md` — o estado citado passa a ser
    spec.
  - `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.43.0`.
- **Commits** — `47381f8` docs(projeto): spec de a primeira fase tem o nome da demanda;
  `7c79ad8` feat: 0.43.0 — a primeira fase se chama registro, e os estados têm um nome só.
- **Validação**
  - Os dois `grep` do Problema, com o mesmo `V`: 9 → 0 e 17 → 0.
  - `grep -c 'registro → entrevista → implementação → fechamento' .claude/CLAUDE.md skills/setup/templates/claude-md.md docs/projeto/PRD.md`
    → 1, 1, 2.
  - `grep -c 'Intake' README.en.md` → 2; `grep -c 'Registro' README.md` → 3.
  - `./scripts/check.sh` → `Tudo verde.`; `agy plugin validate` na cópia de
    [`harnesses.md`](../../referencias/harnesses.md) → `✔ Validation passed`.
  - Revisão de código não pedida: a mudança é troca de texto, sem lógica.
  - **Em aberto:** a conferência visual do mermaid renderizado no GitHub (passo 5 da Verificação)
    não foi feita pelo agente; encerra quando o titular abrir a seção "O ciclo" do README no
    GitHub e vir as quatro caixas. O comportamento da `ajuda`, que o agente não invoca, encerra no
    próximo uso real dela.
- **Escopo efetivo** — o previsto. O `GLOSSARY.md` mudou na entrevista, não na implementação.
- **Promoção** — nada a promover: as lições desta demanda (medir antes de escrever, o comando que
  a Verificação cita se roda) já estão no `CLAUDE.md`.
