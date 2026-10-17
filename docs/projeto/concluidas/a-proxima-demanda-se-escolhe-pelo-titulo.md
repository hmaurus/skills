# A próxima demanda se escolhe pelo título

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

Num projeto privado, perguntado qual a próxima demanda, o agente leu o roadmap inteiro e só o
título das intents. A sugestão saiu sem dois fatos que moravam no corpo: uma intent com prazo
escrito ("antes do primeiro dado real do piloto") e itens dela que o agente fecha sem terceiro, e
outra mais barata de fazer antes de haver dado real. O titular perguntou se as intents tinham sido
lidas, e a sugestão mudou. Nenhuma skill do aicf cobria a pergunta "qual a próxima?".

## Solução

Skill nova, `skills/proxima-demanda/SKILL.md`, alcançável pelo agente: ler o corpo de tudo o que
está aberto, nas duas mídias, mais o `PRD.md` e o trabalho começado fora do registro; ordenar pelo
custo já pago, pelo prazo e pela condição disparada; responder com uma recomendação, até duas
alternativas, a pergunta que decide e o comando de entrada. Só lê: a escolha é do usuário.

## Relatório de implementação (2026-10-17)

- **Status** — concluído no repositório; publicação (push, tag `v0.39.0` e release) a pedido do
  titular.
- **Arquivos alterados**
  - `skills/proxima-demanda/SKILL.md` — a skill.
  - `.claude-plugin/plugin.json` — a skill na lista e a versão `0.39.0`; `CHANGELOG.md`, a entrada.
  - `skills/ajuda/SKILL.md`, `README.md`, `README.en.md` — uma menção cada.
- **Commits** — `3ade431` feat(proxima-demanda): skill que sugere a próxima demanda.
- **Validação** — `./scripts/check.sh` → `Tudo verde.`. Os comandos da seção 1 da skill rodaram
  no projeto privado antes do commit, e um deles mudou a skill: 27 tickets do Matt em `.scratch/`
  estavam `ready-for-agent`, todos de spec concluída — as três primeiras demandas, anteriores aos
  43 tickets `resolved` das três seguintes. Sem a regra do resíduo, a skill sugeriria trabalho já
  feito; com ela, ninguém precisa voltar para marcar ticket antigo.
  Comportamento da skill invocada: depende de o titular atualizar o plugin e abrir sessão nova;
  encerra no primeiro uso real que responda pela seção 3.
- **Escopo efetivo** — o previsto, mais a regra do ticket residual.
- **Promoção** — nada além da própria skill.
