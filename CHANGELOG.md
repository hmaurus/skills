# Changelog

## 0.13.0 — 2026-09-01

- **`criar-spec` e `implementar-spec` passam a ser invocáveis pelo agente.** Sai o `disable-model-invocation: true` das duas. Com a flag, "me entreviste sobre X" e "pode implementar a spec" não carregavam a skill: a documentação diz que o Claude Code bloqueia a chamada e o agente deveria pedir que o usuário digitasse o comando, mas na prática ele fazia o trabalho como tarefa comum, sem a skill. A flag existia pelo critério "side effect ou timing", e o pedido explícito do usuário já resolve o timing — o `fechar-demanda`, que também escreve e commita, nunca a teve. Deixar cada projeto escolher não era opção: `skillOverrides` não afeta skill de plugin. Como a description agora conta para a auto-ativação, as duas passam a dizer **quando não** invocar — pergunta pontual, implementação em curso, tarefa sem spec. `criar-prd` e `setup` mantêm a flag: rodam uma vez ou raramente, e o comando digitado basta.
- **A decisão do caminho de implementação ganha dono e momento.** A regra de que o caminho era sempre pergunta ao usuário morava em três lugares e nenhuma skill estava carregada na hora em que se aplica — entre a spec pronta e a primeira skill de implementação —, então o agente deduzia e ninguém notava, porque a linha `Processo` só era completada no fechamento. Agora o `criar-spec` grava a sugestão ao lado de `a definir` (`sugestão: aicf-direto (motivo)`), porque a entrevista é quando o agente mais sabe sobre a demanda e o usuário a vê ao revisar a spec; o `implementar-spec` ganha o passo de decisão, depois de ler a spec e o código: segue a sugestão quando o caso é óbvio (caminho aicf direto e diff que cabe numa frase), pergunta com `AskUserQuestion` nos demais, para e passa o bastão se a resposta for outra coleção, e entra no plan mode se for `aicf-plan` — plano em sessão com plan mode desligado continua `aicf-direto`. O template do `CLAUDE.md` ganha a linha "Coleções de skills de workflow instaladas", de onde a pergunta tira as opções; e o `fechar-demanda` substitui `a definir · sugestão: ...` pelo caminho seguido, registrando no relatório se divergiu. A regra reescrita — entrevista é pergunta; implementação segue a sugestão no caso óbvio e é pergunta com opções nos demais — vale igual no `workflow-demanda`, no template do `CLAUDE.md` e nos READMEs.
- **"Nativo" vira "aicf".** A palavra queria dizer duas coisas: o caminho próprio do plugin (`nativo-direto`, `nativo-plan`) e ferramenta do Claude Code (plan mode, `/code-review`), às vezes a quatro linhas de distância. "Nativo" fica reservado ao que é do Claude Code; o caminho do plugin passa a ser **caminho aicf**, com os valores `aicf-direto` e `aicf-plan` na linha `Processo`. Demandas já arquivadas não são reescritas.
- **O template do `CLAUDE.md` ganha `## Verificação`**, no formato que o playbook da Anthropic publica: comando por comando, com o que conta como saída saudável, e "se um teste falha, corrigir o código, não o teste". O `fechar-demanda` lia "do `CLAUDE.md`" qual era o comando de check, mas o template não tinha seção para isso; agora o fechamento procura essa seção pelo nome, e o fallback (scripts do projeto, ou registrar a ausência) continua igual. A seção fica no `claude-md.md`, não no `preferencias.md`: o comando é do projeto, e o `preferencias.md` pode ir para o global.
- **O passo 4 do `fechar-demanda` fica completo.** A página `memory` lista quatro gatilhos para escrever no `CLAUDE.md`; a skill conhecia um (o erro pela segunda vez) e submetia o achado de revisão de código ao mesmo limiar, que a documentação não exige. Entram os dois que faltavam — achado de revisão que o agente deveria saber sobre este código, sem esperar a segunda vez, e contexto que um colega novo precisaria — e o destino que não existia em skill nenhuma: regra que só vale para uma parte do código vai para `.claude/rules/<tema>.md` com `paths:`, e carrega só quando o agente toca arquivo daquele padrão. O contrapeso ganha número: o alvo publicado é abaixo de 200 linhas por arquivo `CLAUDE.md`, e o template repete o alvo na seção "Registro".
- **O `implementar-spec` nomeia o subagente no passo 2.** "Ler o que já existe de parecido no repositório" é o ponto do plugin onde o padrão de falha _infinite exploration_ morde; a documentação tem gatilho nomeado para ele — investigação sai do contexto principal — e a skill passa a dizê-lo ali, e só ali. Nas demais fases vale a escolha livre do `workflow-demanda`.
- **O `setup` prova e aponta.** Ao terminar, pede que o usuário rode `/context` na próxima sessão e confira o `CLAUDE.md` em **Memory files** — o arquivo carrega no início da sessão, e a lista é a prova em vez da suposição. Em projeto que já tem código, sugere `/init` com `CLAUDE_CODE_NEW_INIT=1` para a parte do `CLAUDE.md` que se deduz do código (comandos, layout, convenções); o setup segue dono da governança. E o caso Windows sem Developer Mode deixa de "seguir sem `AGENTS.md`": a documentação indica o import `@AGENTS.md` no lugar do link, que preserva o objetivo de um arquivo com dois nomes.

