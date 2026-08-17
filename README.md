# aicf — skills de workflow para Claude Code

Três skills que cobrem o ciclo de uma demanda: **entrevistar** até virar spec, **implementar** a partir dela, **fechar** com registro do que foi feito.

Não é framework nem metodologia nova. É o mínimo que faz um projeto tocado por agente não perder o rastro do que foi decidido e por quê.

## Instalação

```
/plugin marketplace add hmaurus/skills
/plugin install aicf@aicodingflow
```

Reinicie a sessão depois de instalar — skills carregam no início e não trocam a quente.

## As três skills

| Skill                     | Fase          | O que faz                                                                    |
| ------------------------- | ------------- | ---------------------------------------------------------------------------- |
| `/aicf:workflow-demanda`  | o mapa        | O ciclo inteiro, os caminhos de cada fase e as convenções de governança      |
| `/aicf:criar-spec`        | entrevista    | Interroga até não sobrar decisão em aberto, depois escreve a spec no repositório |
| `/aicf:implementar-spec`  | implementação | Lê a spec, implementa, verifica e conduz o fechamento até o registro          |

Comece por `/aicf:workflow-demanda` — as outras duas são as fases dele no caminho nativo.

## O problema que isso resolve

Sessão de agente é volátil. A conversa em que você decidiu **não** usar uma abordagem some no `/clear`, e três semanas depois alguém — humano ou agente — reabre a mesma discussão porque o motivo nunca foi escrito em lugar nenhum.

O ciclo aqui tem quatro fases:

1. **Demanda** — o que se quer, ainda cru
2. **Entrevista** — amadurece a demanda e produz a spec
3. **Implementação** — consome a spec
4. **Fechamento** — relatório do que foi feito **de fato**, com as divergências plano×entrega

O que amarra tudo é o registro: cada demanda vira um arquivo no repositório, e ao concluir ganha um relatório e vai para `concluidas/`. O porquê mora no repo, não na conversa.

## Caminhos, não trilho único

As fases 2 e 3 não estão presas a estas skills. Cada uma tem alternativas, e a escolha é do usuário — o agente sugere, não decide:

- **Entrevista** — `/aicf:criar-spec`, ou `brainstorming` ([Superpowers](https://github.com/obra/superpowers)), ou `grill-with-docs` + `to-spec` ([Matt Pocock](https://github.com/mattpocock/skills))
- **Implementação** — `/aicf:implementar-spec` (com ou sem plan mode), ou `writing-plans` + `subagent-driven-development`, ou `to-tickets` + `implement`

Dá para entrevistar por um caminho e implementar por outro. A demanda registra qual foi usado, numa linha `Processo:`.

## Convenções que as skills assumem

```
docs/projeto/
├── PRD.md             # o porquê do produto
├── CHECKLIST.md       # o que foi entregue e o que falta
└── demandas/
    ├── <demanda>.md
    ├── concluidas/
    └── backlog/
```

Seu projeto pode divergir disso — se houver um `CLAUDE.md` em `docs/projeto/`, ele manda.

## Sobre

Feito para o curso [Claude Code: Criador de Apps](https://aicodingflow.com/curso), do [AI Coding Flow](https://aicodingflow.com). Use à vontade, com ou sem o curso.

MIT.
