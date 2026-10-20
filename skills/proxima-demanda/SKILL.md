---
name: proxima-demanda
description: Sugere a próxima demanda a pegar, depois de ler o corpo de tudo o que está aberto, no registro e fora dele. Invocar quando o usuário pergunta qual a próxima demanda, o que fazer em seguida ou por onde continuar o projeto.
---

# Sugerir a próxima demanda

A sugestão vale o que se leu. **Ler o corpo de cada demanda aberta, não só o título:** prazo,
gatilho, bloqueio e "a decidir" moram no corpo, e o título não diz nenhum deles. A skill só lê e
sugere; o registro fica como está.

## 1. Ler o que está aberto

A linha `**Mídia do registro:**` do `CLAUDE.md` diz onde a demanda mora; sem linha, arquivo.

| O quê | Modo arquivo | Modo issue |
| --- | --- | --- |
| Pronta para implementar | `docs/projeto/specs/` | `gh issue list --state open --label aicf:spec` |
| Decidida | `docs/projeto/intents/` e `ROADMAP.md` → Próximas | `--label aicf:intent` |
| Incerta | `docs/projeto/backlog/` e `ROADMAP.md` → Backlog | `--label aicf:backlog` |
| Aberta por alguém de fora, sem triagem | `gh issue list --state open` | issue aberta sem label `aicf:*` |

No modo issue, o corpo se lê com `gh issue view <n>`. E, nos dois modos:

- **O `PRD.md`** — escopo, ordem e riscos do MVP: é a régua da prioridade. Demanda aberta que ele
  lista em Fora, ou Risco com data vencida, é régua defasada: a resposta avisa e sugere ao usuário
  `/aicf:prd` antes de seguir a ordem.
- **Trabalho começado fora do registro** — `git branch --no-merged`, `git worktree list`,
  `git stash list`, ticket aberto em `.scratch/*/issues/` (Matt Pocock), plano em
  `docs/superpowers/plans/` com tarefa sem marcar (Superpowers). Ticket cuja linha `**Spec:**`
  aponta para `concluidas/` é resíduo, não trabalho: a demanda fechou e o status do ticket ficou
  para trás.
- **O que o `CLAUDE.md` do projeto nomeie como fonte de trabalho além destas** — uma pasta de
  pareceres de revisão, por exemplo.

Feito quando cada fonte da lista foi lida ou constatada ausente no projeto, e o corpo de cada
demanda aberta foi lido.

## 2. Ordenar

Na ordem, o que passa à frente:

1. **O que já tem custo pago** — spec com `## Estado em andamento` (fechamento parcial) e
   trabalho começado fora do registro.
2. **Prazo escrito no corpo** e **condição de backlog que já disparou.** Condição com comando se
   confere rodando o comando; condição com data, contra a data de hoje.
3. **Spec pronta**, já entrevistada.
4. **O próximo bloco do PRD.**
5. As demais decididas.

Demanda cujo gatilho ainda não disparou fica de fora, mesmo decidida. Demanda que depende de
alguém além do agente — parecer, painel de terceiro, credencial — entra com o nome de quem
destrava.

## 3. Responder

- **Uma recomendação**, com o motivo citando o registro: arquivo, issue ou seção do PRD.
- **Até duas alternativas**, cada uma com a condição em que passaria à frente.
- **A pergunta que decide entre elas**, quando o registro não a responde.
- **O comando de entrada**: `/aicf:implementar-spec <spec>` para spec pronta; para intent ou
  linha do roadmap, o caminho de entrevista que a regra do `CLAUDE.md` sugere para o caso.

A escolha é do usuário.