## 0.12.0 — 2026-09-01

- **`intents/` e `specs/` substituem `demandas/`.** A pasta passa a dizer a maturidade do documento, não a certeza de fazer: `intents/<nome>.md` é a demanda decidida e ainda não entrevistada, `intents/backlog/` é o que ainda não se sabe se será feito, `specs/<nome>.md` é a spec pronta para implementar, `specs/concluidas/` é o arquivo morto. Antes, `demandas/<nome>.md` podia ser um parágrafo cru ou uma spec entrevistada, e só abrindo o arquivo dava para saber. A spec é o intent movido com `git mv` — mesmo nome, histórico junto —, e tudo termina em `specs/concluidas/`, inclusive o que a entrevista concluiu não fazer. "Demanda" continua sendo a unidade de trabalho; por isso `workflow-demanda` e `fechar-demanda` mantêm o nome. **Migração:** `git mv demandas/backlog intents/backlog`, `git mv demandas/concluidas specs/concluidas`, o que estava ativo em `demandas/` vai para `specs/`, e `intents/` nasce vazia.
- **A linha `Processo` ganha rótulos** — `Processo — entrevista: <skill> · implementação: <skill>` — e o valor é sempre escrito: `nenhuma` quando não houve entrevista, nome da skill nos outros casos (`criar-spec`, `nativo-direto`, `nativo-plan`, `brainstorming`, `to-spec`…). O formato antigo tinha duas leituras para a mesma forma: `Processo: nativo-direto` significava "sem entrevista" e `Processo: mattpocock` significava "pipeline completo", ambos sem seta. As demandas já arquivadas não são reescritas.
- **`implementar-spec` ganha as duas decisões que se tomam com o código à vista.** Planejar ou ir direto, com o critério que a documentação da Anthropic publica — se dá para descrever o diff em uma frase, não planeje; e, indo direto, dizer a frase antes de editar, que é o gate mais barato que existe. E avaliar se a mudança merece teste e se merece começar pelo teste que falha: correção de bug é o caso claro dos dois; texto e configuração não pedem nenhum; no meio, onde o projeto já testa, a mudança entra testada. Nenhuma das seis skills mencionava teste.
- **O check do `fechar-demanda` passa a incluir a suíte de testes**, quando existe. Só lint, format e typecheck deixavam o teste novo protegendo só a sessão em que nasceu.
- **`criar-spec` ganha o passo zero**: ler o que a demanda toca no repositório, se ainda não tiver lido nesta sessão — a cláusula que evita reler quando a sessão emendou de outra fase. A instrução existia, mas dentro do parágrafo sobre como formular perguntas.
- **Sai o `PLANO-<titulo>.md`.** Ele dizia quais demandas andam juntas, e o `CHECKLIST.md` já diz isso com um título de seção. Demanda grande demais para uma sessão é uma spec só, com as entregas em checkboxes no corpo e fechamento parcial entre sessões; demandas independentes que andam juntas são specs separadas agrupadas no checklist.
- **Sai a recomendação de escrever as diferenças do projeto num `CLAUDE.md` dentro de `docs/projeto/`.** `CLAUDE.md` de subpasta só entra no contexto quando o agente lê um arquivo daquela pasta, e registrar uma demanda nova não exige isso — a recomendação apontava para um lugar que carrega tarde demais, e a frase no `workflow-demanda` mandando procurar esse arquivo existia para compensar. O README passa a dizer o contrário: diferença vai no `CLAUDE.md` da raiz ou em `.claude/rules/`. **Se você seguiu a recomendação antiga, mova o conteúdo de `docs/projeto/CLAUDE.md` para a raiz.**
- A tabela de entrevista do `workflow-demanda` registra que o `brainstorming` do Superpowers só grava arquivo no caminho _architectural_ e que o projeto pode mandá-lo gravar direto em `specs/<nome>.md`; a linha do Matt Pocock ganha a mesma opção via tracker configurado no setup.

## 0.11.0 — 2026-08-30

