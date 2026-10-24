# Revisão da spec — O caminho do Matt não oferece o implement-spec

Data: 2026-10-23. Parecer consultivo sobre a
[spec](../../projeto/concluidas/o-caminho-do-matt-nao-oferece-o-implement-spec.md), ainda sem commit.
Base: `3befd6eeda55667f2da356c893daebc6fbd40454`.
Identificação: `sha256sum docs/projeto/specs/o-caminho-do-matt-nao-oferece-o-implement-spec.md`
→ `eb3c07de2face65377c9f6ee229d60b8e72eaf7cf36566cb86aa72263952dde0`.

Resultado: seis achados P2 e dois P3. A proposta de manter um caminho do Matt,
escolher a forma depois dos tickets e carregar explicitamente o critério comum é
coerente. Antes de implementar, faltam contratos de retomada, acesso aos tickets,
verificação e fechamento que funcionem também fora da sessão que criou o grafo.
P2 significa correção necessária nos cenários descritos; P3, precisão documental.
Não foi identificado achado P1.

## 1. P2 — A passagem pelo contexto limpo perde parte do fluxo novo

**Local:** spec, linhas 70–97 e 144–147; `skills/implementar-spec/SKILL.md`,
linhas 31–34 e 65–70; `skills/criar-spec/SKILL.md`, linhas 98–104.

O único gatilho definido para medir o grafo é voltar do `/to-tickets` **na mesma
sessão**. A regra vigente manda o `implementar-spec` parar ao entregar o caminho
de uma coleção. Além disso, o `criar-spec` já admite limpar a sessão e invocar
`/to-tickets` diretamente, sem passar pelo `implementar-spec`. A spec altera no
`criar-spec` apenas a leitura do critério; não define como esses usuários chegam
à nova escolha depois de publicar os tickets.

Há ainda perda de uma instrução operacional: calcular a fronteira do GitHub pelos
tickets incorporados à branch de integração aparece só no aviso da conversa
(linhas 87–91). Em seguida vem `/clear` e apenas `/implement-spec <spec>`. O
orquestrador novo não recebe aquele aviso. O próprio Matt documenta que consultar
o estado aberto dos bloqueadores durante a execução pode impedir os dependentes
de começar.

**Consequência:** o fluxo continua oferecendo somente o caminho antigo em uma
retomada limpa, pode mandar publicar tickets novamente ao reiniciar o passo 3,
ou inicia o paralelo sem o remédio para a fronteira desatualizada. Avisar o titular
antes de limpar não equivale a instruir o orquestrador depois de limpar.

**Ajuste sugerido:** definir uma retomada explícita pelo alvo da demanda, que
detecte os tickets existentes e entre na medição sem repetir o `/to-tickets`.
Explicitar a exceção à parada da skill e anunciar essa retomada também na saída
do `criar-spec`. Gravar as instruções necessárias ao orquestrador em material
que ele lerá — spec, tickets ou notas apontadas no comando —, preservando a
autoria do usuário na invocação das skills do Matt.

**Contraprova de aceite:** criar tickets, limpar a sessão e retomar só com o alvo
da spec, nos modos arquivo e issue. Não devem nascer tickets duplicados; a forma
deve ser oferecida. No caso `A → B`, B deve começar depois do merge de A na
integração, mesmo com A ainda aberto no tracker. Conferência estática executada:

```bash
nl -ba skills/implementar-spec/SKILL.md | sed -n '24,79p'
nl -ba skills/criar-spec/SKILL.md | sed -n '85,104p'
sed -n '58,60p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/docs/engineering/implement-spec.md
```

## 2. P2 — Uma linha de bloqueio não altera a dependência nativa do GitHub

**Local:** spec, linhas 76–83; tracker instalado do Matt,
`skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md`, linha 42;
`skills/engineering/to-tickets/SKILL.md`, linha 63.

