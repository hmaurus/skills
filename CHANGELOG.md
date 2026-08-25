# Changelog

## 0.9.1 — 2026-08-24

- A sugestão de `/clear` ao fim do `criar-spec` vira condicional: entrevista curta e demanda pequena podem emendar a implementação na mesma sessão; entrevista longa mantém a sugestão, porque a spec deve bastar sozinha — implementar pela memória da conversa esconde spec incompleta.

## 0.9.0 — 2026-08-24

- Nova arquitetura de carregamento: o corte agora é **por fase, não por tema**. A poda por escrita tinha esgotado o ganho — o custo restante era material de fim de sessão (fechamento, relatório, prompt da próxima sessão) viajando desde o turno 1, porque o `implementar-spec` mandava carregar o `workflow-demanda` inteiro logo no passo 2.
- Nasce **`fechar-demanda`** (model-invoked): os cinco passos, o relatório, a linha `Processo:` e o prompt para a próxima sessão saem do `workflow-demanda` para cá. Por ter description própria, o agente a dispara proativamente ao concluir qualquer demanda — inclusive nos caminhos Superpowers e Matt Pocock, que não passam pelo `implementar-spec`.
- `workflow-demanda` vira só o mapa (−41%): ciclo, tabelas de caminho, governança, trabalho recorrente e PLANOs — material de início e triagem, carregado quando é a hora dele. `implementar-spec` deixa de invocá-lo e passa a invocar `/aicf:fechar-demanda` ao final: a sessão de implementação começa com ~250 palavras e só recebe as ~700 do fechamento quando chega lá.
- Custo novo: uma description a mais sempre em contexto (a do `fechar-demanda`). Duplicações deliberadas de 1 linha: a regra do desvio de roteiro ecoa no `implementar-spec`, e o formato `Processo: <entrevista> → <implementação>` fica inline no `criar-spec` — carregar uma skill inteira para recuperar uma linha custa mais do que a repetição.

## 0.8.1 — 2026-08-24

- Segunda rodada de poda nas quatro skills de workflow (−6%, 18.216 → 17.141 chars), desta vez **entre arquivos**: cada regra passou a ter um dono único, e quem precisa dela aponta em vez de reexplicar. O `workflow-demanda` é dono da governança (estrutura, linha `Processo:`, fechamento, "o `CLAUDE.md` do projeto manda"); `criar-spec` e `implementar-spec` ficam só com a técnica da sua fase. O `implementar-spec` encolheu 22% — apontava para o ritual duas vezes no mesmo arquivo e reexplicava a forma do `Processo:` que já morava no `workflow-demanda`.
- Regra de 1 linha repetida ficou repetida de propósito ("rodar fora do plan mode", "perguntar onde gravar"): obrigar o agente a carregar outra skill inteira para recuperar duas linhas custa mais contexto do que economiza. Ponteiro é para bloco, não para frase.
- Os `description` do frontmatter — os únicos caracteres carregados em toda sessão — também encolheram, preservando os substantivos que disparam a auto-invocação do `workflow-demanda`.
- Verificação por inventário: 77 regras normativas extraídas antes da edição e conferidas uma a uma depois. Nenhuma removida.

## 0.8.0 — 2026-08-17

- `workflow-demanda` ganha a seção **O que esta skill não decide**: a governança é obrigatória, o resto é roteiro. Ferramenta do agente (subagente, plan mode, worktree, code review) é escolha livre em qualquer ponto, e sair do roteiro só exige dizer numa linha o que vai fazer e por quê. Existia o risco oposto — um conjunto de skills chamado "workflow" ser lido como trilho, e o agente perder a iniciativa que teria num prompt natural.
- O ritual de fechamento passa a **nomear as opções de revisão de código** (`/code-review`, subagente fresco, code review do harness) em vez de só "propor revisão": instrução sem alternativa nomeada cai na opção mais fraca, que é o agente reler o próprio diff na mesma sessão.
- As quatro skills encolhem 17% no total, sem perder regra. O maior ganho veio de duplicação: o `implementar-spec` mandava não presumir o ritual "pela memória desta skill" e em seguida repetia o ritual inteiro — agora aponta para o `workflow-demanda` e para. O check do projeto também morava em dois lugares e ficou só onde é executado.

## 0.7.1 — 2026-08-17

- Corrige duplicação entre os templates do `setup`: `## Validação` estava no `claude-md.md` **e** no `preferencias.md`, então o `CLAUDE.md` nascia com ela mesmo quando o usuário respondia que o global já cobre os padrões. Achado rodando o `setup` num projeto de verdade.
- O `CLAUDE.md` gerado passa a citar `CONTEXT.md` e `docs/adr/`, que o passo 4 do ritual de fechamento já mandava alimentar.

## 0.7.0 — 2026-08-17

- `setup` passa a criar um `README.md` simples (o que é, status, onde ficam as coisas) e o link simbólico `AGENTS.md -> CLAUDE.md`, para que agentes que leem `AGENTS.md` vejam o mesmo arquivo em vez de uma cópia que envelhece sozinha.

## 0.6.0 — 2026-08-17

- `criar-prd` — entrevista sobre o produto (problema, público, escopo, sucesso, riscos) e escreve o `PRD.md`. Roda de novo em modo revisão, porque o PRD é vivo. Fecha a lacuna que o kit tinha: ele cobria da demanda em diante, não do produto em diante.

## 0.5.0 — 2026-08-17

- A entrevista de ferramentas do `setup` cai de nove categorias para três — gerenciador de senhas, fonte de documentação de biblioteca, coleções de skills de workflow —, as únicas que mudam o comportamento do agente. O catálogo em `references/` sai, e as respostas passam a ser registradas onde já havia lugar, sem seção nova no `CLAUDE.md`.

## 0.4.0 — 2026-08-17

- `setup` passa a levantar **as ferramentas que o projeto usa** — gerenciador de senhas, hospedagem, banco, CI, e as demais conforme o caso — explicando para que cada categoria serve a quem ainda não usa nenhuma. O resultado vira a seção `## Stack e serviços` do `CLAUDE.md`, com o nome da variável de ambiente e nunca o valor. Catálogo em `skills/setup/references/ferramentas.md`.

## 0.3.0 — 2026-08-17

- `setup` passa a oferecer os **padrões de engenharia** (idioma, KISS/YAGNI, validação antes do commit, testes, acessibilidade, tratamento de credencial), perguntando se vão para o `CLAUDE.md` global da máquina ou o do projeto. O global nunca é sobrescrito: quando já existe, a skill mostra o que falta e propõe.

## 0.2.0 — 2026-08-17

- `setup` — cria a base de um projeto novo: `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz. Só invocável pelo usuário.
- README reposicionado: o plugin é a **camada de governança** que falta às coleções focadas na demanda individual, e funciona sozinho ou por cima delas.
- README em inglês.

## 0.1.0 — 2026-08-17

Primeira versão pública.

- `workflow-demanda` — o ciclo de uma demanda: quatro fases, os caminhos de cada uma (nativo, Superpowers, Matt Pocock), nomenclatura, formato do relatório e ritual de fechamento.
- `criar-spec` — a fase de entrevista no caminho nativo: interroga até não sobrar decisão em aberto e escreve a spec no repositório.
- `implementar-spec` — a fase de implementação no caminho nativo: lê a spec, implementa, verifica no projeto inteiro e conduz o fechamento.
