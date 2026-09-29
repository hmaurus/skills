# A refatoração contínua não tem passo que a aplique

Processo — entrevista: a definir · implementação: a definir

Registrada em 2026-09-29, a partir da pergunta do titular sobre onde o método manda o agente
procurar o que simplificar durante uma implementação.

## O defeito

A regra existe só como princípio, no Lema do template do `CLAUDE.md`
(`grep -c 'Refatoração contínua' skills/setup/templates/claude-md.md` → 1):

> **Refatoração contínua:** trecho que ficou mais complexo com o tempo se simplifica antes de
> receber feature nova.

Ela está no contexto de toda sessão de um projeto aicf, mas nenhum passo do ciclo a dispara:
nenhuma skill fala em refatorar (`grep -rli 'refator' skills/*/SKILL.md` → nada). E o
`implementar-spec` puxa na direção contrária — *"Não ampliar o escopo: … ideia nova que aparecer no
caminho vira registro para depois, não código agora"* —, que, sendo a instrução mais específica,
vence o princípio quando o agente vê um trecho a simplificar.

## O que se decidiu

**A regra sai do template do `CLAUDE.md` e vai para o `implementar-spec`**, que é quem a aplica —
pela regra do repositório "Critério mora na skill que o aplica". O lugar natural é o passo 2
("Ler os arquivos que a spec nomeia"): é ali que *este trecho ficou complexo demais para receber a
mudança?* vira pergunta concreta. E a frase do escopo muda na mesma skill, para as duas não se
contradizerem.

O `~/.claude/CLAUDE.md` global foi considerado e descartado: repetiria o princípio sem o gatilho,
que é o que já existe hoje, e carregaria em toda sessão, inclusive nas que não implementam.

## A decidir na entrevista

- **Onde passa a linha do escopo.** Rascunho: simplificar o trecho que a demanda vai tocar é parte
  dela; refatorar trecho vizinho que ela não toca vira registro. Commit separado para a
  refatoração, antes do commit da mudança?
- **Os outros caminhos.** Superpowers e Matt Pocock não passam pelo `implementar-spec`; tirar a
  frase do template os deixa sem o princípio. Aceitar, ou complementar no `fechar-demanda` — que
  roda em todo caminho — com um passe de simplificação sobre o diff (o que o `/simplify` faz)? São
  coisas diferentes: um prepara o terreno antes, o outro arruma o que acabou de ser escrito.
- **O `CLAUDE.md` deste repositório** tem a mesma frase (`grep -c 'Refatoração contínua' CLAUDE.md`
  → 1). Sai junto, fica como regra deste projeto, ou vira ponteiro?
- **Projetos que já passaram pelo setup** continuam com a frase no `CLAUDE.md` deles. Não há
  migração — o setup roda uma vez —; a nota da release diz o que fazer, ou nada?
