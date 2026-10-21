# aicf

Glossário do plugin. Vale para README, skills, PRD, demandas e ADRs. Quando dois nomes disputam a
mesma coisa, o canônico é o que está em negrito; os outros ficam em _Evitar_.

## Linguagem

**Demanda**:
A unidade de trabalho: algo que se quer no projeto, da ideia crua ao registro do que foi feito.
Existe num lugar só, como arquivo ou como issue.
_Evitar_: tarefa, feature, ticket, item

**Intent**:
Uma demanda decidida, ainda não entrevistada. Sabe-se que será feita; não se sabe como.
_Evitar_: ideia, rascunho, proposta

**Backlog**:
Onde espera a demanda que ainda não é certeza. O que a separa de intent é certeza, não urgência.
_Evitar_: wishlist, ideias futuras

**Spec**:
Uma demanda madura: a entrevista acabou e não sobrou decisão em aberto. É o que a implementação
consome.
_Evitar_: design doc, PRD, plano

**Fase**:
Uma das quatro etapas por que toda demanda passa: demanda, entrevista, implementação, fechamento.

**Ciclo de vida da demanda**:
O percurso de uma demanda pelas quatro fases, do registro ao fechamento. É o aicf que o conduz:
escolhe o caminho de cada fase e faz a passagem entre elas. Em inglês, _work item lifecycle_.
_Evitar_: ciclo de desenvolvimento (é o SDLC), ciclo de vida do produto (é mais amplo), fluxo de
demandas

**Caminho**:
Quem conduz uma fase: uma coleção de skills, ou o **caminho aicf**, mínimo, para quem não instalou
as coleções. Escolhe-se um por fase, e as escolhas são independentes entre si: diz-se "caminho de
entrevista" ou "caminho de implementação" conforme a fase.
_Evitar_: método, modo, fluxo, caminho mínimo (como nome)

**Coleção de skills**:
Um conjunto de skills de terceiro que conduz a engenharia de software: Superpowers ou Matt Pocock,
as duas que o aicf integra.
_Evitar_: framework, framework de desenvolvimento, método

**Harness**:
O agente que carrega e roda as skills: Claude Code, Antigravity, Codex, opencode. É **alvo**
quando o aicf é testado nele a cada versão (Claude Code, Antigravity), e **compatível** quando o
aicf evita quebrar nele mas não o testa (Codex, opencode).
_Evitar_: ferramenta, CLI

**Gestão de produto**:
A camada que o aicf acrescenta por cima da engenharia de software: o quê e o porquê do produto, e o
que saiu de fato. São o PRD, o roadmap, o registro de demandas e o relatório. Sem artigo quando é a
disciplina; "gestão do produto" quando se fala de um produto específico.
_Evitar_: governança, gestão de projeto, processo, metodologia

**Engenharia de software**:
A camada do como construir: as fases de entrevista e de implementação, cada uma conduzida por um
caminho.
_Evitar_: implementação (como nome da camada; é o nome de uma fase)

**Registro de demandas**:
O conjunto das demandas que o aicf acompanha num projeto, todas numa mesma mídia. Em inglês,
_work item registry_ — nome adotado pelo aicf, não termo consolidado da indústria.
_Evitar_: governança

**Mídia do registro**:
Onde a demanda mora no projeto: arquivos em `docs/projeto/` ou issues do GitHub. Escolha do
projeto, declarada uma vez.
_Evitar_: tracker, modo arquivo/modo issue (como nome da escolha)

**Fechamento**:
A fase que registra o que saiu de fato: relatório na própria demanda, arquivamento e promoção do
que se aprendeu. Não decide o destino do código; isso é da implementação.
_Evitar_: entrega, conclusão, encerramento

**Relatório**:
O texto do fechamento: o que foi feito e o que saiu diferente do planejado, gravado junto da
demanda.
_Evitar_: resumo, changelog, release notes

**PRD**:
O documento do produto: problema, público, proposta, escopo, modelo, sucesso e riscos. Não passa
pelo ciclo da demanda; é revisado quando uma decisão o contraria.
_Evitar_: visão, briefing, spec do produto
