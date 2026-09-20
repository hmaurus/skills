# PRD — aicf

O porquê do produto. Responde o que nenhuma linha de código responde: para quem isto existe e o que conta como sucesso.

Documento vivo — quando uma decisão o contrariar, revisar por `/aicf:criar-prd`, em vez de deixar envelhecer.

**Última revisão:** 2026-09-19

## Problema

Quem desenvolve software com agente tem, nas coleções de skills de engenharia, cuidado bom para **uma demanda por vez**: elas interrogam a ideia, escrevem a spec, quebram em tarefas e executam com disciplina. Começam numa ideia já formulada e param no commit. Três coisas ficam sem dono:

- **A conversa some no `/clear`.** A decisão de não seguir por um caminho, e o motivo, viveram só na sessão. Semanas depois a mesma discussão volta.
- **Ninguém sabe onde o projeto está.** Specs contam cada mudança, uma por uma. Nenhuma diz o que o produto é, para quem serve e o que ficou de fora por decisão.
- **O que saiu de fato não fica escrito.** Spec e plano foram escritos antes de executar. O que mudou no caminho só existe se alguém escrever no fim, e ninguém pede.

O problema foi vivido nos projetos do autor, e tem uma segunda camada: **framework de processo rígido é burlado no meio do projeto.** A primeira tentativa foi adotar um framework de desenvolvimento completo; no meio de um projeto o autor já contornava o processo dele para simplificar do próprio jeito. A camada de governança que sobreviveu a isso, e à troca de Superpowers pelas skills do Matt Pocock, é a que só faz sentido quando não depende do caminho de implementação.

O momento agrava: desenvolvimento com IA está começando, não há caminho exato validado, e todo mundo, inclusive quem tem experiência, está testando. Quem chega agora está sem instrução para seguir.

## Público

O fio comum: **quem quer empreender desenvolvendo aplicativos web com IA e Claude Code.** Três perfis, com pedidos diferentes:

- **O autor, nos próprios projetos.** Quer um método que sobreviva à troca de ferramenta e que não seja burlado no meio do caminho. É o primeiro usuário e o teste de cada versão.
- **Alunos do curso Claude Code: Criador de Apps.** Estão aprendendo a desenvolver com agente e querem instrução: um setup que pergunta pouco e um ciclo para seguir sem precisar inventar o próprio.
- **Quem já usa Claude Code com Superpowers ou as skills do Matt Pocock** e sente falta da camada de cima. Quer a governança sem trocar o que já usa.

## Proposta

Um plugin de Claude Code que monta a estrutura de documentos do projeto e conduz cada demanda da ideia até o relatório do que foi feito. Duas camadas:

- **Governança**, sempre a mesma: PRD, roadmap, demandas versionadas (arquivo no repositório ou issue do GitHub) e o registro do que saiu. Toda demanda passa por demanda → entrevista → implementação → fechamento.
- **Implementação**, à escolha: a governança escolhe o caminho de cada fase, e dentro da fase o framework escolhido roda inteiro. O aicf traz um caminho mínimo próprio e aceita Superpowers e Matt Pocock nas fases de entrevista e de implementação.

Seis skills, deliberadamente pequenas: dizem o que o agente não teria como inferir — onde gravar, o que registrar, quando fechar — e param aí.

## Escopo

**Dentro:**

- Setup de projeto novo: `PRD.md`, o lugar das demandas (arquivo ou issue) e o `CLAUDE.md` da raiz, com `AGENTS.md` como link.
- PRD por entrevista, revisado quando uma decisão o contraria.
- Roadmap e demandas versionadas, com a maturidade na pasta ou no label.
- Entrevista que produz spec, com sugestão de caminho de implementação.
- Caminho aicf mínimo de implementação, que encadeia o fechamento.
- Fechamento por qualquer caminho: checks, relatório, arquivamento e promoção de conhecimento para `CLAUDE.md`, ADR, `CONTEXT.md`, `docs/referencias/` ou skill.
- Superpowers e Matt Pocock como caminhos alternativos de entrevista e de implementação.

**Fora, por decisão:**

