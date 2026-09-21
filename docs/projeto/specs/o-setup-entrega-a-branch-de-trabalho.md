# O setup entrega a branch de trabalho, em vez de só descrevê-la

Processo — entrevista: nenhuma · implementação: a definir · sugestão: aicf-direto (o roteiro ganha um passo curto, e o template volta ao que era)

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
