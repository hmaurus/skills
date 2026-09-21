# O setup entrega a branch de trabalho, em vez de só descrevê-la

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

A `0.23.1` tirou `develop` do template do `CLAUDE.md` porque o arquivo gerado descrevia um fluxo de
duas branches num repositório que o `git init` cria com uma. A correção estava certa sobre a
contradição e errada sobre qual lado ajustar: **o titular trabalha com `develop`/`main` nos projetos
dele e quer que quem aprende pelo plugin comece assim.**

Voltar o texto sozinho recria o defeito por escolha: o `CLAUDE.md` diria de novo "`develop` — branch
de trabalho" num repositório onde `git branch` lista só `main`, e o primeiro commit do setup
continuaria indo para a branch que o template chama de produção.

## Solução

O setup **cria as duas branches**, e o template volta a descrevê-las porque passam a existir.

A ordem é o que faz funcionar, e vale nos dois modos:

1. `git init`, os arquivos, e o primeiro commit — que cai em `main`.
2. **Só no modo issue:** `gh repo create --source=. --remote=origin --push`. Roda com `main` ativa,
   então é `main` que sobe primeiro e fica sendo o default do repositório no GitHub.
3. **Só no modo issue:** os três labels.
4. `git branch develop` e `git switch develop`. No modo issue, mais `git push -u origin develop`.

O passo 4 é o último antes do fechamento, e é o que garante os dois resultados: `main` como default
no GitHub, e `develop` como branch ativa na máquina — que é onde a primeira demanda vai commitar.

Inverter 2 e 4 é o jeito de errar: com `develop` ativa na hora do `gh repo create`, é ela que sobe
primeiro e vira o default do repositório remoto.

O template do `CLAUDE.md` volta a trazer `develop`/`main`, agora dizendo que o setup já as criou.

## Arquivos e interfaces

- `skills/setup/SKILL.md` — a seção "O primeiro commit" ganha o passo da branch de trabalho, e o
  passo entra na ordem descrita em "O repositório no GitHub, e os labels".
- `skills/setup/templates/claude-md.md` — a seção `## Git` volta ao fluxo de duas branches.
- `README.md`, `README.en.md` — a descrição do comando diz o que ele entrega.
- `.claude-plugin/plugin.json`, `CHANGELOG.md` — em par.

## Fora de escopo

- **Perguntar se o usuário quer uma branch ou duas.** Decidido: cria sempre. Quem quiser uma só
  apaga a `develop` com um comando, e o roteiro não ganha pergunta.
- **`git flow`, release branches, proteção de branch no GitHub.** O setup entrega as duas branches,
  e nada além disso.
- **Migrar projeto que já rodou o setup.** Quem montou a governança na `0.23.x` cria a `develop` na
  mão; as notas da versão trazem os dois comandos.

## Verificação

1. Num diretório novo, a sequência que o roteiro descreve deixa o estado certo:

   ```bash
   git branch --show-current              # develop
   git branch --format='%(refname:short)' # develop, main
   git log main --oneline | wc -l         # 1 — o commit do setup está em main
   ```

2. Com remoto, `main` é a primeira a subir e continua sendo o HEAD do remoto depois que a `develop`
   entra — conferido contra um bare local antes de esta spec fechar, e no GitHub de verdade pela
   passada do ramo issue.

3. O template voltou, e agora corresponde ao que o setup entrega:

   ```bash
   grep -c 'develop' skills/setup/templates/claude-md.md  # 0 hoje, 1 depois
   grep -c 'git branch develop' skills/setup/SKILL.md     # 0 hoje, 1 depois
   ```

4. `./scripts/check.sh` termina em `Tudo verde.` e sai com 0.

