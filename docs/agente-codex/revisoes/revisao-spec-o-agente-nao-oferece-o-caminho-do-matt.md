# Revisão da spec — O agente não oferece o caminho do Matt

Data: 2026-10-07. Parecer consultivo sobre
`docs/projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md`, linhas 1–150.
Base do repositório: `73e6dfa`. A spec estava não rastreada no início da revisão;
esta revisão não a adiciona ao git nem altera seu conteúdo. Identificação da cópia:
`sha256sum docs/projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md` →
`e7de6c041de39c7cdc814b410ca9d610276b1dbfddd9950a2a80b2c2a605abde`.

Resultado: três achados P2 a resolver antes da implementação. As causas descritas e
a substituição do `to-spec` pelo `criar-spec` são sustentadas pelos arquivos
consultados; as lacunas estão na cobertura dos pontos de entrada e na retomada.
P2 significa correção necessária para os cenários descritos, sem urgência operacional.

## 1. P2 — Incluir as instruções ativas deste repositório na mudança

**Local:** spec, linhas 81–110, inventário e migração do template.

A spec altera `skills/setup/templates/claude-md.md` e prevê que o titular migre o
projeto privado de origem. Falta incluir o
[`.claude/CLAUDE.md`](../../../.claude/CLAUDE.md) deste repositório. Ele também declara
Matt e Superpowers instalados e contém as regras que estão sendo substituídas:
`grill-with-docs` → `to-spec`, sugestão sem os critérios novos e passagem do
`brainstorming` pela receita da mídia. É o arquivo que os agentes leem aqui, antes
de invocar qualquer skill; mudar o template não modifica essa cópia.

**Consequência:** depois da entrega, uma demanda entrevistada neste próprio projeto
continua recebendo instruções para usar o `to-spec` e pode pular o `criar-spec` na
passagem de fase. O plugin e suas instruções locais passam a prescrever fluxos
diferentes exatamente no ponto em que a demanda quer eliminar o viés.

**Ajuste sugerido:** incluir a atualização dos trechos correspondentes do
`.claude/CLAUDE.md` em Arquivos e interfaces e na verificação estática. A migração
dos projetos consumidores continua nas notas da release.

**Conferência executada:**
``grep -nE 'grill-with-docs|vira a spec da demanda pela receita da mídia' .claude/CLAUDE.md``
mostra as duas regras antigas na base. Encerra quando os trechos ativos daqui
prescreverem o mesmo fluxo que o template novo.

## 2. P2 — Cobrir a conversão de intent sem entrevista e a entrada de spec externa

**Local:** spec, linhas 47–55 e 91–98.

O contrato novo diz que **toda spec passa pelo `criar-spec`**, para que o formato e
as decisões de teste sejam definidos pela skill que os possui. Entretanto, a spec
só prevê alterar o passo 3 do `implementar-spec`. O
[passo 1 atual](../../../skills/implementar-spec/SKILL.md) ainda aceita spec de
`docs/superpowers/specs/` diretamente e transforma intent em spec **pela receita
da mídia**, com `entrevista: nenhuma`, quando o usuário pede implementação sem
entrevista. Nenhum dos dois casos manda carregar o `criar-spec`.

**Consequência:** o usuário pode chegar à escolha do Matt com uma spec criada por
esse atalho sem o item Testes que a solução passou a exigir. A dependência de um
formato conhecido deixa de ser garantida fora das duas entrevistas citadas.

**Ajuste sugerido:** decidir explicitamente se o contrato abrange esses pontos de
entrada. Se abrange, incluir o passo 1 e um modo de normalização no `criar-spec`
que preserve o pedido de pular a entrevista e `entrevista: nenhuma`, exigindo
somente decisões realmente faltantes. Se o contrato cobre apenas as entrevistas
por `brainstorming` e `grill-with-docs`, delimitar a frase “toda spec” e definir
como o `implementar-spec` verifica Testes antes de entregar uma spec ao Matt.

**Conferência executada:** `sed -n '10,16p' skills/implementar-spec/SKILL.md`
mostra ambos os pontos de entrada. Encerra com uma regra explícita para os dois e
um cenário de verificação de demanda de código que chega sem entrevista.

## 3. P2 — Preservar o vínculo com a spec e os testes na retomada dos tickets

**Local:** spec, linha 42, linhas 63–77 e Verificação, linhas 144–150.

