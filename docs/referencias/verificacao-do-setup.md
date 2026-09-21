# Verificação de comportamento do `/aicf:setup`

O que cada passada tem que provar, o que já passou, e o que ainda não rodou.

## Por que este doc existe

O `skills/setup/SKILL.md` tem `disable-model-invocation: true`: o harness recusa a invocação e também
imitar o roteiro por fora. **Nenhum agente verifica essa skill** — quem roda é o titular, e a demanda
que a altera fecha com a verificação em aberto e nomeada.

Isso se repete a cada mudança do setup, e a condição de aceite acabou espalhada por quatro demandas
concluídas. Aqui ela fica junta.

## Antes de qualquer passada

1. `/plugin update`, e **sessão nova** — a skill que roda é a carregada no início da sessão, não a do
   disco.
2. Conferir o cabeçalho do comando: `cache/aicodingflow/aicf/<versão>/skills/setup`. Sem isso, a
   passada pode estar exercitando a versão anterior.
3. **Diretório novo.** O setup roda uma vez por projeto, e não migra projeto que já tem governança.

## O que cada ramo prova

### Modo arquivo

```bash
git log --oneline | wc -l                    # 1
git show --stat --name-only HEAD             # só o que o setup escreveu
git branch --show-current                    # develop
git branch --format='%(refname:short)'       # develop, main
ls docs/projeto/                             # PRD.md, ROADMAP.md e as quatro pastas
grep '^\*\*Coleções' CLAUDE.md               # "Superpowers" uma vez só na linha
grep -n 'develop' CLAUDE.md                  # a seção Git descreve o que existe
grep -n 'Repositório' docs/projeto/ROADMAP.md  # "Repositório no GitHub e CI mínimo"
```

### Modo issue

```bash
gh label list | grep -c '^aicf:'                                # 3
git log origin/main --oneline | wc -l                           # 1 — o --push funcionou
gh repo view --json defaultBranchRef -q .defaultBranchRef.name  # main
git branch --show-current                                       # develop
ls docs/projeto/                                                # só PRD.md
gh repo delete <nome> --yes                                     # o repositório de teste é descartável
```

O repositório sai da máquina, então é privado e some no fim. `gh label list` num repositório criado
pelo próprio setup é a condição que encerra o ramo issue.

## O que já passou

| Quando | Ramo | Versão | Resultado |
| --- | --- | --- | --- |
| 2026-09-20 | arquivo | `0.23.0` | **passou** — um commit, só os caminhos criados, `git init` oferecido antes da pergunta da mídia, e a pergunta da mídia feita com a opção issue dizendo o que faltava |
| — | issue | — | **nunca rodou** |

**A passada de 2026-09-20 achou três defeitos que nenhuma revisão tinha achado** — todos nos
templates, nenhum no roteiro. Viraram a `0.23.1`
([os templates contradizem o projeto que nasce](../projeto/concluidas/os-templates-contradizem-o-projeto-que-nasce.md)).
É o argumento para rodar a passada de verdade em vez de confiar em leitura: o `check.sh` estava
verde, e um subagente tinha revisado o diff inteiro.

## O que está em aberto

**O ramo issue nunca rodou.** Encerra com o bloco de comandos acima; a condição nasceu em
[a profundidade da pasta quebra os links](../projeto/concluidas/a-profundidade-da-pasta-quebra-os-links.md)
e foi herdada por
[o setup entrega projeto sem repositório](../projeto/concluidas/o-setup-entrega-projeto-sem-repositorio.md).

**O ramo arquivo passou na `0.23.0`, e o setup mudou duas vezes desde então.** A passada não
exercitou nem os templates corrigidos (`0.23.1`) nem a criação da `develop` (`0.24.0`). As duas
mudanças valem nos dois modos, então uma passada do ramo issue cobre quase tudo — **menos o
`ROADMAP.md`**, que no modo issue não existe. Essa linha está provada por `grep` e pelo diff, e
encerra de vez na próxima passada em modo arquivo.