A correção de colisões e migrations é descrita como edição dos tickets, com
“uma linha de bloqueio entre eles”. Isso representa a aresta no modo arquivo.
No GitHub, o Matt exige a dependência nativa quando disponível; o texto é o
recurso para plataformas sem essa capacidade. O tracker instalado usa
`issue_dependencies_summary.blocked_by` para consultar bloqueios.

**Consequência:** duas migrations podem continuar elegíveis em paralelo pelo
grafo nativo mesmo depois de o usuário aprovar a edição textual que deveria
serializá-las. O diff do corpo não prova que a aresta usada pelo tracker mudou.

**Ajuste sugerido:** distinguir as operações por mídia: atualizar `Blocked by`
nos arquivos; no GitHub, criar a relação nativa pelo procedimento do tracker,
usando o ID de banco da issue bloqueadora, e manter o corpo coerente. Usar o
texto como substituto apenas quando a plataforma não oferece a relação.
Recalcular a largura depois de acrescentar as arestas, antes da decisão final.

**Conferência executada:**

```bash
M=~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1
sed -n '60,65p' $M/skills/engineering/to-tickets/SKILL.md
sed -n '40,45p' $M/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md
```

Encerra com um cenário de duas migrations inicialmente independentes em cada
mídia: depois da correção, o segundo ticket deve ter o primeiro como bloqueador
na representação que o orquestrador efetivamente consulta.

## 3. P2 — O modo arquivo precisa tornar os tickets acessíveis nas worktrees

**Local:** spec, linhas 76–86, 96–102 e 118–119;
`skills/midia/arquivo.md`, linhas 54–60 e 78–80.

O remédio fica no ticket local, em `.scratch/`, mas o fluxo não exige que esses
arquivos estejam versionados nem define como os subagentes os leem quando essa
pasta está no gitignore. Alinhar o tracker só fixa a localização da spec e a
referência `**Spec:**`. Essa referência resolve ticket → spec; não torna o próprio
ticket disponível em outro checkout. O Matt manda os subagentes trabalhar em
worktrees e comunicar-se por ponteiros para spec e tickets.

**Consequência:** num projeto com `.scratch/` ignorada, o orquestrador consegue
ler o grafo no checkout principal, mas o subagente que recebe um caminho relativo
ao ticket não encontra o arquivo na sua worktree. As instruções acrescentadas
ao ticket também ficam inacessíveis nesse caso. No modo issue, o alvo remoto
continua acessível e não sofre dessa ausência local.

**Ajuste sugerido:** definir a forma de acesso aos tickets locais a partir de
qualquer worktree: ponteiros absolutos para uma origem compartilhada, cópia
acessível fora do repositório ou material versionado, conforme a convenção
escolhida. Distinguir esse material das credenciais; não mandar copiar `.env`
como solução genérica. Incluir esse caso na Verificação.

**Contraprova executada:** foi criado um repositório descartável em
`/tmp/aicf-revisao-implement-spec-2exck97o/main`, com `.scratch/` no gitignore e
um ticket local, e uma worktree do mesmo HEAD. Nenhum arquivo do projeto foi
alterado. Reproduzir a leitura do resultado:

```bash
git -C /tmp/aicf-revisao-implement-spec-2exck97o/main check-ignore .scratch/feature/issues/01-ticket.md
test -f /tmp/aicf-revisao-implement-spec-2exck97o/main/.scratch/feature/issues/01-ticket.md
test -f /tmp/aicf-revisao-implement-spec-2exck97o/ticket-worktree/.scratch/feature/issues/01-ticket.md
```

O primeiro comando identifica o arquivo ignorado; os dois `test` retornam,
respectivamente, 0 e 1. O subagente deve conseguir abrir o ticket mesmo nesse
cenário para encerrar o achado.

## 4. P2 — Rodar no checkout principal não garante testar o código do ticket

