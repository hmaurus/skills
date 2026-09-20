# A profundidade da pasta quebra os links da demanda

Processo — entrevista: criar-spec · implementação: aicf-plan

## Problema

O estado de uma demanda é a pasta onde ela mora, e **duas das quatro pastas estão um nível abaixo
das outras**: `intents/backlog/` e `specs/concluidas/`. O `git mv` do passo 2 do fechamento desce
um nível, e todo link relativo que **sai** do arquivo passa a resolver errado — `../../adr/` vira
`../../../adr/`, `../intents/` vira `../../intents/`.

O ritual só ensina o sentido contrário. O passo 2 do `/aicf:fechar-demanda` e a linha "Corrigir
referências após mover" do `midia-arquivo.md` dão `grep -rn '<nome-do-arquivo>'`, que acha quem
**aponta para** o arquivo movido e não enxerga nada do que sai dele.

O dano é real e já foi pago: o commit `07cb4a9` consertou dois links de saída da demanda *as
skills carregam o que não vão usar*, depois que o CI acusou — e a mensagem dele registra a causa,
"o passo 2 procura quem aponta para o arquivo movido; os links que saem dele mudaram de base".
Quem o pegou foi o `scripts/check_links.py`, que existe **neste** repositório; num projeto que
instala o plugin e não tem check de links, o mesmo `git mv` quebra em silêncio.

A exposição de hoje se mede: **33 links relativos moram dentro das pastas fundas**
(`grep -rno '](\.\./[^)]*)' docs/projeto/specs/concluidas/*.md docs/projeto/intents/backlog/*.md | wc -l`)
e **17 links apontam para elas de fora**
(`grep -rno '](\([^)]*\)\(specs/concluidas\|intents/backlog\)[^)]*)' --include='*.md' . | wc -l`).
Todo fechamento passa por essa transição.

**Nenhuma das duas coleções vizinhas tem esse problema, porque nenhuma move o registro.** No
Superpowers 5.0.0, `grep -rc 'git mv' --include='*.md' ~/.claude/plugins/cache/superpowers-marketplace/superpowers`
não devolve uma ocorrência sequer: o design doc nasce em
`docs/superpowers/specs/YYYY-MM-DD-<topico>-design.md` e morre lá. No Matt Pocock 1.2.3 o estado é
um campo no corpo do arquivo, não o caminho dele —
`grep -n 'Status:' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.2.3/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md`
mostra `Status: claimed` para pegar o ticket e `Status: resolved` para encerrá-lo, com o arquivo
parado em `.scratch/<feature>/issues/NN-<slug>.md`.

O aicf é o único dos três que codifica o estado na profundidade do caminho, e é daí que o defeito
vem. A prova de que a profundidade é a causa, e não o movimento: `intents/` → `specs/` é o outro
`git mv` da governança, acontece na mesma frequência e **nunca quebrou um link de saída** — as duas
pastas estão no mesmo nível.

## Solução

As quatro pastas viram irmãs, sob `docs/projeto/`:

```
docs/projeto/
  backlog/      <- era intents/backlog/
  intents/
  specs/
  concluidas/   <- era specs/concluidas/
```

Com isso **nenhum `git mv` da governança muda de nível**, e todo `../` de dentro de uma demanda
continua resolvendo depois do movimento. A pasta segue sendo o estado, então o
[ADR 0003 — um item, um lugar](../../adr/0003-um-item-um-lugar.md) fica de pé: o que muda é o
aninhamento, não quem é a fonte da verdade.

O que sobra para o ritual é o sentido de entrada — quem apontava para o arquivo movido —, e para
esse o `grep -rn '<nome-do-arquivo>'` de hoje já serve. O parágrafo "Mover quebra link" do
`midia-arquivo.md` **encolhe** em vez de crescer: passa a falar de um sentido só, e some a frase
sobre a base mudar.

**A convenção de referência vira regra explícita.** A tabela do `midia-arquivo.md` já prescreve
`[título](../<pasta>/<nome>.md)`; achatado, é essa forma que garante a estabilidade — link para
irmão da mesma pasta escrito como `[título](<nome>.md)` continua quebrando no `git mv`, porque a
pasta de origem deixa de conter o alvo. A linha da tabela passa a dizer que a referência entre
demandas é **sempre** `../<pasta>/<nome>.md`, mesmo entre arquivos da mesma pasta.

**O `criar-spec` ganha a correção que nunca teve.** O `git mv` de `intents/` para `specs/` não
quebra link de saída, mas quebra quem apontava para `intents/<nome>.md` — e hoje a skill não manda
corrigir nada. Ela passa a apontar para a receita do `midia-arquivo.md`, que é onde o comando mora;
o passo 2 do `fechar-demanda` faz o mesmo, em vez de repetir o `grep` inline.

**Migração de quem já instalou:** as notas da versão explicam o layout novo e trazem os `git mv`
mais o `grep` de correção. O plugin é instrução, não código — projeto que não migrar continua
funcionando, com as skills falando de uma pasta que lá tem outro nome. O `/aicf:setup` não muda.

**Ponteiro dentro de arquivo imutável se reaponta; o texto não se toca.** O
[ADR 0005](../../adr/0005-a-documentacao-humana-e-um-arquivo-so.md) tem dois links relativos para
`../projeto/specs/concluidas/`, e o `CHANGELOG.md` tem um (linha 230). Nos três muda só o caminho
dentro dos parênteses — nenhuma palavra do texto. O que cita as pastas **em prosa ou dentro de
crase** fica como está: o comando `head -qn1` do ADR 0003 (linha 29) e as entradas antigas do
`CHANGELOG.md` descrevem o repositório da época, e o check de links não olha para dentro de crase.

