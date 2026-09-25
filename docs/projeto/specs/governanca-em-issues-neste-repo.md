# Sugestão de fora entra por issue, e a governança fica em arquivo

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (template, uma linha de receita e dois READMEs, sem decisão de abordagem)

## De onde veio

Esta demanda nasceu como *"a governança deste repositório passa a viver em issues, e assume ser
pública"*: migrar intents, specs e concluídas para issues do GitHub, consumindo o modo issue criado
em [escolher entre arquivos e issues](../concluidas/escolher-entre-arquivos-e-issues.md). A
entrevista de 2026-09-24 **descartou a migração** e manteve o problema.

O texto anterior está no histórico: `git show d59afc8:docs/projeto/intents/governanca-em-issues-neste-repo.md`.
Por que a migração saiu:

- **O único argumento que sobrou não precisa dela.** A própria intent já tinha perdido o índice
  gerado (ver [o `CHECKLIST.md` sai do método](../concluidas/o-checklist-sai-do-metodo.md)), e o
  que restava era permitir que alguém de fora contribuísse. Para isso basta a issue servir de
  entrada, não de registro.
- **O custo cresceu.** A teia de links relativos entre demandas quebra inteira numa migração
  (`grep -rno '\](\.\./[^)]*\.md' docs/projeto/*/*.md | wc -l` remede), e o relatório como
  comentário de issue some do `git clone`, contra o *"quem precisa saber é o repositório"*.
- **O repositório é o exemplo vivo do modo arquivo**, que o README apresenta primeiro.

## Problema

Quem usa o plugin e quer sugerir um ajuste não tem caminho declarado. As issues do repositório
estão habilitadas (`gh repo view hmaurus/skills --json hasIssuesEnabled` → `true`), mas nada diz
que pode abri-las nem o que acontece depois, e nenhuma foi aberta até hoje
(`gh issue list --state all --limit 1` sai vazio).

O método tem a mesma lacuna. A tabela Arquivo × Issue do README diz que, no modo arquivo, a
contribuição de fora é por **pull request**. Qualquer projeto em modo arquivo com repositório
público recebe issue do mesmo jeito, e a receita do modo arquivo não diz o que o agente faz com
ela.

## Solução

**A issue de fora é entrada, não registro.** Na triagem ela vira arquivo, ou é recusada, e nos dois
casos é fechada. O estado da demanda continua morando só em `docs/projeto/`, e a regra de revisão
"dois mecanismos coexistindo" não se aplica, porque a issue não guarda estado.

1. **Receita do modo arquivo:** uma linha nova na tabela de operações:
   - **Aceita:** vira arquivo em `backlog/` ou `intents/`, com a linha `Origem: #<n>` logo abaixo
     da linha `Processo`. Depois `gh issue close <n> --comment "<permalink>"`, e o permalink
     aponta para o arquivo **no sha do commit que o criou** (`/blob/<sha>/...`). É um link fixo,
     e o arquivo muda de pasta ao longo do ciclo. Link para `main` quebraria no primeiro `git mv`.
   - **Recusada:** `gh issue close <n> --reason "not planned" --comment "<motivo>"`.
   A triagem já é gatilho do `/aicf:workflow-demanda` ("Consultar ao começar, triar ou registrar
   uma demanda"), e é ele que manda ler a receita da mídia.
2. **Template de issue deste repositório:** um único issue form bilíngue pt/en,
   `.github/ISSUE_TEMPLATE/sugestao.yml`. O campo obrigatório é o **problema**, do ponto de vista
   de quem usa, no formato de uma intent. O opcional é o **contexto**: versão do plugin, comando,
   o que esperava. Não aplica label.
3. **README (pt e en):**
   - A célula "Contribuição de fora" da coluna Arquivo troca "pull request" por algo como
     "issue como entrada, triada para arquivo".
   - A seção `## Sobre` ganha uma frase dizendo que sugestões entram por issue.
4. **Versão patch** (`0.29.4`), com a entrada no `CHANGELOG.md`, porque a receita é conteúdo de
   skill.

## Arquivos e interfaces

- `skills/workflow-demanda/references/midia-arquivo.md`: a linha nova na tabela de operações
- `.github/ISSUE_TEMPLATE/sugestao.yml`: arquivo novo. Antes de escrever, conferir a sintaxe de
  issue forms na doc do GitHub (`name`, `description`, `body` com `type: textarea` e
  `validations.required`)
- `README.md` e `README.en.md`: a célula da tabela e a frase em `## Sobre` / `## About`
- `.claude-plugin/plugin.json` → `0.29.4`, e a entrada do `CHANGELOG.md`

## Fora de escopo

- **Migrar a governança para issues.** Descartada, pelos motivos em *De onde veio*.
- **Template de bug separado.** Bug de comportamento de skill também é sugestão de ajuste, e a
  triagem separa os dois. Dois arquivos para manter sem ganho.
- **`config.yml` que desliga issue em branco.** Quem só quer perguntar não deve esbarrar em campo
  obrigatório.
- **Issue aberta até a demanda concluir.** Poria o estado em dois lugares. Quem sugeriu acompanha
  pelo permalink.
- **`CONTRIBUTING.md`.** A frase em `## Sobre` basta enquanto o fluxo cabe numa frase.
- **Mudança no modo issue.** Lá a issue de fora já é adotada por `/aicf:criar-spec #<n>`.
- **Labels no template.** Nenhuma triagem depende de label, e as `aicf:*` são do modo issue.

## Verificação

1. `./scripts/check.sh` termina em `Tudo verde.`.
2. A receita tem a linha e o README não diz mais "pull request":
   ```
   grep -c 'gh issue close' skills/workflow-demanda/references/midia-arquivo.md   # 2 (hoje 0)
   grep -c 'Contribuição de fora | pull request' README.md                        # 0 (hoje 1)
   grep -c 'Outside contribution | pull request' README.en.md                     # 0 (hoje 1)
   ```
3. Depois do push, `https://github.com/hmaurus/skills/issues/new/choose` mostra o formulário
   *Sugestão / Suggestion*. O GitHub exibe o erro de validação na própria página quando o YAML do
   form é inválido. Conferir no navegador.
4. **A triagem ponta a ponta fica em aberto** até a primeira issue real de fora ser triada pela
   receita. Não vale abrir issue de teste num repositório público só para isso. O relatório de
   fechamento registra esta condição, e ela se encerra quando existir em `docs/projeto/` um arquivo
   com `Origem: #<n>` (`grep -rln '^Origem: #' docs/projeto/` não vazio).
