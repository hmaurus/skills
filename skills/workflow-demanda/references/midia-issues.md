# Mídia do registro: issues (GitHub)

A receita do modo issue, operação por operação. O que é comum às mídias — a linha de
configuração, os quatro estados, "um item, um lugar", o que não muda com a mídia — está no
`/aicf:workflow-demanda`.

## Operação por operação

| Operação | Comando |
| --- | --- |
| Gravar demanda incerta | `gh issue create --title '<título>' --body-file <arq> --label aicf:backlog` |
| Gravar demanda decidida | o mesmo, com `--label aicf:intent` |
| Gravar demanda que já nasce pronta | o mesmo, com `--label aicf:spec` |
| Virar spec | `gh issue edit <n> --body-file <arq> --remove-label aicf:intent --add-label aicf:spec` |
| Ler a demanda | `gh issue view <n> --comments` |
| Listar um estado | `gh issue list --state open --label aicf:spec` |
| Listar os três estados abertos | `gh issue list --state open --search "label:aicf:backlog,aicf:intent,aicf:spec"` |
| Gravar o relatório | `gh issue comment <n> --body-file <arq>` |
| Concluir | `gh issue edit <n> --remove-label <label-atual>` e `gh issue close <n>` |
| Referenciar outra demanda | `#<n>` |
| Corrigir referências após mover | não se aplica — `#12` não muda de lugar |

Os três labels são exclusivos entre si: mudar de estado é sempre **remover o atual e pôr o novo**,
nunca só acrescentar. "Concluída" não tem label — é a issue fechada, e o label sai junto com o
fechamento; uma issue fechada nunca carrega `aicf:*`.

**Corpo longo vai em `--body-file`, não em `--body`.** Título e corpo da demanda são prosa com
acento, crase e quebra de linha; passar isso inline num argumento é onde o shell estraga o texto
sem avisar. Gravar o corpo num arquivo temporário e apontar para ele.

### O `--label` repetido filtra por todos

Dois `--label` devolvem as issues que têm **todos** eles, não qualquer um. Como os três labels são
exclusivos, `--label aicf:intent --label aicf:spec` devolve sempre vazio. Para ver mais de um estado
de uma vez, a sintaxe é a de busca, com os nomes separados por vírgula dentro de um `label:` só —
a forma da tabela. Os dois-pontos do nome não pedem aspas; o que quebraria a forma sem aspas é
espaço no nome, que nenhum label `aicf:*` tem.

### O índice de label atrasa depois de um `edit`

**Confirmar troca de estado com `gh issue view`, nunca com `gh issue list`.** O filtro `--label` lê
um índice de busca eventualmente consistente, e logo depois de um `gh issue edit` ele ainda devolve
o estado anterior à troca — a issue some do label novo, ou aparece no antigo, enquanto a coluna de
labels exibida já mostra o atual. Não é raro o bastante para ignorar, nem constante o bastante para
um `sleep` resolver.

```bash
gh issue edit <n> --remove-label aicf:intent --add-label aicf:spec
gh issue view <n> --json labels -q '[.labels[].name]|join(",")'   # autoritativo, imediato
```

**Listar também morde**, e o caso é real: o `criar-spec` promove a issue a `aicf:spec` e o
`implementar-spec` lista as specs abertas em seguida, na mesma sessão — a issue recém-promovida pode
não aparecer. Quando a listagem vem logo depois de uma troca de estado feita nesta sessão, conferir
os números que a sessão tocou com `gh issue view` antes de concluir que sumiram, ou dizer ao
usuário que o índice pode estar atrasado em vez de afirmar que a lista está completa.

## A linha `Processo`

É a **primeira linha do corpo** da issue, no formato do `/aicf:fechar-demanda`. O título da issue é
o título da demanda, sem o `# `. Referência externa continua entrando no fim da linha; **o número da
própria issue não** — a demanda *é* a issue, e repetir o número dentro dela é o segundo lugar
guardando o mesmo estado.

## Criar os labels

**Criar o label é passo do `/aicf:setup`, não da demanda:** `gh issue create --label` com label
inexistente falha em vez de criar. Criação **idempotente** — label que já existe vira aviso, não
erro; daí o `|| true`.

```bash
gh label create aicf:backlog --color FBCA04 \
  --description 'Demanda incerta. Certeza, não urgência: o que é certo e sem prioridade já é aicf:intent.' || true
gh label create aicf:intent  --color 0E8A16 \
  --description 'Demanda decidida, ainda não entrevistada.' || true
gh label create aicf:spec    --color 1D76DB \
  --description 'Spec pronta para implementar.' || true
```

A descrição de `aicf:backlog` carrega o critério **certeza, não urgência**, que no modo arquivo
vive no `ROADMAP.md` e aqui não teria outro lugar. Descrição de label tem **limite de 100
caracteres**; o que não couber fica de fora, e o critério inteiro está no `/aicf:workflow-demanda`.

## Adotar uma issue que já existe

`/aicf:criar-spec #12` e `/aicf:fechar-demanda #12` aceitam um número como alvo. Em vez de criar
issue nova, a skill **reescreve o corpo daquela** e ajusta o label. Issue que nunca teve label
`aicf:*` ganha um agora — é assim que uma issue de fora da governança entra nela.

**Olhar o label atual antes de escrever.** O alvo `#<n>` não é só para issue crua: é também como o
usuário aponta a skill para uma demanda que já está na governança, e aí só acrescentar label deixa
a issue com dois, contando a mesma demanda em dois estados.

```bash
gh issue view 12 --json labels -q '[.labels[].name]|join(",")'   # o que já tem
gh issue edit 12 --body-file <arq> --remove-label aicf:intent --add-label aicf:spec   # tinha label aicf:*
gh issue edit 12 --body-file <arq> --add-label aicf:spec                              # não tinha nenhum
```

Dois casos concretos, e os dois quebram sem adoção:

- **O `to-spec` do Matt cria issue nova, não edita uma existente.** Quem entrevista por ele com os
  dois apontando para o GitHub terminaria com duas issues para a mesma demanda. Com adoção:
  `to-spec` publica, `/aicf:criar-spec #<n>` adota — uma issue só.
- **Contribuição de fora.** Alguém abre uma issue crua propondo algo, e `/aicf:criar-spec #<n>` a
  transforma em spec no lugar onde nasceu, com o histórico da conversa junto. Sem adoção o aicf
  abriria uma issue paralela e a do contribuidor viraria duplicata.

## Quando o `gh` falha

Sem rede, token expirado, sem permissão: a skill **mostra o erro e para**. Não grava em arquivo, não
grava em rascunho; o usuário resolve o acesso e retoma. Gravar em `docs/projeto/` "só desta vez" é
exatamente como um repositório acaba com governança em duas mídias sem ninguém ter escolhido isso.
