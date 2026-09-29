# A refatoração contínua não tem passo que a aplique

Processo — entrevista: criar-spec · implementação: aicf-direto

Registrada em 2026-09-29, a partir da pergunta do titular sobre onde o método manda o agente
procurar o que simplificar durante uma implementação. Entrevistada no mesmo dia.

## Problema

A regra existe só como princípio, no Lema do template do `CLAUDE.md`
(`grep -c 'Refatoração contínua' skills/setup/templates/claude-md.md` → 1 em `45edc04`):

> **Refatoração contínua:** trecho que ficou mais complexo com o tempo se simplifica antes de
> receber feature nova.

Ela está no contexto de toda sessão de um projeto aicf, mas nenhum passo do ciclo a dispara:
nenhuma skill fala em refatorar (`grep -rli 'refator' skills/*/SKILL.md` → nada, sai com 1). E o
`implementar-spec` puxa na direção contrária — *"Não ampliar o escopo: … ideia nova que aparecer no
caminho vira registro para depois, não código agora"* —, que, sendo a instrução mais específica,
vence o princípio quando o agente vê um trecho a simplificar.

## Solução

**A regra sai do template do `CLAUDE.md` e vai para o `implementar-spec`**, que é quem a aplica —
pela regra do repositório "Critério mora na skill que o aplica".

1. **Passo 2 do `implementar-spec`** ("Ler os arquivos que a spec nomeia") ganha a pergunta: *o
   trecho que a demanda vai mudar ficou complexo demais para receber a mudança?* Se sim,
   simplificá-lo faz parte da demanda — sem mudar comportamento, num **commit próprio, antes do
   commit da mudança**, para a revisão separar o que só reorganiza do que muda o que o código faz.
   O critério de "complexo demais" fica escrito ali, curto e concreto (ex.: a mudança copiaria uma
   duplicação que já existe, ou acrescentaria mais um ramo a uma condicional que já não se lê).
2. **A frase do escopo, na seção "Implementar"**, passa a traçar a mesma linha, para as duas não se
   contradizerem: simplificar o trecho que a demanda toca é parte dela; refatorar um trecho vizinho
   que ela não toca é ideia nova, e vira registro.
3. **A frase sai do template** (`skills/setup/templates/claude-md.md`) **e do `CLAUDE.md` deste
   repositório**, que também implementa pelo `implementar-spec` — manter as duas seria ter dois
   mecanismos para a mesma regra. O resto do Lema (simplicidade e o "Gatilho de revisão") fica.
4. **Versão e `CHANGELOG.md`** sobem juntos, no commit de código. A **nota da release** diz, em uma
   linha, que a regra passou para o `/aicf:implementar-spec` e que quem já rodou o setup pode apagar
   a frase do próprio `CLAUDE.md` — mantê-la não conflita com nada.

## Arquivos e interfaces

- `skills/implementar-spec/SKILL.md` — passo 2 e a seção "Implementar"
- `skills/setup/templates/claude-md.md` — sai a linha 11 e a linha em branco que a segue
- `CLAUDE.md` — sai a linha 13 e a linha em branco que a segue
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — versão nova no topo

Ninguém aponta para este arquivo pelo caminho de `intents/`
(`grep -rn 'a-refatoracao-continua' . --exclude-dir=.git` só acha o próprio arquivo).

## Fora de escopo

- **Os caminhos Superpowers e Matt Pocock** ficam sem a regra. Cada método tem o próprio critério
  de design, e o `implementar-spec` já diz que o aicf não interrompe nem substitui passo interno de
  outro método.
- **Passada de simplificação sobre o diff no `fechar-demanda`** (o que o `/simplify` faz): resolve
  outro problema — arrumar o que acabou de ser escrito, não preparar o terreno antes — e somaria um
  passo ao ritual de todo caminho.
- **O `~/.claude/CLAUDE.md` global**: repetiria o princípio sem o gatilho, que é o que já existe
  hoje, e carregaria em toda sessão, inclusive nas que não implementam.
- **Migração dos projetos que já rodaram o setup**: o setup roda uma vez, e a frase que sobra é
  inofensiva; a nota da release basta.

## Verificação

1. `grep -c 'Refatoração contínua' skills/setup/templates/claude-md.md CLAUDE.md` → `0` nos dois
   (hoje, `1` nos dois).
2. `grep -rli 'refator' skills/*/SKILL.md` → `skills/implementar-spec/SKILL.md`, e só ele (hoje,
   nada).
3. Ler o passo 2 e a frase do escopo do `implementar-spec` lado a lado: a linha "trecho tocado ×
   trecho vizinho" é a mesma nos dois, e o commit próprio da refatoração está dito.
4. `./scripts/check.sh` → `Tudo verde.`, com a versão nova no topo do `CHANGELOG.md`.
5. **Comportamento fica para o uso real.** Testar o `implementar-spec` depende de atualizar o plugin
   e reiniciar a sessão, o que é do titular; pela regra de 2026-09-25, não se pede. Encerra na
   primeira demanda implementada pelo `implementar-spec` cujo trecho tocado pedia simplificação: o
   agente a propõe no passo 2 e ela sai num commit próprio, antes do da mudança.

## Relatório de implementação (2026-09-29)

- **Status** — concluído; CI do push de `de6f871` conferido no fechamento.
- **Arquivos alterados**
  - `skills/implementar-spec/SKILL.md` — o passo 2 pergunta se o trecho a mudar ficou complexo
    demais e manda a simplificação para um commit próprio, antes do da mudança; a frase do escopo
    separa trecho tocado de trecho vizinho
  - `skills/setup/templates/claude-md.md` e `CLAUDE.md` — sai a frase "Refatoração contínua"
  - `.claude-plugin/plugin.json` e `CHANGELOG.md` — `0.34.0`
- **Commits** — `44c2992` docs(projeto): entrevista da refatoração contínua vira spec ·
  `de6f871` feat(implementar-spec): a refatoração contínua vira pergunta ao ler os arquivos
- **Validação**
  - `grep -c 'Refatoração contínua' skills/setup/templates/claude-md.md CLAUDE.md` → `0` nos dois
  - `grep -rli 'refator' skills/*/SKILL.md` → só `skills/implementar-spec/SKILL.md`
  - Passo 2 e frase do escopo lidos lado a lado: a mesma linha "trecho tocado × trecho vizinho"
  - `./scripts/check.sh` → `Tudo verde.`, `0.34.0` no topo do `CHANGELOG.md`
  - Sem revisão de código: a mudança é texto de skill, `+8 −3` no `implementar-spec`
    (`git diff --stat 44c2992 de6f871 -- skills/implementar-spec/SKILL.md`)
  - **Comportamento em aberto**, pela Verificação 5: encerra na primeira demanda implementada pelo
    `implementar-spec` cujo trecho tocado pedia simplificação — o agente a propõe ao ler os
    arquivos e ela sai num commit próprio, antes do da mudança.
- **Escopo efetivo** — o previsto. O passo 2 é descrito sem número na frase do escopo, para não
  criar ponteiro que envelhece.
- **Promoção** — nada a promover; o fechamento não gerou ADR, regra nem doc. Nenhuma outra demanda
  muda.