5. Ponta a ponta, do titular, pelo `disable-model-invocation: true`: a passada do ramo issue que a
   demanda [o setup entrega projeto sem repositório](../concluidas/o-setup-entrega-projeto-sem-repositorio.md)
   deixou em aberto passa a provar também isto — `develop` ativa ao fim, e `main` como default branch
   do repositório recém-criado (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`).


## Relatório de implementação (2026-09-21)

**Status** — concluído. As Verificações 1 a 4 rodaram e passaram. A 5 é a passada do ramo issue,
do titular pelo `disable-model-invocation: true`, e agora prova três demandas de uma vez.

**Causa raiz** — não é bug: é uma decisão de projeto que a `0.23.1` tomou na direção errada por
falta de um dado que só o titular tinha. Ela viu a contradição certa — `CLAUDE.md` descrevendo
`develop` num repositório de uma branch — e escolheu ajustar o texto, porque o critério à mão era
"descrever o que existe". O critério que faltava era que o fluxo de duas branches é o que o plugin
quer ensinar, e aí quem se ajusta é o repositório.

**Arquivos alterados**

| Arquivo | O quê |
| --- | --- |
| `skills/setup/SKILL.md` | nasce "A branch de trabalho", último passo antes do fechamento; "O primeiro commit" diz que cai em `main` e aponta para lá; a `description` e o fechamento acompanham |
| `skills/setup/templates/claude-md.md` | `## Git` volta a `develop`/`main`, dizendo que o setup criou as duas e em qual você está |
| `README.md`, `README.en.md` | a descrição do comando diz o que ele entrega |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.24.0`, em par |

**Commits**

| Sha | O quê |
| --- | --- |
| `41743eb` | a demanda nasce pronta para implementar |
| `3b51450` | o passo da branch, o template de volta, READMEs, versão e CHANGELOG |

**Validação**

- `./scripts/check.sh` — `Tudo verde.`, `108 links conferidos, 0 quebrados`.
- Verificação 1 e 2, rodadas contra um remoto local com a sequência exata do roteiro: `develop`
  ativa, as duas branches locais, um commit em `main`, e `git symbolic-ref HEAD` no remoto em
  `refs/heads/main` **depois** de a `develop` subir.
- Verificação 3 — `grep -c 'develop' skills/setup/templates/claude-md.md` e
  `grep -c 'git branch develop' skills/setup/SKILL.md` devolvem `0` em `f67e76e` e `1` aqui.
- **Sem revisão de código externa**: a mudança é um passo de roteiro de cinco linhas mais a
  restauração de uma linha de template, e a ordem — que é a parte que poderia errar — foi executada
  em vez de julgada.

**Escopo efetivo** — igual à spec, mais os dois READMEs e a `description` da skill, que descrevem o
comando e ficariam desatualizados.

**Lições**

- **"Descrever o que existe" e "existir o que se quer descrever" resolvem a mesma contradição, e a
  escolha entre as duas não está no código.** A `0.23.1` tinha todos os fatos e ainda assim escolheu
  errado, porque o dado que decide — qual fluxo o plugin quer ensinar — mora no titular e não no
  repositório. O sintoma de que a escolha é dessa família: os dois lados deixam o repositório
  coerente, e só um deles ensina o que se quer ensinar. Vale a pena perguntar quando aparecer de
  novo, em vez de adotar o lado mais barato.
- **Versão revertida em parte no mesmo dia não é retrabalho perdido.** A `0.23.1` pagou o custo de
  achar a contradição — que estava invisível havia meses e só a passada real expôs. A `0.24.0`
  aproveitou o achado inteiro e trocou só a direção da correção.

**Saída do passo 3** — nenhuma. Nenhum ADR: a decisão se reverte apagando uma branch e uma linha, e
o [ADR 0007](../../adr/0007-o-setup-age-fora-do-disco-local.md) já cobre o que era difícil de
reverter aqui — o setup agir no repositório do usuário. Nenhuma regra nova no `CLAUDE.md`: a lição
acima é sobre uma escolha que se faz uma vez, não sobre um erro que se repete. Nenhuma demanda nova,
e nenhuma tornada obsoleta.
