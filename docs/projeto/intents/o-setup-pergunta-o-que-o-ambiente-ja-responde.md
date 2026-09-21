# O setup pergunta o que o ambiente já responde, e despeja o mapa na tela

Processo — entrevista: a definir · implementação: a definir

> **Encerra quando** o roteiro do `skills/setup/SKILL.md` tratar os quatro pontos abaixo — cada um
> resolvido ou descartado com o motivo escrito —, e a próxima passada de verificação confirmar o
> comportamento novo. Ou quando a entrevista concluir que o roteiro está certo e quem desviou foi o
> agente, e este arquivo for para `concluidas/` dizendo isso.

## Origem

A primeira passada do ramo issue, em 2026-09-21, na `0.24.0`. Ela **passou** — os cinco comandos de
[verificacao-do-setup.md](../../referencias/verificacao-do-setup.md) deram o esperado, e nenhum
arquivo gerado tinha defeito. O que ela achou foi outra coisa: quatro pontos em que o agente desviou
do roteiro, três deles porque o roteiro pede mais trabalho do que o caso exigia.

A evidência dos quatro está no transcript da sessão, em
`~/.claude/projects/-home-mh-dev-tmp-teste-aicf-issues/*.jsonl` — extrair com o `jq` que o doc de
verificação traz.

## Os quatro pontos

**1. As três perguntas de ferramentas, quando o global já as respondeu.** O roteiro manda perguntar
gerenciador de senhas, fonte de documentação e coleções de skills *"uma de cada vez, em pergunta
aberta"*. O agente leu o `~/.claude/CLAUDE.md`, achou Bitwarden e Context7 declarados, detectou as
coleções instaladas, e pediu **confirmação das três de uma vez**. O usuário respondeu *"tudo ok,
pode seguir"*. Três perguntas viraram uma confirmação, e o resultado gravado foi o mesmo. O roteiro
não prevê ler o global — e é ele que tem a resposta em quase toda máquina que já usa o método.

**2. O mapa do workflow cai na tela.** O passo 2 de "Ao terminar" manda *"carregar
`/aicf:workflow-demanda`"*, e o agente fez `cat` do `SKILL.md` — 167 linhas na `0.24.0`
(`wc -l < skills/workflow-demanda/SKILL.md`) impressas no meio da apresentação do método, para quem
está vendo o aicf pela primeira vez. A skill **não** tem `disable-model-invocation`, então a
ferramenta Skill a carrega sem imprimir nada. É o defeito com efeito mais visível dos quatro, e o
único que contraria diretamente [a entrada de quem chega](../concluidas/a-entrada-de-quem-chega.md),
cuja restrição era o setup não virar muro de texto.

**3. A ordem das opções da mídia.** O roteiro marca *arquivos em `docs/projeto/`* como default, e a
pergunta saiu com *Issues (GitHub)* em primeiro — e o `AskUserQuestion` lê a primeira opção como a
sugerida. O diretório se chamava `teste-aicf-issues`, o que provavelmente enviesou; num projeto real
o nome também enviesa. O roteiro não diz que a ordem das opções é parte da prescrição.

**4. Mídia e padrões numa chamada só.** O roteiro descreve duas chamadas de `AskUserQuestion`
(*"Depois, com `AskUserQuestion`, perguntar onde ficam os padrões"*), e o agente juntou as duas
perguntas numa chamada. As duas são independentes, então juntar funcionou e economizou uma rodada.

## O que decidir na entrevista

- **O setup lê o `~/.claude/CLAUDE.md` antes de perguntar?** Se sim, as três perguntas de
  ferramentas viram confirmação do que já está lá — e o roteiro precisa dizer o que fazer quando o
  global responde só uma das três. Se não, o roteiro precisa dizer por que não, porque o agente vai
  ler de novo.
- **O passo 2 de "Ao terminar" passa a nomear a ferramenta Skill?** Ou a instrução muda de forma —
  *"invocar, não imprimir"* — para valer também em harness que só tem shell, onde `cat` é o único
  caminho e o despejo na tela é inevitável.
- **A ordem das opções vira prescrição?** O roteiro diz qual é o default; falta dizer que default é
  a primeira opção da lista.
- **As duas perguntas viram uma, ou a separação tem motivo?** Se o motivo é que a resposta da mídia
  pode mudar a pergunta dos padrões, ele não está escrito. Se não há motivo, uma chamada é menos
  interrupção.