A spec passa a morar em `docs/projeto/specs/`, enquanto os tickets locais ficam
no tracker do Matt. Isso é compatível com a separação entre governança e plano,
mas falta definir como uma sessão nova encontra a spec original e suas decisões
de teste ao implementar um ticket.

No Matt `1.3.1`, o template de ticket local do `to-tickets` tem entrega, bloqueios,
status e critérios de aceite; não exige referência à spec nem cópia dos pontos de
teste acordados. A seção Parent aparece no template de issue remota. Já a
configuração padrão do tracker local situa a spec em
`.scratch/<feature-slug>/spec.md`, que o novo fluxo deixa de criar. O `implement`
manda trabalhar no item descrito pelo usuário e usar TDD nos pontos previamente
acordados, sem determinar a leitura de uma spec externa ao ticket. São contratos
dos arquivos pinados, não uma afirmação de que o agente necessariamente falhará.
[Fonte: `to-tickets` 1.3.1](https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/to-tickets/SKILL.md),
[tracker local](https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md) e
[`implement`](https://github.com/mattpocock/skills/blob/24fe0ef7737efae15c87225755e9f6f5965e4888/skills/engineering/implement/SKILL.md).

**Cenário:** entrevista e `to-tickets` terminam numa sessão; em outra, o usuário
entrega apenas um ticket local ao `/implement`. A confirmação dos pontos de teste
ficou na spec do aicf, e o ticket pode não dizer onde encontrá-la. Esse é o cenário
de várias sessões usado pela própria spec como critério para recomendar Matt.

**Ajuste sugerido:** definir a entrega com alvos explícitos: referência à spec
canônica — caminho no modo arquivo, número ou URL no modo issue — e aos tickets
selecionados na implementação. As decisões de teste precisam continuar acessíveis
sem depender da conversa anterior e sem duplicar a spec em `.scratch/`. A instrução
pode acompanhar o comando que o aicf entrega, sem alterar skills ou configuração
do Matt. Definir também que o fechamento final é da demanda canônica; um ticket
terminado não equivale à demanda inteira concluída.

A Verificação 3 termina antes do `to-tickets`. Estendê-la, como condição de uso
real pelo titular, até publicar tickets e retomar um em sessão nova, conferindo
a recuperação da spec e dos pontos de teste. O texto atual
`/to-tickets <caminho da spec>` também precisa de variante para modo issue; o
`to-tickets` aceita número ou URL como referência.

**Conferência executada no clone pinado:**
`sed -n '65,92p' skills/engineering/to-tickets/SKILL.md` mostra os dois templates;
`sed -n '1,15p' skills/engineering/implement/SKILL.md` mostra o contrato de
implementação; `sed -n '1,15p' skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md`
mostra onde o tracker local espera a spec. Encerra quando a entrega e a retomada
garantirem acesso à spec canônica e aos testes em uma sessão nova.

## Validação e limites

As nove contagens de “antes” da Verificação 1 foram executadas com os mesmos
padrões e arquivos da spec. Resultado, na ordem escrita:
`0, 1, 1, 0, 0, 0, 1, 1, 2`; todas conferem. `wc -l skills/criar-spec/SKILL.md`
confirma as 82 linhas atuais. A estimativa de linhas depois da mudança não foi
tratada como critério de aceite.

As afirmações sobre o Matt foram conferidas no cache indicado e num clone de
`v1.3.1`, cujo `git rev-parse HEAD` retornou
`24fe0ef7737efae15c87225755e9f6f5965e4888`. Os arquivos usados no parecer foram
comparados byte a byte com o cache. Reprodução do clone:

```bash
git clone --depth 1 --branch v1.3.1 https://github.com/mattpocock/skills.git /tmp/matt-spec-review
git -C /tmp/matt-spec-review rev-parse HEAD
```

O `grep -l 'disable-model-invocation: true'` nos quatro arquivos nomeados pela
spec confirmou os quatro. O wrapper `grill-with-docs` manda carregar `grilling`
e `domain-modeling`; ambos podem ser invocados pelo agente segundo o frontmatter.
A criação de glossário pelo `domain-modeling` e a ausência de `user stor` nos
diretórios consultados também foram conferidas com os comandos da spec.
O significado de `disable-model-invocation` foi conferido na
[documentação oficial do Claude Code](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill).

Esta é uma revisão estática da spec. Não foram invocadas skills dos fluxos
propostos nem simulado seu comportamento. A verificação em uso real continua
com o titular, depois da implementação e da migração das instruções do projeto.

O fechamento do `aicf:fechar-demanda` foi aplicado somente ao parecer, respeitando
a restrição de atuação do Codex. A demanda permanece aberta, e as sugestões são
para decisão e aplicação pelo agente líder com o usuário. Não houve promoção de
conhecimento fora deste diretório.

`./scripts/check.sh` terminou em `Tudo verde.`, com saída 0, Claude Code
`2.1.292`, 167 links conferidos e nenhum quebrado, os dois `Validation passed`
e versão `0.36.0` no topo do changelog. O commit contém somente este parecer.
Nenhum push faz parte desta revisão; o envio do parecer e a conferência do CI
ficam com o titular ou o agente líder, junto do registro da spec que ainda está
não rastreada. O whitespace do parecer é conferido com `git diff --cached --check`
antes do commit.

## Segunda revisão — 2026-10-07

Esta seção substitui o resultado anterior para a versão atual da spec, sem apagar
o histórico do parecer. Base: `8002e06`. Identificação da cópia revisada:
`sha256sum docs/projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md` →
`2cd8c7246f0b2738bf763bc69732354c5781ee5856a41225061ce98fcb196f0b`.

**Resultado: um achado P2.** Os três achados anteriores foram tratados: a spec
inclui as instruções ativas daqui; delimita a passagem obrigatória pelo
`criar-spec` às entrevistas e explica os atalhos; entrega a spec junto do ticket
e estende a verificação à retomada. Não é necessário reabrir esses achados.

### P2 — Escolher a referência do ticket pelo tracker do Matt

**Local:** [spec](../../projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md),
linhas 69–72, comandos entregues ao usuário; a regra também é levada ao passo 3
do `implementar-spec` pelo inventário de arquivos.

Os comandos propostos associam a mídia arquivo do aicf a tickets em `.scratch/`
e a mídia issue a tickets identificados por `#<ticket>`. Entretanto, a mídia do
aicf e o tracker do Matt são configurações independentes. Isso é permitido pela
[demanda anterior](../../projeto/concluidas/o-setup-nao-avisa-que-o-matt-pergunta-o-mesmo.md)
e pelo próprio `implementar-spec`, que avisa da divergência e segue a linha do
`CLAUDE.md` para a governança. Já o `to-tickets` publica no tracker configurado
em `docs/agents/issue-tracker.md`.

**Cenário e consequência:** aicf em arquivos e Matt em GitHub. O `to-tickets`
recebe corretamente `docs/projeto/specs/<nome>.md`, mas publica tickets remotos.
O comando de implementação prescrito aponta então para um ticket em
`.scratch/` que não existe. No caso inverso, aicf em issues e Matt em arquivos,
`#<ticket>` não identifica o ticket local criado. Com trackers remotos diferentes,
dois números sem origem também podem identificar itens errados.

**Ajuste sugerido:** determinar cada alvo pela sua configuração: a referência
da spec vem da mídia do aicf; a referência do ticket vem do tracker do Matt e dos
itens efetivamente publicados. Entregar primeiro o `to-tickets` com a spec; após
a publicação, entregar `implement` com a spec e o ticket escolhido, usando caminho
para ticket local e URL ou identificador inequívoco para remoto. Exemplos mistos:

```text
/implement docs/projeto/specs/<nome>.md <URL-do-ticket>
/implement <URL-da-spec> .scratch/<feature>/issues/<NN>-<slug>.md
```

Isso mantém a configuração alheia intacta e dispensa uma tabela de todas as
combinações. Acrescentar à verificação de uso real um caso com configurações
diferentes, conferindo que os dois alvos entregues existem e são lidos na retomada.
O achado encerra quando a regra separar a origem de cada referência e a condição
de verificação cobrir o caso misto.

**Evidência executada:** clone de `v1.3.1` em `/tmp/matt-review-8002e06`, com
`git -C /tmp/matt-review-8002e06 rev-parse HEAD` →
`24fe0ef7737efae15c87225755e9f6f5965e4888`. Nesse clone:

```bash
sed -n '38,49p' skills/engineering/setup-matt-pocock-skills/SKILL.md
sed -n '51,62p' skills/engineering/to-tickets/SKILL.md
```

O primeiro comando mostra a escolha independente de GitHub, GitLab, arquivos ou
outro tracker; o segundo, a publicação segundo essa escolha. Os arquivos
`SKILL.md` de `setup-matt-pocock-skills`, `to-tickets`, `implement`,
`grill-with-docs`, `tdd` e `domain-modeling` foram comparados byte a byte com o
cache `1.3.1` indicado na spec: todos iguais.

### Validação e fechamento desta revisão

Os treze `grep -c` da Verificação 1 foram executados com os padrões e os arquivos
escritos na spec. Resultados, na ordem: `0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 2`.
Todos conferem com os valores de antes. As contagens verificam presença de texto;
a retomada com os dois alvos é a condição que comprova o comportamento proposto.

Revisão estática: nenhuma skill de entrevista ou implementação foi invocada.
O uso real permanece com o titular, após a implementação. O fechamento
`aicf:fechar-demanda` foi aplicado somente ao parecer; a spec permanece aberta e
intacta. Não houve promoção de conhecimento fora do diretório permitido ao Codex.
O commit desta revisão contém somente a atualização do parecer. Nenhum push faz
parte desta revisão; envio e conferência do CI ficam com o titular ou agente líder.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, Claude Code `2.1.293`,
170 links conferidos e nenhum quebrado, os dois `Validation passed` e versão
`0.36.0` no topo do changelog. Antes do commit, `git diff --cached --check`
confere o whitespace do parecer.

## Terceira revisão — 2026-10-07

Esta seção substitui o resultado da segunda revisão para a versão atual da
[spec](../../projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md).
Base: `1e94218`. Identificação da cópia revisada:
`sha256sum docs/projeto/specs/o-agente-nao-oferece-o-caminho-do-matt.md` →
`aa3c1c286751644c56f77ccb3b0ab32107a689b45d447f286e71a3f1a1072ff0`.

**Resultado: nenhum novo achado que exija correção antes da implementação.**
O achado da segunda revisão foi tratado por uma decisão explícita de escopo:
o caminho de implementação do Matt só é oferecido com o tracker alinhado à mídia
do aicf — markdown local para arquivos, GitHub no mesmo repositório para issues.
A alternativa de suportar configurações divergentes foi descartada com motivo.
Essa decisão torna coerentes as referências dos comandos propostos, sem exigir
que o agente combine trackers diferentes. A Verificação 4 cobre a recusa do
caminho quando a configuração diverge ou está ausente.

As soluções dos três achados iniciais continuam presentes: atualização das
instruções ativas deste repositório, delimitação da passagem pelo `criar-spec`
às entrevistas e entrega da spec junto do ticket na retomada. O parágrafo novo
na seção Implementar também determina como os caminhos aicf usam o item Testes,
inclusive a invocação de `/tdd` quando o Matt está instalado.

### Evidência e limites

Os quatorze `grep -c` da Verificação 1 foram executados com os padrões e arquivos
da spec. Resultados, na ordem escrita:
`0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 2`.
Todos conferem com os valores de antes. As contagens de depois continuam como
critérios para a implementação; não comprovam comportamento por si mesmas.

Foram relidos `criar-spec`, `implementar-spec`, o template e o setup do aicf,
além de `grill-with-docs`, `domain-modeling`, `to-tickets`, `implement`, `tdd`
e a configuração de tracker local no cache do Matt `1.3.1` indicado pela spec.
Os comandos da spec para conferir as quatro skills de invocação exclusiva pelo
usuário, a criação do glossário, a confirmação dos pontos de teste e os modelos
de ticket foram executados novamente. A busca por `user stor` não retornou
ocorrências nos quatro diretórios indicados; a busca por `seam` retornou
`implement` e `tdd`.

Revisão estática: nenhuma skill dos fluxos propostos foi invocada. A oferta do
caminho, a passagem de fase e a retomada em sessão nova precisam da verificação
em uso real das condições 3 e 4, pelos responsáveis definidos na spec. Não há
promessa de que esses comportamentos tenham sido testados nesta revisão.

O fechamento de `aicf:fechar-demanda` aplica-se somente ao parecer. A spec
permanece aberta e intacta; nenhuma alteração ou promoção de conhecimento foi
feita fora do diretório permitido ao Codex. O commit desta revisão contém
somente este parecer. O envio e a conferência do CI ficam com o titular ou
agente líder; nenhum push faz parte desta revisão.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, Claude Code `2.1.293`,
171 links conferidos e nenhum quebrado, os dois `Validation passed` e versão
`0.36.0` no topo do changelog. O whitespace do parecer é conferido com
`git diff --cached --check` antes do commit.