**Local:** spec, linhas 84–90 e 99–102;
`skills/implementar-spec/SKILL.md`, linhas 72–79.

A exceção à proibição vigente de worktree com estado não versionado vira uma
linha no ticket: verificar no checkout principal. Falta definir **quando** e
**sobre qual revisão**. Enquanto o implementador trabalha na própria branch,
o checkout principal pode estar na branch de origem ou na integração ainda sem
aquele ticket. A linha 89 especifica a branch para a verificação ponta a ponta
final, mas não para o teste de cada ticket que depende desse estado.

**Consequência:** o teste que foi pulado na worktree pode ser executado contra
código anterior no checkout principal e ainda assim dar verde. Migrations de
tickets diferentes também podem disputar o mesmo banco fora das worktrees se
essa fase de verificação não tiver ordem definida.

**Ajuste sugerido:** fixar que a verificação dependente de estado local ocorre
depois de o código correspondente chegar à integração, com o checkout de teste
nessa revisão, e registrar seu resultado antes de considerar o ticket verificado.
Serializar o acesso ao estado compartilhado. Se o workspace disponível não
permite isso, recomendar a execução serial e explicar o impedimento.

**Conferência executada:** os passos 4–6 do Matt implementam na worktree e só
depois fazem merge na integração:

```bash
sed -n '27,34p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/implement-spec/SKILL.md
sed -n '66,68p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/docs/engineering/implement-spec.md
```

**Contraprova de aceite:** um ticket muda comportamento coberto por fixture
ignorada. O teste deve falhar contra o código anterior e passar contra o commit
do ticket incorporado à integração. Registrar apenas o diretório de execução
não satisfaz essa condição.

## 5. P2 — O fechamento por PR precisa preservar o estado da demanda do aicf

**Local:** spec, linhas 65–69 e 104–126;
`skills/fechar-demanda/SKILL.md`, linhas 16–20 e 37–42;
`skills/midia/issues.md`, linhas 9–12 e 31–38.

O passo 3 do Matt abre o PR com fechamento da **spec e dos tickets**. O passo 8
marca o PR como pronto para revisão; não o deixa em rascunho nem faz o merge.
A tabela proposta ainda apresenta PR em rascunho como resultado da integração.

Ao mandar fazer o merge antes do relatório, a solução permite que a própria
issue `aicf:spec` seja fechada automaticamente antes do ritual. Falta dizer como
o aicf reconhece essa issue já fechada, acrescenta o relatório e remove o label.
A mídia exige que issue concluída não carregue `aicf:*`; o fechamento automático
do PR não executa a operação de remoção definida nessa receita.

Também ficaram incompatíveis as decisões “a integração [...] não terminou
enquanto [...] não entrou na de origem” e oferecer “PR” ou “deixar a branch”
como saídas, sem definir se essas escolhas deixam a demanda parcial. A regra
atual exige decidir o destino; a nova redação passa a exigir entrada efetiva.

**Consequência:** no modo issue, a demanda pode desaparecer da lista de specs
abertas com label antigo e sem relatório. Nos dois modos, o agente não sabe se
deve concluir a demanda quando o usuário mantém a branch ou deixa o PR aguardando
revisão. Invocar o fechamento na integração também não define onde continua o
ritual depois do merge dela na origem.

**Ajuste sugerido:** especificar os estados após o método: branch entregue sem
PR, PR pronto ainda aberto e PR integrado. Definir em quais deles o fechamento
é definitivo ou parcial, onde fica seu commit e como adotar a issue da spec já
fechada pelo merge, removendo o label e registrando o relatório sem duplicar a
demanda. Corrigir a tabela para distinguir criação em rascunho de entrega pronta
para revisão. Aplicar a regra no `fechar-demanda` e na receita que a executa.

**Conferência executada:**

```bash
M=~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1
sed -n '25p;38p' $M/skills/engineering/implement-spec/SKILL.md
sed -n '31,38p' skills/midia/issues.md
sed -n '16,20p;37,42p' skills/fechar-demanda/SKILL.md
```

