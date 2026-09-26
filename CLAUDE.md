# AGENT — Projeto aicf

## O que é

Plugin de skills para Claude Code que cuida da governança e do planejamento macro de um projeto de software: PRD, roadmap e demandas versionadas, e o ciclo que leva cada demanda da ideia ao registro do que foi feito.

Este repositório é a fonte editável do plugin, publicado no marketplace `aicodingflow`.

## Lema

**Simplicidade e manutenibilidade acima de tudo.** Havendo trade-off entre a solução mais completa e a mais direta, escolher a direta — desde que entregue o resultado. Gatilho de revisão: dois mecanismos coexistindo, sincronização entre estados, ou abstração antecipando o futuro.

**Refatoração contínua:** trecho que ficou mais complexo com o tempo se simplifica antes de receber feature nova.

## Registro

**Memory é atalho do agente — quem precisa saber é o repositório.** Decisões, IDs, gotchas e lições vivem em `docs/`, no `CLAUDE.md` e no código. Memory pode sumir ou ficar desatualizada; validar contra o repositório antes de confiar.

**Exceção:** credenciais ficam em `.env` (não commitado) ou no gerenciador de senhas. Nunca no repositório, nunca em memory.

**Glossário do domínio** (`CONTEXT.md`) e **decisões difíceis de reverter** (ADR em `docs/adr/`, numerado e imutável) nascem quando houver o primeiro termo ambíguo ou a primeira decisão a registrar — o passo 3 do ritual de fechamento manda escrever nos dois.

**Afirmação verificável carrega o teste que a refuta.** Número em doc ou em mensagem de commit vem com o comando que o remede; afirmação de estado vem com a condição que a encerra. A forma está no passo 3 do `/aicf:fechar-demanda`. Escrito por causa de dois números errados na mesma mensagem de commit, em 2026-09-09. **Número tirado do histórico do git se pina num commit, não numa data** — "em 44 commits" virou 45 no dia seguinte; `git log --oneline <sha> | wc -l` reproduz para sempre.

**Verificação que quebra algo de propósito confirma que quebrou.** `sed -i` que não casa sai com 0 e não muda arquivo nenhum: o check roda no repositório intacto, fica verde, e a leitura de fora é "o check não pegou o defeito" — quando o que falhou foi o comando do teste. Vale para todo passo de verificação que edita para ver falhar: conferir o diff (`git diff --stat` não vazio) antes de acreditar na saída. Escrito por causa do passo 1 da Verificação de [nenhum teste acusa link morto](docs/projeto/concluidas/nenhum-teste-acusa-link-morto.md), em 2026-09-19, cujo `sed` apontava para um link que aquele arquivo não tinha.

**Afirmação sobre ferramenta de terceiro carrega o comando que a confere, no texto que a propõe.** Errar sobre o próprio repositório é barato; errar sobre a ferramenta de outra pessoa derruba o crédito da comparação inteira, e quem conhece aquela ferramenta descobre em dez segundos. Escrito por causa de duas frases erradas na mesma seção do `README.md`, em 2026-09-18: o Matt não força issue tracker (o setup dele oferece GitHub, GitLab ou markdown local em `.scratch/`, e outro tracker descrito em prosa) e o Superpowers não apaga o registro (remove a worktree; plano e design doc ficam commitados em `docs/superpowers/`). As duas sobreviveram a várias revisões porque ninguém tinha motivo para abrir o repositório do vizinho. **Carregar o comando não basta: ele se roda no clone do sha pinado antes de a frase ir para o arquivo.** A correção de 2026-09-18 já trazia o comando ao lado e ainda assim errou o tracker do Matt — ninguém o executou; consertada em 2026-09-20. O bloco de clone do [relatório de pesquisa](docs/referencias/governanca-nos-frameworks-vizinhos.md) monta os repositórios nos shas certos em poucos minutos. **E o comando que se roda é o que a frase cita, não um parente dele:** em 2026-09-20 uma mensagem de erro do `git push` cru foi atribuída ao `gh repo create --push` em quatro arquivos, com um teste ao lado que rodava — e provava — o `git push`. O `gh` valida antes de chamar a API e devolve outra mensagem, o que só aparece rodando o `gh`.

