# O aicf promete qualquer caminho e integra dois

Processo — entrevista: grill-with-docs · implementação: a definir · sugestão: aicf-plan (cerca de vinte arquivos de prosa e um SVG numa sessão, com ordem entre eles e sem TDD)

## Problema

O README, o PRD, o glossário e as skills apresentam o aicf como uma camada que funciona "por cima
do caminho de implementação que você já usa" e "igual em qualquer caminho". Na prática, ele integra
só o Superpowers e as skills do Matt Pocock, e cada integração exigiu um acoplamento específico: o
[ADR 0008](../../adr/0008-o-aicf-escreve-a-convencao-no-tracker-do-matt.md) escreve a convenção do
aicf no tracker do Matt, e o `CLAUDE.md` tem regras próprias para o `brainstorming` e o
`grill-with-docs`. Quem chega com spec-kit, GSD ou outra coleção lê uma promessa que o plugin não
cumpre.

O nome da camada também atrapalha. "Governança" tem usos consolidados em TI que não são este:
governança de TI (COBIT, ISO/IEC 38500), o `GOVERNANCE.md` de projeto open source no GitHub e,
principalmente, governança de IA e de agentes (políticas, permissões, auditoria). A `description`
do `plugin.json`, "Governança de projeto para desenvolver com agentes", parece de ferramenta de
compliance. E a palavra nomeia duas coisas no repositório: a camada do aicf
(`skills/ajuda/SKILL.md:9`) e o conjunto das demandas registradas ("uma issue de fora da governança
entra nela", `skills/midia/issues.md:103`).

Medido antes da mudança, sobre os arquivos vivos
(`V="README.md .claude-plugin skills .claude/CLAUDE.md docs/projeto/PRD.md docs/projeto/ROADMAP.md docs/projeto/intents docs/projeto/backlog docs/assets/hero.svg docs/referencias"`):
`grep -rni 'governan' $V | grep -v 'governanca-nos-frameworks-vizinhos' | wc -l` → 58, e
`grep -rni 'qualquer caminho\|caminho que você já usa\|caminhos de fora' $V | wc -l` → 14.

## Solução

O aicf passa a se apresentar como o que é: **integra gestão de produto e engenharia de software,
conduzindo o ciclo de vida de cada demanda, do registro ao fechamento**. Superpowers e Matt Pocock
são as duas maiores coleções de skills de engenharia no GitHub; o aicf une as duas e acrescenta por
cima o PRD, o roadmap, o registro de demandas e o relatório do que saiu. O caminho aicf continua,
como caminho mínimo para quem não instalou as coleções.

Lema, só na abertura do README: *"Você não precisa escolher entre Superpowers e Matt Pocock:
escolha os dois, com o aicf."* É a única frase de efeito do README, como exceção declarada.

O vocabulário novo já está no [`GLOSSARY.md`](../../../GLOSSARY.md), gravado durante a entrevista:
**gestão de produto**, **engenharia de software**, **registro de demandas**, **ciclo de vida da
demanda**, e **caminho** com o **caminho aicf** dentro dele.

## Histórias

1. Como quem chega pelo README, quero ler na primeira tela que o aicf une Superpowers e Matt
   Pocock, para saber logo se ele serve ao que eu uso.
2. Como quem usa spec-kit, GSD ou outra coleção, quero que nenhum texto do aicf prometa integrar o
   meu caminho, para não instalar esperando algo que não acontece.
3. Como quem usa Superpowers e Matt Pocock, quero ler que posso entrevistar por um e implementar
   pelo outro, para saber que não preciso escolher.
4. Como quem não instalou nenhuma das duas coleções, quero saber que o caminho aicf mínimo funciona
   sozinho, para começar sem instalar nada.
5. Como quem procura no marketplace, quero que a `description` do plugin fale em gestão de produto
   e nas duas coleções, sem "governança", para não confundi-lo com ferramenta de compliance de
   agente.
6. Como quem lê o README em inglês, quero o mesmo posicionamento com os termos *product
   management*, *software engineering*, *work item registry* e *work item lifecycle*.
7. Como quem roda o `/aicf:setup` sem as coleções, quero que a sugestão de instalá-las diga que o
   aicf foi feito para unir as duas, e que ele continue aceitando "nenhum" e não instale nada.
8. Como agente que lê uma skill do aicf, quero o vocabulário do glossário em toda skill, para não
   tratar "gestão de produto" e "registro de demandas" como a mesma coisa.
9. Como agente num projeto novo, quero que o `CLAUDE.md` gerado pelo template diga "gestão de
   produto", "engenharia de software" e "o aicf fecha a demanda", sem "governança".
10. Como titular de um projeto que já usa o aicf, quero nas notas da release um pedido pronto para
   colar no agente, que compare a seção "Processos de desenvolvimento" do meu `CLAUDE.md` com o
   template novo e me traga o diff, para atualizar a prosa sem perder o que personalizei.
11. Como titular de um projeto que já usa o aicf, quero que o meu `CLAUDE.md` antigo continue
   funcionando sem eu mexer nele, porque nenhuma skill procura a palavra "governança" nele.
12. Como quem mantém o plugin, quero um ADR que registre por que o aicf deixou de se dizer agnóstico,
   para que a próxima sessão não volte a prometer "qualquer caminho".
13. Como quem mantém o plugin, quero que o histórico (entradas antigas do `CHANGELOG.md`,
   `concluidas/`, ADRs 0001 a 0008, notas de sessão, pareceres do Codex) **não** mude, porque
   registra o que valia quando foi escrito.
14. Como quem lê o PRD, quero que Problema, Público, Proposta e "Fora, por decisão" digam que o aicf
   integra Superpowers e Matt, e que outras coleções ficam fora por decisão, com o motivo.
15. Como quem vê a imagem do README, quero gestão de produto no topo, o aicf no meio conduzindo o
   ciclo de vida da demanda, e as coleções de engenharia embaixo, sem "por qualquer caminho".
16. Como quem desconfia do "maiores no GitHub", quero o número com o comando que o confere e a data,
   para conferir sozinho.

## Decisões de implementação

- **Termos e convenção editorial.** "Gestão de produto" sem artigo para a disciplina e para a
  camada; "gestão do produto" quando se fala de um produto específico; títulos em caixa de frase,
  como o resto do repositório. Convenção editorial, sem rigidez.
- **O segundo sentido de "governança" não vira "gestão de produto".** Conforme o contexto:
  *demanda registrada* (uma demanda), *registro de demandas* (o conjunto), *ciclo de vida da
  demanda* (entrada, passagem entre fases e fechamento), *estrutura do projeto* (arquivos e
  pastas, inclusive no commit do setup: `chore: estrutura do projeto`). Não se cria termo para
  "fluxo de demandas".
- **A gestão de produto cobre PRD, roadmap, registro de demandas e relatório.** Conduzir o ciclo
  (escolher o caminho de cada fase, fazer a passagem entre elas) tem como sujeito **o aicf**: "a
  passagem entre fases é do aicf", "o método escolhido fecha o código; o aicf fecha a demanda".
- **A outra camada é engenharia de software.** "Implementação" volta a ser só o nome de uma fase.
- **Caminho continua sendo de uma fase.** A prosa diz "caminho de entrevista" ou "caminho de
  implementação"; o do próprio aicf é o **caminho aicf**, e "mínimo" entra como adjetivo, não como
  nome.
- **ADR 0009**, `docs/adr/0009-o-aicf-integra-superpowers-e-matt.md`: a virada de agnóstico para
  integrar duas coleções, as alternativas (agnóstico como estava; integrar mais coleções), e a troca
  de termo com a observação de que o vocabulário dos ADRs 0001 a 0008 fica como está. O ADR 0001
  continua valendo: a independência entre as fases é o que permite entrevistar por uma coleção e
  implementar pela outra.
- **PRD editado direto**, nesta demanda, citando o ADR 0009: o parágrafo "só faz sentido quando não
  depende do caminho de implementação", "sobreviva à troca de ferramenta" no Público, as duas
  camadas da Proposta, o "Fechamento por qualquer caminho" do Escopo, e uma entrada nova em "Fora,
  por decisão": outras coleções de skills, porque integrar cada uma exige acoplamento específico
  (ADR 0008), e acrescentar uma só quando houver quem a exercite.
- **README em pt e en.** Abertura com o lema e o parágrafo da Solução; sai o spec-kit da abertura;
  o número de estrelas entra com o comando e a data (em 2026-10-20: `obra/superpowers` 302.590,
  `mattpocock/skills` 298.641, `github/spec-kit` 142.143, por
  `gh api repos/<repo> --jq .stargazers_count`). A seção "Por que este, e não…" troca "cuida só da
  governança" pelo novo posicionamento; a comparação com GSD e BMAD continua.
- **Manifestos.** `description` do `plugin.json` e do plugin no `marketplace.json`: "Gestão de
  produto e ciclo de vida da demanda para Claude Code, integrando Superpowers e Matt Pocock: PRD,
  roadmap, registro de demandas e o relatório do que foi feito." A `description` do marketplace
  segue a mesma linha. `keywords`: sai `governanca`, entram `gestao-de-produto`, `superpowers` e
  `mattpocock`.
- **Skills e template.** `ajuda`, `setup` (com `ferramentas.md` e `templates/claude-md.md`),
  `criar-spec`, `implementar-spec`, `fechar-demanda` e `midia/issues.md` trocam o vocabulário. No
  `ferramentas.md`, só a frase de explicação da sugestão de coleções muda; a mecânica (sugere,
  aceita "nenhum", não instala) fica.
- **`.claude/CLAUDE.md` deste repositório** acompanha o template.
- **`hero.svg` redesenhado à mão**: três faixas — Gestão de produto (o quê e por quê; PRD ·
  roadmap · registro de demandas · relatório) no topo, a faixa do aicf (integração e condução do
  ciclo de vida da demanda) no meio, e Engenharia de software (como construir) embaixo, com
  Superpowers e Matt Pocock e o caminho aicf menor ao lado. `<title>` e `<desc>` acompanham. O
  banner fica como está.
- **Doc de referência** `docs/referencias/governanca-nos-frameworks-vizinhos.md`: o texto troca o
  vocabulário; o nome do arquivo fica.
- **Registro aberto** (`intents/`, `backlog/`, `ROADMAP.md`) troca o vocabulário onde aparece.
- **Projetos existentes.** As notas da release levam o pedido para colar no agente: *"Compare a
  seção 'Processos de desenvolvimento' do CLAUDE.md com `skills/setup/templates/claude-md.md` do
  aicf 0.42.0 e me traga o diff, mantendo o que este projeto personalizou."* A intent
  [o setup não serve a projeto já rodando](../intents/o-setup-nao-serve-a-projeto-ja-rodando.md)
  ganha esta troca como caso concreto em "O que já se sabe".
- **Versão `0.42.0`**, com a entrada do `CHANGELOG.md` no commit de código.

## Fora de escopo

- **Integrar outras coleções** (spec-kit, GSD, BMAD). Cada uma exige acoplamento específico; entra
  só quando houver quem a exercite.
- **Reescrever o histórico.** Entradas antigas do `CHANGELOG.md`, `concluidas/`, ADRs 0001 a 0008,
  `docs/notas-de-sessao/` e `docs/agente-codex/` registram o que valia quando foram escritos.
- **Renomear `docs/referencias/governanca-nos-frameworks-vizinhos.md`.** O nome descreve a
  pesquisa como ela foi feita, e os links para ele seguem valendo.
- **O banner** (`docs/assets/banner*.png`). É imagem rasterizada e pede outra demanda.
- **Atualizar o `CLAUDE.md` dos projetos existentes por skill.** Detectar prosa antiga é impreciso e
  a regra ficaria para sempre na skill; o caminho geral é a intent do setup para projeto já
  rodando.
- **Mudar a mecânica do setup** para instalar coleções. Ele sugere e aceita "nenhum".

## Verificação

Com `V` como no Problema:

1. `./scripts/check.sh` → termina em `Tudo verde.`
2. `grep -rni 'governan' $V | grep -v 'governanca-nos-frameworks-vizinhos' | wc -l` → 0 (era 58).
3. `grep -rni 'qualquer caminho\|caminho que você já usa\|caminhos de fora' $V | wc -l` → 0 (era 14).
4. `grep -ci 'governance' README.en.md` → 0 (era 6), e
   `grep -ci 'any path\|any implementation path\|paths from outside' README.en.md` → 0 (era 5).
5. `grep -c 'Superpowers, Matt Pocock e spec-kit' README.md` e
   `grep -c 'Superpowers, Matt Pocock and spec-kit' README.en.md` → 0 cada (era 1).
6. `grep -c '"gestao-de-produto"' .claude-plugin/plugin.json .claude-plugin/marketplace.json` → 1
   em cada (era 0).
7. `test -f docs/adr/0009-o-aicf-integra-superpowers-e-matt.md` passa.
8. `grep -c '0.42.0' docs/projeto/intents/o-setup-nao-serve-a-projeto-ja-rodando.md` → ≥ 1 (era 0).
9. `python3 -I -c "import sys,xml.dom.minidom as m; m.parse(sys.argv[1]); print('svg-ok')" docs/assets/hero.svg`
   → `svg-ok`, e um screenshot do `hero.svg` em tema claro e escuro mostra as três faixas legíveis
   nos dois.
10. `agy plugin validate .` → `✔ Validation passed`, sem `only the first 24000 are loaded`.
11. Depois da release:
    `gh release view v0.42.0 --json body --jq .body | grep -c 'templates/claude-md.md'` → 1.