Encerra com aceite que cubra PR pronto sem merge, merge que fecha a própria spec
e decisão de manter a branch, conferindo relatório, label e destino do commit.

## 6. P2 — A Verificação reprova a escolha padrão de executar um ticket por vez

**Local:** spec, linhas 53–61, 74–76 e 195–199.

A solução diz que `/implement` por ticket é o padrão e que a escolha pertence ao
usuário. A Verificação 5, porém, exige da próxima demanda pelo Matt a entrega de
`/clear` + `/implement-spec`, independentemente da largura medida ou da opção
escolhida. Ela não cobre a retomada limpa nem o fechamento descritos acima.

**Consequência:** um grafo estreito ou a preferência do titular pela execução
serial produzem comportamento correto que o próprio aceite considera falha.
Uma implementação que sempre entregue o paralelo pode satisfazer esse aceite.

**Ajuste sugerido:** dividir o resultado esperado por decisão: grafo estreito
ou escolha serial → `/implement <ticket>`; grafo largo e escolha paralela →
preparação e `/implement-spec <spec>`. Manter o teste de uso real em aberto com
responsável explícito, incluindo os cenários de retomada e fechamento por mídia.

**Contraprova de aceite:** uma spec com cadeia estritamente linear deve oferecer
o padrão serial e passar na verificação; um grafo que satisfaça o critério deve
oferecer o paralelo, mas respeitar a escolha serial do usuário. É uma
contradição entre condições escritas na spec, não falha observada de uma skill
já implementada.

## 7. P3 — A fonte citada não mede quatro tickets na mesma fronteira

**Local:** spec, linhas 55–57.