**Comando que um doc escreve se roda antes de o doc fechar.** A Verificação de uma spec, a condição que encerra um item de backlog e a medição numa mensagem de commit são afirmações sobre a saída de um comando; executá-lo é o que separa a condição de aceite do palpite. Escrito por causa da Verificação 4 de [a profundidade da pasta quebra os links](docs/projeto/concluidas/a-profundidade-da-pasta-quebra-os-links.md), em 2026-09-20: ela previa que um `grep` sobraria duas ocorrências e sobravam dezenas, o que a entrevista teria visto rodando o comando que estava escrevendo. É a segunda ocorrência — a correção sobre o tracker do Matt, dois dias antes, também trazia o comando sem executá-lo. **E o comando mira o trecho que muda, não o assunto:** na terceira ocorrência, em 2026-09-20, uma Verificação previa `grep -c 'Superpowers'` em 1 e eram 2, porque a segunda ocorrência da palavra era legítima e ficava; `grep -c 'Superpowers, Matt Pocock'` — a linha que de fato sai — devolve 1 e 0.

**Referência que o agente carrega leva a regra e o comando; a medição que os provou vai para o `CHANGELOG.md` ou para a spec.** Evidência é para quem mantém o plugin, e ninguém a relê em runtime: o `midia.md` carregou desde a `0.17.0` o exemplo em `denoland/deno` e o "4 de 6 rodadas" que já estavam na entrada da `0.17.0`. Escrito em 2026-09-19, na demanda [as skills carregam o que não vão usar](docs/projeto/concluidas/as-skills-carregam-o-que-nao-vao-usar.md).

**Skill com `disable-model-invocation: true` o agente não verifica — planejar isso desde a spec.** São `setup` e `criar-prd`; o harness recusa a invocação e também imitar o roteiro por fora. Mexer nelas entrega com a verificação de comportamento em aberto, e o relatório registra quem a encerra e como, em vez de prometer um teste que não vai acontecer. O que cada passada do `setup` prova, o que já passou e o que segue em aberto vivem em [verificacao-do-setup.md](docs/referencias/verificacao-do-setup.md) — a condição de aceite fica lá, não espalhada pelos relatórios.

**A skill que roda é a do início da sessão, não a do cache.** `/plugin update` no meio da conversa troca o disco e não recarrega o que já está em contexto: quem verifica comportamento de skill logo depois de atualizar testa a versão anterior sem perceber. **Reiniciar a sessão antes de verificar**, e conferir a versão no cabeçalho do comando (`cache/aicodingflow/aicf/<versão>/skills/<nome>`) antes de acreditar no resultado. Escrito em 2026-09-20: a passada que encerrou a verificação do `setup` começou na `0.20.0` e imprimiu o layout antigo; quem pegou foi o titular, reconhecendo a árvore velha.

**Exemplo vindo de projeto privado entra anonimizado.** Este repositório é público, e a lição nunca depende de qual projeto a produziu: *"num projeto privado que consome estas skills"* basta — sem nome de repositório, domínio de negócio ou caminho de arquivo de lá. Vale em qualquer mídia: doc, ADR, mensagem de commit, issue. Ao citar um caso de origem, `grep -rn '<nome-do-projeto>' --exclude-dir=.git .` antes de commitar, e o que ele achar vira a forma anônima.

**Passo citado por número é ponteiro, e ponteiro envelhece.** Renumerar um passo de skill quebra em silêncio quem cita o número de fora: na `0.16.0` foram quatro referências, uma delas no template que vai para o `CLAUDE.md` de todo projeto novo. Nenhum grep pelo assunto as pega — elas citam o número. Ao mexer na numeração, `grep -rn 'passo [0-9]' --include='*.md' .` antes de fechar.

