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

**Caminho**:
Quem conduz uma fase: o aicf, ou uma coleção de skills. Escolhe-se um por fase, e as escolhas
são independentes entre si.
_Evitar_: método, modo, fluxo

**Coleção de skills**:
Um conjunto de skills de terceiro que cuida da implementação: Superpowers, Matt Pocock. O aicf
convive com elas e não as substitui.
_Evitar_: framework, framework de desenvolvimento, método

**Governança**:
A camada do aicf: registra o que será feito e o que foi feito. É sempre a mesma, seja qual for o
caminho de cada fase.
_Evitar_: processo, metodologia, workflow

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
