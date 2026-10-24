# O caminho do Matt depois do `/to-tickets`

Lido pelo `implementar-spec`, no passo 3, ao voltar do `/to-tickets` ou retomar uma spec com
tickets, antes de escolher a forma.

O Matt tem duas formas de executar os tickets: `/implement`, um ticket por sessão, ou
`/implement-spec`, o grafo inteiro numa execução, com subagentes em paralelo, cada um na sua
worktree, juntos numa branch de integração. A forma se escolhe aqui, com o grafo à vista.

## Os dois pontos de entrada

- **De volta do `/to-tickets`, na mesma sessão.**
- **Retomada:** `/aicf:implementar-spec <spec>` numa sessão nova, quando a spec já tem tickets — no
  modo arquivo, arquivos em `.scratch/<feature>/issues/` com a linha `**Spec:**` apontando para
  ela; no modo issue, issues com `## Parent` apontando a issue da spec. Não entregar o
  `/to-tickets` de novo nem criar ticket: ir direto à medição. É a exceção à regra de que a skill
  para ao entregar o caminho de uma coleção.

## Medir

Ler os tickets e medir quatro coisas. **Fronteira** é o conjunto de tickets sem bloqueio pendente.

1. A largura da fronteira, em cada ponto do grafo.
2. Se dois tickets da mesma fronteira tocam o mesmo arquivo.
3. Quantos tickets geram migration.
4. Se a verificação de algum ticket depende de `.env`, banco ou pasta no gitignore.

## Escolher a forma

Com as medidas, recomendar a forma numa pergunta com opções (`AskUserQuestion` no Claude Code):

- **`/implement` por ticket** é o padrão. O titular conduz cada ticket e lê o trabalho de cada um
  ao terminar.
- **`/implement-spec`** quando a spec se divide em **4 ou mais tickets com pelo menos 2 prontos ao
  mesmo tempo** em algum ponto do grafo. Sem grafo de verdade, `/implement`.

Pesam contra o `/implement-spec`, e viram aviso na pergunta: arquivo compartilhado entre tickets
da mesma fronteira; migration em mais de um ticket; verificação que depende de estado não
versionado. O custo dele: o titular revisa a branch de integração inteira no fim, e precisa de
cota de uso para vários subagentes ao mesmo tempo.

Escolhido o `/implement`, entregar o comando do primeiro ticket da fronteira —
`/implement .scratch/<feature>/issues/<NN>-<slug>.md`, ou `/implement #<ticket>` — e esperar.

## Escolhido o `/implement-spec`

### 1. Editar os tickets

O implementador só lê o próprio ticket. Propor a edição, mostrar o diff e aplicar com o aceite do
usuário:

- **Dois tickets da mesma fronteira que tocam o mesmo arquivo:** bloqueio entre eles, ou os nomes
  que cada um acrescenta fixados nos dois. A worktree não evita a colisão, só a adia para o merge.
- **Migration em mais de um ticket da mesma fronteira:** bloqueio, para que elas não rodem em
  paralelo contra o mesmo banco.
- **Ticket cuja verificação depende de estado não versionado:** a linha
  `**Verificação no checkout principal:** <comando> — na worktree ela não roda; reportar isso em vez de verde.`
  Na worktree, o teste que lê arquivo no gitignore é pulado em silêncio.

**Bloqueio, por mídia:**

- **Arquivo:** a linha `Blocked by: NN, NN` do ticket.
- **Issue:** a dependência nativa do GitHub, como o tracker do Matt a descreve:

  ```bash
  gh api repos/<owner>/<repo>/issues/<bloqueador> --jq .id    # id de banco, não o número
  gh api --method POST repos/<owner>/<repo>/issues/<bloqueado>/dependencies/blocked_by -F issue_id=<id>
  ```

  O corpo do ticket acompanha. A linha `Blocked by: #<n>` no corpo só substitui a dependência onde
  a plataforma não a oferece.

Depois de acrescentar bloqueios, medir a largura da fronteira de novo antes da decisão final.

### 2. Conferir o tracker

As regras para o orquestrador moram na seção `## Quando o /implement-spec roda` do
`docs/agents/issue-tracker.md`, escrita pela operação "Alinhar o tracker do Matt" da receita da
mídia. Rodar as conferências da operação e propor o que faltar: na retomada, o tracker pode ser
de antes da `0.44.0`.

### 3. Dizer na conversa

- Se começar uma segunda revisão ampla depois da correção, interromper e pedir só checagens
  focadas nos achados corrigidos: o ciclo de revisão e correção do `implement-spec` não diz quando
  parar.
- O titular revisa a branch de integração inteira no fim.
- A verificação ponta a ponta da spec roda no checkout principal, com a branch de integração em
  checkout.
- **No Antigravity:** os subagentes rodam em background, mas a worktree por subagente não está
  documentada nem foi testada. O aviso sai quando uma passada no `agy` confirmar ou derrubar isso.

### 4. Entregar

`/clear`, e então:

```
/implement-spec <spec> — antes de começar, ler docs/agents/issue-tracker.md, seção "Quando o /implement-spec roda"
```

`<spec>` é o mesmo do `/to-tickets`: `docs/projeto/specs/<nome>.md` no modo arquivo, `#<n>` no
modo issue. O sufixo só aponta a seção; as regras ficam no tracker, que também alcança quem digita
o comando sem ele. Entregar e esperar.

Quando o `/implement-spec` terminar, o `/aicf:fechar-demanda` roda uma vez, sobre a branch de
integração.