**Critério mora na skill que o aplica.** Skill só entra no contexto quando invocada: a que diz "pelo critério do `/aicf:<outra>`" sem mandar carregá-la faz o agente aplicar o que não tem na frente. Ponteiro entre skills serve para o que o agente pode ir buscar, nunca para a regra do passo que ele está executando. Escrito em 2026-09-25, na demanda [os critérios moram longe de quem os usa](docs/projeto/concluidas/os-criterios-moram-longe-de-quem-os-usa.md), com duas ocorrências — workspace no `implementar-spec`, skill×hook no `fechar-demanda`. ``grep -rnE 'crit[ée]rio[^.]*`/aicf:' skills/*/SKILL.md`` acusa as duas em `780a386` e nenhuma depois; o padrão não enxerga a frase quebrada entre linhas.

**Este arquivo é lido inteiro em toda sessão.** O alvo que a documentação do Claude Code publica é abaixo de 200 linhas; regra que só vale para uma parte do código vai para `.claude/rules/<tema>.md` com `paths:` no frontmatter, e procedimento de vários passos vira skill. `/doctor` propõe cortes do que o agente já deduz do código.

## Processos de desenvolvimento

Duas camadas: a **governança** registra o que será feito e o que foi feito, e é sempre a mesma; a **implementação** é como o código sai, e tem caminhos à escolha. Uma demanda passa por quatro fases: demanda → entrevista → implementação → fechamento.

**O mapa do workflow está na skill `/aicf:workflow-demanda`** — ciclo, caminhos de cada fase e nomenclatura; invocar ao começar ou registrar uma demanda. **O fechamento — relatório e ritual — está em `/aicf:fechar-demanda`**, que o agente aplica ao concluir qualquer demanda, por qualquer caminho.

**Coleções de skills de workflow instaladas:** Superpowers, Matt Pocock. _(São os caminhos que o `implementar-spec` pode oferecer além do aicf.)_

**Mídia do registro:** arquivos em `docs/projeto/`

Quatro regras valem antes de abrir qualquer doc:

- **Na entrevista, o caminho é pergunta ao usuário; na implementação, o agente segue a sugestão gravada na spec quando o caso é óbvio — caminho aicf direto e diff que cabe numa frase — e pergunta com opções nos demais.** O agente sugere pelo ponto forte que couber ao caso; a decisão é do usuário quando há escolha real.
- **O método escolhido fecha o código; a governança fecha a demanda.** Rodar o processo de implementação inteiro — inclusive o passo de integração que ele encadeia — e só então `/aicf:fechar-demanda`.
- **Bug de causa desconhecida** → depurar de forma sistemática antes de propor correção; se `systematic-debugging` (Superpowers) ou `/diagnosing-bugs` (Matt Pocock) estiverem instalados, usar.
- Operação que se repete vira **skill** em `.claude/skills/`, não improviso na hora.

## Verificação

Um comando só, antes de commitar: **`./scripts/check.sh`**. Saída saudável termina em `Tudo verde.` e sai com 0, depois de imprimir a versão do Claude Code usada, `N links conferidos, 0 quebrados` e os dois `✔ Validation passed`. Ele confere três coisas: link relativo de markdown que aponta para arquivo inexistente, o formato do plugin (`claude plugin validate --strict` nos manifestos de `.claude-plugin/` e no frontmatter das skills) e se a versão do `plugin.json` é a entrada **do topo** do `CHANGELOG.md`. O check de links não enxerga o que está dentro de bloco cercado ou de crase — link de exemplo é ilustração — e ignora `skills/setup/templates/**`, onde o link fala do projeto que vai receber a cópia: **link quebrado dentro de um template passa batido**, e isso encerra quando chegar ao projeto de um usuário.

Depois do push, conferir o run: `gh run list --workflow=ci.yml --limit 1` → `completed success`. O workflow chama o mesmo script, com uma versão pinada do Claude Code; quando o check local reprovar com uma versão mais nova que a do `.github/workflows/ci.yml`, subir o pin. Se um check falha, corrigir o repositório, não o script.

## Publicação

- **A versão e a entrada do `CHANGELOG.md` sobem juntas, no commit de código.** O bump do `.claude-plugin/plugin.json` viaja junto com a mudança que ele descreve, e o `./scripts/check.sh` confere os dois em par — separá-los deixaria o check vermelho em todo commit de release, que é a hora em que ele é rodado. O commit de fechamento ainda pode ajustar o texto da entrada, com o que o fechamento descobriu.
- **A release do GitHub fecha a versão:** `git tag -a vX.Y.Z <sha do HEAD>`, push da tag, e `gh release create vX.Y.Z --title "<título>" --notes-file <arquivo> --latest`. A tag aponta para o **HEAD**, não para o commit de código, para que o tarball leve o `CHANGELOG.md` e a doc da versão junto. `--target` com sha abreviado é recusado; criar a tag antes evita isso.
- **As notas da release são para quem usa o plugin; o `CHANGELOG.md` é para quem o desenvolve.** Não reaproveitar o texto de um no outro. Nome interno de demanda não diz nada de fora — "a entrada de quem chega" não parece falar de README —, e decisão de projeto (o que foi descartado, ADR, regra nova) não interessa a quem só quer saber o que mudou no comando dele. A release diz o que mudou no uso, como atualizar, e para.

## Git

- **`main`** — única branch. Não há `develop` aqui.
- Commitar direto na branch de trabalho por padrão; branch + PR só para mudança grande ou a pedido.
- O fechamento de uma demanda vai em commit próprio, separado do commit de código.
