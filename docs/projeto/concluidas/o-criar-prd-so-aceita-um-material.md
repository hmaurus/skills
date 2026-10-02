# O criar-prd não cita pasta como material de partida

Processo — entrevista: criar-spec · implementação: aicf-direto

## Problema

O `/aicf:criar-prd` recebe um argumento, `[arquivo ou texto de contexto]`, e a seção *Material de
partida* diz o que fazer com cada um: caminho de arquivo se lê, texto é o próprio material. Pasta
não aparece. Quem chega com vários insumos numa pasta não vê, nem no `argument-hint` nem na skill,
que pode passá-la.

O contorno funciona: num projeto privado que consome estas skills, em 2026-09-30,
`/aicf:criar-prd Leia todos os arquivos de docs/insumos/ antes da primeira pergunta.` leu os quatro
insumos sem problema. A mudança é de contrato escrito, não de comportamento quebrado.

## Solução

Pasta passa a ser um dos tipos nomeados de material:

- `argument-hint` vira `"[arquivo, pasta ou texto de contexto]"`;
- a frase da seção *Material de partida* ganha o caso: se for pasta, ler os arquivos de texto
  dentro dela.

O resto da seção não muda: ler antes da primeira pergunta, mostrar o que o material responde por
seção, e o que ele afirma se confirma com o usuário.

## Arquivos e interfaces

- `skills/criar-prd/SKILL.md` — `argument-hint` e a seção *Material de partida*
- `.claude-plugin/plugin.json` — versão `0.35.1`
- `CHANGELOG.md` — entrada `0.35.1` no topo

## Fora de escopo

- **Vários materiais no mesmo argumento** (vários caminhos, ou caminho e texto misturados). O caso
  real coube numa pasta, e o contorno por texto segue funcionando para o que não couber.
- **Repositório remoto como tipo.** Exigiria `gh` para buscar; repositório local já é pasta.
- **Regras de leitura da pasta** — recursão, o que pular (binário, `node_modules`), limite de
  tamanho, perguntar antes de ler pasta grande. O contorno nunca precisou delas; entram se um caso
  real precisar.
- **Contradição entre materiais.** A regra existente (o que o material afirma se confirma com o
  usuário) já cobre.
- **Pasta convencional `docs/insumos/`** sugerida pelo setup ou pela skill. Nenhum caso pediu.
- **Argumento no `/aicf:criar-spec`.** O contexto de uma demanda vai para o intent, como decidido
  na `0.35.0`.

## Verificação

1. `grep -c 'arquivo, pasta ou texto' skills/criar-prd/SKILL.md` devolve 1 e
   `grep -ci 'se for pasta' skills/criar-prd/SKILL.md` devolve 1 — hoje os dois devolvem 0.
2. `./scripts/check.sh` termina em `Tudo verde.`.
3. **Comportamento em aberto:** a `criar-prd` tem `disable-model-invocation: true`, e o agente não
   a invoca. Encerra na primeira rodada real em que o titular passar uma pasta como argumento e o
   agente ler os arquivos dela antes da primeira pergunta.

## Relatório de implementação (2026-10-02)

- **Status** — concluído; CI run `37072913693` em `f49b236`, `completed success`
  (`gh run view 37072913693`).
- **Arquivos alterados**
  - `skills/criar-prd/SKILL.md` — `argument-hint` e o caso de pasta na seção *Material de partida*
  - `.claude-plugin/plugin.json` — `0.35.1`
  - `CHANGELOG.md` — entrada `0.35.1`
- **Commits**
  - `2858e9c` docs(projeto): spec do criar-prd com pasta como material de partida
  - `f49b236` feat(criar-prd): aceita pasta como material de partida
- **Validação** — `grep -c 'arquivo, pasta ou texto' skills/criar-prd/SKILL.md` → 1 e
  `grep -ci 'se for pasta' skills/criar-prd/SKILL.md` → 1 (os dois davam 0 em `2858e9c`);
  `./scripts/check.sh` → `Tudo verde.`. Sem revisão de código: a mudança é só texto.
  **Comportamento em aberto:** a `criar-prd` tem `disable-model-invocation: true`; encerra na
  primeira rodada real em que o titular passar uma pasta como argumento e o agente ler os arquivos
  dela antes da primeira pergunta.
- **Escopo efetivo** — o da spec. A intent pedia vários materiais misturados; a entrevista
  reduziu a nomear pasta, porque o contorno por texto nunca falhou e o incômodo era só a skill não
  citar o caso.
- **Lições** — a primeira versão da Verificação previa `grep -c 'pasta'` em 2, e a palavra já
  aparecia uma vez na skill ("inventar pasta"); trocada por `grep` do trecho que muda, como o
  `CLAUDE.md` já manda. Nada novo a promover.