A mudança pede **ADR próprio** — é difícil de reverter (16 arquivos movidos, convenção pública em
um plugin já na `0.19.0`) e tem trade-off real contra a alternativa do Matt. O ADR registra a
decisão, por que o estado continua na pasta em vez de virar campo, e que os ponteiros dos ADRs
anteriores foram reapontados sem o texto mudar.

## Arquivos e interfaces

| Arquivo | O que acontece |
|---|---|
| `docs/projeto/specs/concluidas/*.md` → `docs/projeto/concluidas/` | 12 arquivos, `git mv`; os `../` de dentro perdem um nível |
| `docs/projeto/intents/backlog/*.md` → `docs/projeto/backlog/` | 4 arquivos, `git mv`; idem |
| `skills/workflow-demanda/references/midia-arquivo.md` | tabela e parágrafo "Mover quebra link" reescritos: um sentido só, e a referência entre demandas sempre `../<pasta>/<nome>.md` |
| `skills/workflow-demanda/SKILL.md` | tabela dos quatro estados (linhas 73 e 76) com os caminhos novos |
| `skills/fechar-demanda/SKILL.md` | passo 2 com o caminho novo, apontando para a receita do `midia-arquivo.md` em vez de repetir o `grep` |
| `skills/criar-spec/SKILL.md` | o `git mv` de `intents/` para `specs/` passa a mandar corrigir quem apontava para o arquivo |
| `skills/setup/SKILL.md`, `skills/setup/templates/roadmap.md` | tabela de arquivos criados e o `head -qn1` do template com as quatro pastas |
| `README.md`, `README.en.md`, `docs/projeto/PRD.md`, `docs/projeto/ROADMAP.md` | a menção a `specs/concluidas/` vira `concluidas/`; no ROADMAP, também o `head -qn1` do topo |
| `CLAUDE.md` | dois links relativos para demandas concluídas |
| `docs/adr/0005-...md`, `CHANGELOG.md` | só o caminho dos ponteiros (2 + 1 links); texto intacto |
| `docs/referencias/governanca-nos-frameworks-vizinhos.md` | as menções ao layout |
| `docs/adr/000N-...md` | **novo.** O ADR do layout achatado |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | bump e entrada, pela sistemática de publicação |
| `docs/projeto/ROADMAP.md` | **já feito ao gravar esta spec:** a linha de `Próximas` saiu — quem tem arquivo não tem linha |

O `scripts/check_links.py` **não muda**: ele já resolve caminho relativo a partir do arquivo, e é o
juiz de cada passo da migração.

## Fora de escopo

- **O comando que confere os links de saída.** Foi escrito e testado nesta entrevista — `grep -o`
  dos destinos mais `test -e` — e cai com o achatamento: achatado, o único link de saída que ainda
  quebraria é o que aponta para irmão sem `../`, e a convenção da tabela cobre esse caso por
  escrito. Ele também carrega um custo medido: como não mascara bloco de código, acusou **3 falsos
  positivos** ao varrer os 14 arquivos de demanda, todos links de exemplo dentro de crase. Encerra
  se aparecer um movimento de pasta que a convenção não cubra.
- **Estado no corpo do arquivo, como o Matt.** Resolveria também o sentido de entrada, já que nada
  se moveria nunca. Descartado: tiraria "a pasta diz o estado" das skills, trocaria o `ls` de um
  estado por `grep`, e exigiria um ADR que supersedesse o 0003 — preço alto para o sentido que o
  `grep` de hoje já cobre.
- **O `/aicf:setup` detectar a estrutura antiga e propor migração.** As notas da versão bastam, e o
  `setup` tem `disable-model-invocation: true`: o comportamento não teria como ser verificado na
  sessão que o escrevesse.
- **Reescrever prosa histórica** no `CHANGELOG.md` e no comando do ADR 0003. Ponteiro se reaponta;
  relato do que uma versão fez fica como foi escrito.
- **Gerar check de links nos projetos que usam o aicf** — já fora de escopo por decisão de
  [nenhum teste acusa link morto](../concluidas/nenhum-teste-acusa-link-morto.md), e nada
  aqui muda isso.

## Verificação

1. **Provar que o defeito existe antes.** Medido nesta entrevista, e reproduzível enquanto o layout
   for o atual: `cp docs/projeto/specs/concluidas/as-skills-carregam-o-que-nao-vao-usar.md docs/projeto/specs/_teste-tmp.md`
   e rodar `python3 scripts/check_links.py` acusa **4 links quebrados** no arquivo copiado — os
   mesmos que o `git mv` do fechamento quebraria. Conferir que a cópia existe (`git status --porcelain`
   não vazio) antes de acreditar na saída, e `rm` no fim.
2. **Provar que o layout novo os elimina.** Com a migração feita, `git mv docs/projeto/specs/<qualquer>.md docs/projeto/concluidas/`
   seguido de `python3 scripts/check_links.py` devolve `0 quebrados` **sem editar um link sequer**,
   e `git diff --stat` mostra só o rename. Desfazer com `git mv` de volta.
3. `./scripts/check.sh` termina em `Tudo verde.`, com `N links conferidos, 0 quebrados` e os dois
   `✔ Validation passed`.
4. `grep -rn 'specs/concluidas\|intents/backlog' --include='*.md' .` devolve **apenas** o texto
   histórico deliberado: o comando do ADR 0003, as entradas antigas do `CHANGELOG.md` e a prosa das
   demandas em `concluidas/`. Qualquer outra linha é caminho esquecido. **As concluídas entraram
   nessa lista na implementação**: a spec as tinha esquecido, e elas caem no mesmo princípio que o
   `CHANGELOG.md` — ponteiro se reaponta, relato do que uma versão fez fica como foi escrito.
5. Depois do push, `gh run list --workflow=ci.yml --limit 1` → `completed success`.
