# 0010 — O aicf escreve no tracker do Matt as regras do `implement-spec`

Data: 2026-10-24 · Status: aceita · Versão: `0.44.0` · **Amplia o [0008](0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md)**

## Decisão

Nos dois modos, arquivo e issue, a operação "Alinhar o tracker do Matt" acrescenta ao fim do
`docs/agents/issue-tracker.md` a seção `## Quando o /implement-spec roda`, com aceite e diff, e
confere o ponteiro que o setup do Matt grava na raiz (``See `docs/agents/issue-tracker.md`.``, na subseção
`### Issue tracker` da seção `## Agent skills` do `CLAUDE.md` ou do `AGENTS.md`). O 0008 continua valendo para as três frases
do modo arquivo; o que muda é que o modo issue deixa de não escrever nada, e a escrita deixa de
ser só troca de frase.

**O que a seção diz:** calcular a fronteira pelo que já entrou na branch de integração; rodar no
checkout principal, depois do merge, a verificação do ticket marcado com
`**Verificação no checkout principal:**`; e, só no markdown local, passar os tickets aos
subagentes por caminho absoluto e achar os tickets da spec pela linha `**Spec:**`.

**O comando que o aicf entrega** leva um sufixo que só aponta a seção:
`/implement-spec <spec> — antes de começar, ler docs/agents/issue-tracker.md, seção "Quando o /implement-spec roda"`.

## Por quê

A doc do Matt manda *"tell the orchestrator"* em dois casos — calcular a fronteira pela branch de
integração e rodar no checkout principal a verificação que depende de estado não versionado
(`grep -n 'Tell the orchestrator to track\|tell the orchestrator to run it' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/docs/engineering/implement-spec.md`
→ linhas 60 e 68). Dizer isso no argumento só alcança quem copia o comando que o aicf entregou: é
o erro que o 0008 desfez com o `/implement`. O tracker sobrevive ao `/clear` e chega também a quem
chama o Matt direto.

Nada no Matt manda o orquestrador abrir o tracker: o `implement-spec` só supõe que ele foi
fornecido (`sed -n 9p .../skills/engineering/implement-spec/SKILL.md`), e o `CLAUDE.md` carrega o
ponteiro, não o arquivo. A mesma cadeia já funcionou para o `to-tickets`, que diz a mesma frase
(linha 11): num projeto privado que consome estas skills, os tickets saíram com a linha
`**Spec:**`, que só existe no tracker. O sufixo torna a leitura garantida quando o aicf entrega o
comando; a conferência do ponteiro protege o elo da cadeia que o aicf alcança.

O sufixo aponta e não copia as regras, para que elas morem num lugar só.

## Consequências

- **Rodar `/setup-matt-pocock-skills` de novo regrava o tracker e apaga a seção**, como apaga a
  convenção do 0008; a próxima chamada da operação a repõe.
- **O `implement-spec` digitado sem o sufixo depende de o orquestrador abrir o tracker por conta
  própria.** Ninguém observou isso ainda; a verificação de uso real da `0.44.0` registra o que
  acontecer.
- **Reverter** é tirar a seção e a conferência das duas operações e copiar as regras no sufixo do
  `implementar-spec/matt.md`; os trackers já editados ficam com a seção, que não atrapalha o Matt.