O trecho “Author Insight” do [resumo citado](https://developer.tenten.co/mattpocock-skills-v1-3-pr-implement-spec-retro)
recomenda specs com “four or more tickets with independent parallel frontiers”.
Isso mede o total de tickets e exige paralelismo; não fixa largura mínima da
fronteira em quatro. Um grafo com quatro tickets divididos em duas ondas de dois
atende à descrição publicada, mas não ao limiar proposto na spec. A doc primária
do Matt não fixa esse número, como a própria spec reconhece.

**Consequência:** uma decisão de heurística do aicf é apresentada como número
extraído da fonte, com unidade diferente. Isso enfraquece a justificativa do
critério que será carregado pelas duas skills.

**Ajuste sugerido:** assumir explicitamente o limiar de largura como decisão do
aicf, com justificativa e contraprova, ou usar exatamente o critério da fonte.
Não atribuir ao Matt nem ao resumo uma medida que eles não publicam.

**Conferência executada:** leitura da URL citada pelo navegador de pesquisa,
seção “Author Insight”; no material primário instalado, leitura da tabela
“When to reach for it” e de “Prerequisites”:

```bash
sed -n '7,22p' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/docs/engineering/implement-spec.md
```

## 8. P3 — Separar o cache da release e o checkout posterior usado como pino

**Local:** spec, linhas 127–132 e 207–212.

O checkout `5beb35b` não é a tag `v1.3.1`: ele está depois dela. O cache instalado
confere com a documentação da tag, enquanto `docs/engineering/implement-spec.md`
já tem outro texto naquele checkout. A skill `implement-spec/SKILL.md` confere
entre os dois, portanto isso não invalida seu passo 8, mas são fontes distintas.

A frase proposta para a governança diz que a skill saiu de `in-progress/` “na
v1.3.1”; o Contexto levantado e o changelog instalado registram a promoção na
v1.3.0. O `grep 'resolve each ticket'` prova a regra de fechamento, não a versão
ou a data da promoção.

**Consequência:** a correção de um relatório histórico introduz outra imprecisão,
e reproduzir pelo sha não significa reproduzir exatamente a cópia instalada.

**Ajuste sugerido:** escrever que a skill está publicada **desde a v1.3.0** e
foi conferida no cache v1.3.1; identificar separadamente o checkout posterior,
se ainda necessário. Acrescentar o comando do changelog ou histórico à afirmação
de promoção. Manter o pino histórico `c55ee46` com a nota datada continua viável.

**Conferência executada**, usando os clones já existentes, sem alterá-los:

```bash
R=/tmp/claude-1000/-home-mh-dev-skills/85d7cca3-cc45-4e45-b6db-67e9d3a14b81/scratchpad/repos
M=~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1
git -C $R/skills rev-parse HEAD v1.3.1^{}
git -C $R/skills describe --tags --always
cmp $R/skills/docs/engineering/implement-spec.md $M/docs/engineering/implement-spec.md
git -C $R/skills show v1.3.1:docs/engineering/implement-spec.md | cmp - $M/docs/engineering/implement-spec.md
sed -n '9,16p' $M/CHANGELOG.md
```

Os hashes retornados foram `5beb35b040e3de97e54fa9e386d7e42d15c295c2` e
`24fe0ef7737efae15c87225755e9f6f5965e4888`; o `describe` devolveu
`v1.3.1-47-g5beb35b`. O primeiro `cmp` acusou diferença na linha 5; a comparação
com a tag retornou 0. A entrada `1.3.0` do changelog registra a promoção.

## Validação e limites

Foram lidos `AGENTS.md`, `.claude/CLAUDE.md`, o parecer de referência, a spec,
`criar-spec`, `implementar-spec`, `fechar-demanda`, ambas as receitas de mídia,
o template do setup, os READMEs e o relatório de governança. No cache instalado
do Matt foram conferidos `implement-spec`, sua documentação, `implement`,
`to-tickets`, o setup e os trackers local e GitHub. Os clones já presentes foram
conferidos com `git rev-parse HEAD`: Matt no sha citado acima e Superpowers em
`2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`.

O novo arquivo de critérios, quando **explicitamente lido** por ambas as skills,
atende ao propósito de “critério mora na skill que o aplica”: a regra estará
carregada no passo que decide. Não há exigência de duplicá-la. A exclusão de
atualização automática de projetos existentes tem encaminhamento explícito no
intent e nas notas da release. Os arquivos previstos cobrem as alterações
descritas, ressalvadas as lacunas de fluxo dos achados.

### Comandos da Verificação executados literalmente

| Item | Resultado atual | Conferência com “hoje” |
| --- | --- | --- |
| 1: `./scripts/check.sh` | `Tudo verde.`, saída 0 | Confere |
| 2: `grep -rl 'quando cabe numa sessão' skills/` | `skills/implementar-spec/SKILL.md` e `skills/criar-spec/SKILL.md` | Confere |
| 2: referências a `caminhos.md`, com `wc -l` | 0 | Confere |
| 3: ocorrências de `implement-spec` | 0 em cada arquivo existente; erro de arquivo inexistente para `caminhos.md` | Confere com a ressalva escrita; o comando completo sai com 2 |
| 4: frase antiga em cada README | 1 em português e 1 em inglês | Confere |
| 4: data no relatório de governança | 0 | Confere |
| 5: comportamento | Não executado | Depende da implementação e do uso real pelo titular |

O primeiro grep do item 2 mede uma frase da redação antiga. O conteúdo decidido
para `caminhos.md` não obriga a conservar essa frase; presença textual também
não prova exclusividade do critério inteiro. É limite desse aceite estático,
não contagem atual divergente. Da mesma forma, a presença de `implement-spec`
em cada arquivo não verifica a correção dos fluxos descritos.

### Linhas e comandos das fontes

As referências ao relatório de governança **estão certas**: a linha 90 é a linha
do critério 4 na tabela; a 215 é a afirmação 4 com a nota sobre a skill não
publicada. Conferido com:

```bash
nl -ba docs/referencias/governanca-nos-frameworks-vizinhos.md | sed -n '85,90p;212,216p'
```

Com `M` atribuído corretamente, os greps citados na spec para `resolve each
ticket`, `gives each one a git worktree`, `clear the context and type` e `run it
in the main checkout` reproduzem as linhas 38, 22, 40 e 68 no cache. A referência
às seams na linha 52 também confere. A atribuição deve ser `M=...`, sem `$` à
esquerda; a notação literal `$M=...` da linha 208 não é atribuição válida no shell.
O histórico de adição reproduziu `24f41cc 2026-09-24 Graduate implement-spec to
engineering`. Esses comandos foram executados com `R` apontando para os clones
indicados no achado 8; a spec não inicializa `R` em seu próprio texto.

No clone pinado do Superpowers, o grep `in parallel (conflicts)` reproduziu a
linha 233 e `Batch small same-shape work` encontrou a linha 5 de `batching.md`.
A [issue #945](https://github.com/obra/superpowers/issues/945) confirma a decisão
do mantenedor por execução iterativa. A [issue #429 do Matt](https://github.com/mattpocock/skills/issues/429)
confirma a recomendação de worktree por sessão de `/implement`. O
[relato de uso](https://dev.to/day_b3fa2204948ded3059f6f/turning-matt-pococks-implement-into-a-parallel-orchestrator-in-claude-code-1d4a)
contém os números e incidentes resumidos na spec; não é benchmark comparativo.
Na [documentação do Antigravity](https://antigravity.google/docs/cli/features),
a seção de subagentes confirma execução concorrente em background e não
documenta ali isolamento por worktree. Isso sustenta manter a ressalva; não
prova ausência dessa capacidade em todo o produto.

**Comando que não reproduziu a consulta:** `gh issue view 945 -R
obra/superpowers --comments` falhou com `error connecting to api.github.com`.
As consultas adicionais de leitura por `gh` às PRs 1213 e 1534 e à issue 429
também falharam por rede. A leitura web confirmou a issue 945 e a 429, mas a PR
1213 não carregou e a página disponível da PR 1534 mostrava estado aberto em
captura anterior. Portanto, **não foi possível confirmar o fechamento das duas
PRs em 2026-09-27**; não se toma essa captura anterior como prova de que a frase
é falsa. Essa afirmação e a ausência de benchmark independente ficam sem
validação conclusiva neste parecer. A spec também não traz comando específico
para conferir aquelas datas de fechamento nem as buscas por benchmark.

### Checks e fechamento do parecer

`wc -c skills/*/SKILL.md` conferiu o limite em cada skill existente; o
`check.sh` confirmou que nenhuma passa de 24000 bytes. Antes das mudanças,
`criar-spec`, `implementar-spec` e `fechar-demanda` têm, respectivamente,
6681, 8598 e 10187 bytes (`wc -c` nos três arquivos). O limite precisa ser
conferido novamente depois da implementação, como a Verificação já manda.

Nenhuma skill de entrevista ou implementação foi invocada. A contraprova de
worktree usou somente arquivos temporários. O fechamento de
`aicf:fechar-demanda` foi aplicado apenas ao parecer, respeitando “Agente Codex:
só revisa”: a spec e os demais arquivos permanecem intactos; decisões e aplicação
das sugestões cabem ao agente líder e ao titular.

O check antes do commit terminou em `Tudo verde.`, saída 0, com Claude Code
`2.1.310`, ambas as validações aprovadas, versão `0.43.2` no topo do changelog e
nenhuma skill acima do limite. O validador emitiu aviso de ícone ausente, sem
reprovação. O whitespace e o escopo do commit são conferidos antes de commitar;
o `git mv` preexistente permanece no index. Não há push neste trabalho, por
instrução do titular; envio e eventual CI ficam com ele ou o agente líder.