- **O caminho de implementação** (TDD, plano, subagentes, revisão de código). Fica com a coleção escolhida ou com o agente. Motivo: é o que as coleções fazem bem, e é onde um processo rígido é burlado. [ADR 0001](../adr/0001-fronteira-de-fase.md).
- **Migração entre arquivo e issue.** A escolha de mídia vale do ponto em diante; o que está em arquivo fica onde está. Motivo: migrar é uma demanda de conversão a manter, e ninguém pediu. [ADR 0004](../adr/0004-midia-do-registro-e-config-propria.md).
- **Manual ou tutorial separado do README.** Motivo: dois documentos humanos divergem; o que é para quem já usa fica dobrado no README. [ADR 0005](../adr/0005-a-documentacao-humana-e-um-arquivo-so.md).
- **Outros agentes (Codex, OpenCode, Cursor) como alvo.** O alvo é Claude Code. A porta fica aberta: o formato `SKILL.md` é o padrão aberto Agent Skills, que esses agentes leem (`curl -s https://agentskills.io/llms.txt` lista os clientes), e o setup já gera `AGENTS.md`. Mas o empacotamento é plugin de Claude Code, e a prosa cita ferramentas dele (`AskUserQuestion`, plan mode, `/clear`, `disable-model-invocation`) em cerca de vinte pontos (`grep -rnoE 'AskUserQuestion|plan mode|/clear|\.claude/rules|hooks?' skills/ --include='*.md' | wc -l`). Ninguém testou, e o plugin não promete. Motivo: o público é quem usa Claude Code, e cada agente a mais é uma superfície a manter sem quem a exercite.
- **A organização interna de `docs/referencias/`.** A pasta existe: o `/aicf:workflow-demanda` a nomeia para doc que descreve o mundo em vez de um trabalho a fazer, e o passo 3 do `/aicf:fechar-demanda` manda conhecimento operacional para lá (`grep -n 'docs/referencias' skills/workflow-demanda/SKILL.md skills/fechar-demanda/SKILL.md`). O que fica fora é o resto: o setup não a cria (nasce no primeiro arquivo, como `docs/adr/` e `CONTEXT.md`), e o plugin não impõe índice, nome de arquivo nem subpasta dentro dela. Motivo: o que tem padrão já tem lugar — decisão em ADR, vocabulário em `CONTEXT.md`, regra em `CLAUDE.md`, procedimento em skill —, e o que sobra (referência de serviço de terceiro, estudo, pesquisa) varia demais entre projetos para ter forma imposta. Esta entrada dizia que a pasta inteira era fora de escopo, contradizendo as duas skills; corrigido em 2026-09-19.
- **Trackers além do GitHub Issues** (Linear, Jira). Motivo: o plugin só carrega o que o autor usa e consegue testar, e até hoje foram só arquivo markdown e GitHub Issues. A mídia é uma linha de configuração, então acrescentar uma depois é possível, mas só quando houver quem a exercite.

## Modelo

**Gratuito, sustentado pelo curso.** O plugin é MIT e livre para todos. É material e vitrine do curso pago do AI Coding Flow, e é o curso que paga o tempo de manutenção.

## Sucesso

**O sinal que serve de prova hoje:** os projetos do autor rodam o ciclo inteiro, demanda → entrevista → implementação → fechamento, sem o processo ser burlado. Quando o autor contorna uma fase, o plugin falhou no que motivou sua criação. Verificação: em cada projeto que consome o plugin, toda demanda em `specs/concluidas/` (ou issue fechada) tem relatório de fechamento.

**A definir.** Uso por aluno sem ajuda, contribuição de fora e sobrevivência à troca de coleção são sinais plausíveis, mas ainda é cedo: o plugin foi exercitado com duas coleções e poucos projetos. Revisar esta seção quando houver alunos usando.

## Riscos

- **O processo pesa e é burlado.** É o que matou o primeiro framework do autor. Se acontecer: cada contorno vira demanda contra a skill que pesou, para simplificá-la, não exceção tolerada. As skills continuam pequenas por princípio.
- **Claude Code muda o formato de plugin ou de skill.** Se acontecer: o CI pina a versão do Claude Code e valida os manifestos; quando uma versão nova reprovar, subir o pin e corrigir o repositório na mesma release.
- **Uma coleção, ou a própria Anthropic, absorve a governança.** Se acontecer: comparar e aposentar a skill sobreposta. O aicf já delega a implementação; delegar mais uma fase é continuidade, não derrota.
- **Depende de uma pessoa só.** Manutenção e evolução dependem do tempo do autor, dividido com o curso e os projetos. Se acontecer: o repositório é público e MIT, a governança dele está em arquivo, e as skills são arquivos sem servidor. A última release continua funcionando sem manutenção, e quem quiser continua de onde parou.
