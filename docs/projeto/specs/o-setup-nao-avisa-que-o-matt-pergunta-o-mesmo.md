# O `/aicf:setup` não avisa que o Matt Pocock faz a mesma pergunta

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (duas frases
em dois `SKILL.md`, sem decisão de abordagem em aberto)

## Problema

As duas coleções perguntam **onde o trabalho mora**, e guardam a resposta em arquivos diferentes: a
do aicf na linha `**Mídia do registro:**` do `CLAUDE.md`, a do Matt em `docs/agents/issue-tracker.md`.
As duas podem discordar, e isso é legítimo.

Quem roda o `/aicf:setup` com o Matt habilitado e ainda sem o `issue-tracker.md` escolhe a mídia sem
saber que o `/setup-matt-pocock-skills` vai perguntar a mesma coisa depois, do zero, sem olhar para o
`CLAUDE.md`. As duas respostas nascem independentes, e o custo aparece mais tarde: com o aicf em
arquivo e o Matt em `.scratch/`, uma entrevista pelo `to-spec` deixa a spec num lugar que o aicf não
lê e não adota.

**No modo arquivo, o aicf não suporta alinhamento.** O tracker local do Matt tem outra estrutura, não é
só outra pasta: `.scratch/<feature>/spec.md`, um arquivo por ticket em `issues/NN-<slug>.md` com
linha `Status:`, e o `map.md` do `/wayfinder` (`issue-tracker-local.md` do
`setup-matt-pocock-skills` 1.2.3, seção "Conventions"). Apontar o "Other" do Matt para
`docs/projeto/specs/` faria `to-tickets` e `/wayfinder` escreverem dentro da pasta de estados do
aicf, e isso é o modo misto que o `workflow-demanda` descarta. **No modo issue o alinhamento é
direto:** os dois em GitHub, e a adoção por `/aicf:criar-spec #<n>` fecha o ciclo.

Mesmo assim, o `workflow-demanda` promete um caso que o aicf não suporta: na tabela da entrevista, a linha do
Matt diz *"ou `specs/<nome>.md`, se o tracker configurado no setup apontar para lá"*.

### O que já está resolvido desde o intent

- **A ordem das perguntas.** A detecção de coleções roda antes da pergunta da mídia, e a linha do que
  foi detectado já abre o enunciado dela (`0.29.1`). O setup sabe se o Matt está habilitado na hora
  da escolha.
- **O `issue-tracker.md` já existente.** O setup lê o arquivo e propõe o default a partir dele (seção
  "A mídia do registro"). O aviso novo é para o caso em que ele ainda não existe.

## Restrição

**O aicf não escreve em configuração de coleção alheia** ([ADR 0004](../../adr/0004-midia-do-registro-e-config-propria.md):
ler para propor, nunca gravar). Esta demanda informa; não configura, e não oferece escrever o
`issue-tracker.md`.

## Solução

**1. `skills/setup/SKILL.md`, seção "A mídia do registro".** Quando a detecção achou o Matt
habilitado e `docs/agents/issue-tracker.md` **não existe**, a descrição (`description`) de cada opção
do `AskUserQuestion` ganha uma frase com a consequência para o Matt:

- **Arquivos** — *informa*: o `/setup-matt-pocock-skills` vai perguntar o mesmo, e em arquivo o Matt
  guarda o trabalho dele em `.scratch/`, separado de `docs/projeto/`.
- **Issues (GitHub)** — *instrui*: no setup do Matt, escolher GitHub, e os dois ficam nas mesmas
  issues.

O enunciado não cresce: a linha da detecção continua sendo o único acréscimo nele. A frase fica junto
da escolha a que se refere, e sem o Matt habilitado nada muda. Quando a opção issue não é oferecida
(sem `gh`, ou remote de outro provedor), só a frase do modo arquivo aparece.

**2. `skills/workflow-demanda/SKILL.md`, linha do Matt na tabela "Entrevista — produz a spec".** Tirar
a promessa de `specs/<nome>.md` e dizer o que acontece de fato: no modo issue, a issue é adotada por
`/aicf:criar-spec #<n>`; no modo arquivo, a spec do `to-spec` fica em `.scratch/` e o aicf não a
adota.

**3. `CHANGELOG.md` e `.claude-plugin/plugin.json`** sobem juntos (patch), no commit de código.

## Fora de escopo

- **Quem instala o Matt depois do setup.** Já há cobertura parcial: `criar-spec`, `implementar-spec`,
  `fechar-demanda` e `criar-prd` avisam uma vez quando o `issue-tracker.md` discorda da linha do
  `CLAUDE.md` (`grep -rln "issue-tracker.md" skills/ | wc -l` devolve 6: esses quatro, o setup e o
`workflow-demanda`). O aviso
  chega depois da escolha, mas chega. Não se sabe se o agente considera "arquivo" contra "local
  markdown" uma discordância, já que os dois são arquivos. Se isso aparecer num projeto real, vira
  item próprio.
- **Ensinar o "Other" do Matt apontando para `docs/projeto/specs/`.** Descartado na entrevista: é o
  modo misto (ver Problema). Uma descrição em prosa que divida os destinos (a spec do `to-spec` em
  `docs/projeto/specs/`, tickets e mapas em `.scratch/`) talvez funcione, mas depende de várias skills
  do Matt respeitarem a prosa, e ninguém testou. Ensinar isso seria o aicf mantendo documentação de
  configuração alheia.
- **Empurrar para o modo issue quem quer usar o `to-spec`.** O aviso na opção de issues já diz que
  ali os dois se alinham; o default continua arquivo.
- **Escrever o `issue-tracker.md` pelo usuário.** Fora pela Restrição, não por custo.

## Verificação

**Estática, pelo agente:**

```bash
grep -n 'scratch' skills/setup/SKILL.md                          # hoje 0 linhas; depois ≥ 1, na seção "A mídia do registro"
grep -c 'se o tracker configurado no setup apontar para lá' skills/workflow-demanda/SKILL.md   # hoje 1; depois 0
./scripts/check.sh                                               # termina em "Tudo verde."
```

**De comportamento, pelo titular.** O `setup` tem `disable-model-invocation: true`, e nenhum agente
consegue verificar. A demanda fecha com esta condição registrada em aberto em
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md), que é quem a encerra:

1. Diretório novo, sessão nova na versão desta demanda, **Matt Pocock habilitado** e sem
   `docs/agents/`. Rodar `/aicf:setup`.
2. No transcript, a chamada `AskUserQuestion` da mídia traz `.scratch/` na descrição da opção de
   arquivos e "GitHub" como instrução para o setup do Matt na opção de issues. O enunciado continua só
   com a linha da detecção e a pergunta:

   ```bash
   jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="AskUserQuestion")
     | .input.questions[] | .question, (.options[] | .label + " — " + .description)' <arquivo>.jsonl
   ```

3. Contraprova: passada com o Matt **desabilitado** não traz `.scratch/` em nenhuma descrição.

## Origem

Levantado em 2026-09-18, numa pergunta sobre o funcionamento atual: *"se no setup o usuário escolher
issue, isso já padroniza também para o Matt Pocock?"* A resposta é não, e a decisão de manter assim
foi confirmada na mesma conversa. A entrevista, em 2026-09-24, descobriu que o alinhamento só é suportado
no modo issue, e que a tabela do `workflow-demanda` prometia o outro.
