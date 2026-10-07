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
