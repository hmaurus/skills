# 0009 — O aicf integra Superpowers e Matt Pocock, em vez de se dizer agnóstico

Data: 2026-10-20 · Status: aceita · Versão: `0.42.0`

## Contexto

Até a `0.41.1`, o README, o PRD e as skills apresentavam o aicf como uma camada que funcionava
"por cima do caminho de implementação que você já usa" e "igual em qualquer caminho". Na prática,
cada coleção que o aicf oferece como caminho exigiu acoplamento próprio: o
[ADR 0008](0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md) escreve a convenção da spec no
tracker do Matt, e o `CLAUDE.md` tem regras específicas para o `brainstorming` (Superpowers) e para
o `grill-with-docs` (Matt). O que funciona bem é a integração com essas duas, e só com elas.

O nome da camada também atrapalhava. "Governança" tem usos consolidados em TI que não são este:
governança de TI, o `GOVERNANCE.md` de projeto open source e, principalmente, governança de IA e de
agentes (políticas, permissões, auditoria). E a palavra nomeava duas coisas no repositório: a
camada e o conjunto das demandas registradas.

## Decisão

**O aicf integra Superpowers e Matt Pocock, as duas maiores coleções de skills de engenharia no
GitHub, e acrescenta por cima a gestão de produto.** Outra coleção entra como caminho só quando
houver quem a exercite, com o acoplamento que ela pedir.

**A camada do aicf passa a se chamar gestão de produto**: PRD, roadmap, registro de demandas e
relatório. A outra camada é a engenharia de software. Quem conduz o ciclo de vida da demanda —
escolhe o caminho de cada fase e faz a passagem entre elas — é o aicf. O vocabulário completo está
no [`GLOSSARY.md`](../../GLOSSARY.md).

## Alternativas descartadas

- **Continuar agnóstico.** A promessa não se cumpre: quem chega com spec-kit, GSD ou BMAD não
  encontra integração, e manter o discurso obriga a escrever as regras das duas coleções como se
  fossem exemplos de um caso geral que não existe.
- **Integrar mais coleções agora.** Cada uma custa acoplamento e uma superfície a testar, e só as
  duas são usadas pelo autor. É o mesmo critério dos trackers no PRD: entra quando houver quem
  exercite.
- **Manter "governança" e só redefinir no glossário.** O leitor de fora não lê o glossário antes do
  README, e a `description` do plugin continuaria parecendo de ferramenta de compliance.

## Consequências

- O [ADR 0001](0001-fronteira-de-fase.md) continua valendo: a independência entre as fases é o
  que permite entrevistar por uma coleção e implementar pela outra, e é isso que o lema "escolha os
  dois" promete. O vocabulário dele e dos ADRs 0002 a 0008 fica como foi escrito — onde dizem
  "governança", leia-se gestão de produto (a camada) ou registro de demandas (o conjunto).
- Projetos que já usam o aicf continuam funcionando com o `CLAUDE.md` antigo: nenhuma skill procura
  a palavra nele. A atualização da prosa vai nas notas da release da `0.42.0`, e o caso entra na
  intent [o setup não serve a projeto já rodando](../projeto/intents/o-setup-nao-serve-a-projeto-ja-rodando.md).
- Reverter significaria reescrever README, PRD, manifestos, glossário e o vocabulário das skills e
  do template, e voltar a prometer o que não se testa.