- O passo 4 do `fechar-demanda` ganha **fonte, limiar e contrapeso**. Fonte: além do relatório, o agente relê os achados da revisão de código — o material com maior chance de virar regra útil (o caso de borda que faltou, a suposição que não se sustentava) vivia na sessão ou nos comentários do PR e evaporava no `/clear`. Limiar: a rota `CLAUDE.md` deixa de aceitar qualquer regra e passa a exigir que o erro tenha aparecido duas vezes, porque uma vez é caso isolado. Contrapeso: promover para o `CLAUDE.md` obriga a olhar o que de lá saiu de validade. Sem esses dois últimos, a skill produzia exatamente o padrão de falha que a documentação da Anthropic nomeia — o `CLAUDE.md` sobre-especificado, longo o bastante para o agente ignorar metade dele. Não havia limiar de entrada, teto de tamanho, nem saída.
- `workflow-demanda` ganha a outra metade da regra de trabalho recorrente. A seção dizia que procedimento repetido vira skill ou command e parava aí. Faltava a distinção: skill é conselho que o modelo pode não seguir, **hook** é script que roda sempre. Regra que precisa valer sem exceção — formatar após editar, barrar escrita em pasta protegida — escrita como linha de skill é regra que vai falhar em silêncio algum dia, e o critério é justamente esse, se a falha passaria despercebida.
- O passo 2 do `criar-spec` para de gravar o que ainda não aconteceu. Ele mandava perguntar o caminho de implementação e fechar a linha `Processo:` inteira, enquanto o passo 3 logo abaixo recomendava `/clear` — e dava o argumento que derruba o 2: se a spec deve bastar sozinha, a escolha do caminho pertence a quem vai lê-la, não a quem a escreveu. Agora a linha nasce como `<entrevista> → a definir` e o fechamento a completa, que é onde ela já mora. Perguntar continua certo no outro ramo do passo 3, quando a implementação emenda na mesma sessão.

## 0.10.1 — 2026-08-29

- O check do fechamento ganha default: o `CLAUDE.md` continua sendo a fonte de qual é o comando, mas na ausência dele o agente usa os scripts que o projeto expõe, e não havendo nenhum registra o fato no relatório. Antes a instrução era só "rodar o script de check do projeto" — sem `CLAUDE.md`, o agente adivinhava ou pulava calado. Skill precisa funcionar sozinha; o `CLAUDE.md` refina, não habilita.

## 0.10.0 — 2026-08-29

- Sai do `fechar-demanda` a instrução **"prompt para a próxima sessão"**. Ela mandava montar um bloco autocontido com contexto, escopo, fora de escopo, DoD, skills, checks e branch — e todos esses campos já moram no arquivo da demanda e no `CLAUDE.md` do projeto. O prompt era uma cópia manual dos dois, criando uma terceira fonte que diverge das outras: uma skill que existe para tirar o porquê da conversa terminava mandando exportar o repositório de volta para a conversa. Com o registro em dia, a retomada é `implementa a próxima demanda do checklist` numa sessão limpa; se isso não basta, o defeito está no checklist ou na demanda, e é lá que se corrige. Some junto a regra de cercar o bloco com `---`, que só existia para proteger o formato dele.
- Entra no lugar a seção **"Sessão que acaba antes da demanda"**, o caso que faltava: os cinco passos assumiam demanda concluída (mover para `concluidas/`, marcar `- [x]`) e não havia caminho para "parei no meio". Agora contexto no fim com demanda aberta também é fechamento, só que parcial — o arquivo fica em `demandas/`, o checklist não é marcado, e o que a sessão descobriu vai para `## Estado em andamento` no próprio doc. O critério do que entra ali: se a frase serve para qualquer demanda, ela é do `CLAUDE.md`.
- Dois disparos, com donos diferentes: quando o usuário sinaliza a parada, o agente registra sem perguntar — é execução de ritual, igual ao fechamento normal, e é o caso que hoje falha em silêncio (dá-se `/clear` e o estado evapora); quando é o agente que percebe o aperto, ele avisa e a decisão de continuar, compactar ou cortar é do usuário. Encerrar o trabalho por conta própria para registrar continua fora.
- `workflow-demanda` ganha a premissa de tamanho: **estas skills dizem o que o agente não teria como inferir e param aí**. Ausência de instrução é liberdade, não lacuna — o que a ferramenta nativa já faz bem e o que se decide melhor no caso concreto ficam com o agente. Serve como critério de edição: quanto mais a skill descreve, mais ela precisa ser reescrita a cada evolução do modelo.
- O gatilho do caso novo mora na **description** do `fechar-demanda`, não num template de `CLAUDE.md`. Regra de "quando invocar" colocada no template só chega a quem rodou o `/aicf:setup` nesta versão, e não acompanha upgrade do plugin — a description viaja com a skill. Dependência do `CLAUDE.md` continua legítima para o que só o projeto sabe (qual é o comando de check, qual é a branch); para gatilho, não.

## 0.9.2 — 2026-08-25

- O fim do `setup` e o template do PRD passam a apontar para `/aicf:criar-prd` em vez de mandar "preencher o `PRD.md`" na mão — texto anterior à skill, nunca atualizado. Como ela é manual (`disable-model-invocation`), só é descoberta se alguém apontar, e o setup é o lugar natural desse ponteiro.

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
