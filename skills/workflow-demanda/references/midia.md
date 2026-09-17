# A mídia do registro — as duas receitas

Onde a demanda mora é **escolha do projeto**. A governança não muda com ela: as quatro fases, o
ritual de fechamento e a linha `Processo` são as mesmas nos dois modos. O que troca é o substrato.

Este doc é o único lugar onde comando concreto de mídia mora. As skills dizem a operação —
"gravar a demanda", "arquivar a demanda" — e mandam ler a coluna daqui.

## Ler a configuração

Uma linha no `CLAUDE.md` da raiz, na seção "Processos de desenvolvimento":

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

```bash
grep -m1 'Mídia do registro' CLAUDE.md
```

**Linha ausente significa arquivo.** Não é sinalização por ausência de propósito — é
compatibilidade com todo projeto criado antes desta opção existir. O `/aicf:setup` sempre grava a
linha, nos dois modos, para que em projeto novo a escolha seja explícita.

## Os quatro estados

| Estado | Modo arquivo | Modo issue |
| --- | --- | --- |
| Incerto — nem se sabe se será feito | `intents/backlog/<nome>.md`, ou linha em `ROADMAP.md` → Backlog | issue aberta, `aicf:backlog` |
| Decidido, ainda não entrevistado | `intents/<nome>.md`, ou linha em `ROADMAP.md` → Próximas | issue aberta, `aicf:intent` |
| Pronta para implementar | `specs/<nome>.md` | issue aberta, `aicf:spec` |
| Concluída | `specs/concluidas/<nome>.md`, com o relatório no fim | issue fechada, com o relatório em comentário |

**Uma demanda é uma issue só, do nascimento ao fechamento.** O label troca, o número não. Os três
labels são exclusivos entre si, e "concluída" não tem label — é a issue fechada.

No modo issue as duas distinções de custo desaparecem. "Próximas" é o que já foi decidido e ainda
não tem arquivo; `intents/` é o que já foi decidido e tem arquivo — a diferença entre as duas é o
custo de criar arquivo, que a issue não tem. **No modo issue não existe `ROADMAP.md`**, e não há
substituto: ele só fazia sentido onde criar arquivo custa mais que ter a ideia. O critério que ele
explicava passa a viver na descrição do label `aicf:backlog`.

## Operação por operação

| Operação | Modo arquivo | Modo issue |
| --- | --- | --- |
| Gravar demanda incerta | `docs/projeto/intents/backlog/<nome>.md`, ou linha no `ROADMAP.md` → Backlog | `gh issue create --title '<título>' --body-file <arq> --label aicf:backlog` |
| Gravar demanda decidida | `docs/projeto/intents/<nome>.md`, ou linha no `ROADMAP.md` → Próximas | o mesmo, com `--label aicf:intent` |
| Virar spec | `git mv docs/projeto/intents/<nome>.md docs/projeto/specs/` e reescrever | `gh issue edit <n> --body-file <arq> --remove-label aicf:intent --add-label aicf:spec` |
| Ler a demanda | `cat docs/projeto/specs/<nome>.md` | `gh issue view <n> --comments` |
| Listar um estado | `head -qn1 docs/projeto/specs/*.md \| sed 's/^# //'` | `gh issue list --state open --label aicf:spec` |
| Listar os três estados abertos | o mesmo `head`, com as três pastas | `gh issue list --state open --search "label:aicf:backlog,aicf:intent,aicf:spec"` |
| Gravar o relatório | no fim do arquivo da demanda | `gh issue comment <n> --body-file <arq>` |
| Concluir | `git mv` para `docs/projeto/specs/concluidas/` | `gh issue close <n>` |
| Referenciar outra demanda | link relativo — `[título](../intents/<nome>.md)` | `#<n>` |
| Corrigir referências após mover | `grep -rn '<nome-do-arquivo>' --include='*.md' .` | não se aplica — `#12` não muda de lugar |

**Corpo longo vai em `--body-file`, não em `--body`.** Título e corpo da demanda são prosa com
acento, crase e quebra de linha; passar isso inline num argumento é onde o shell estraga o texto
sem avisar. Gravar o corpo num arquivo temporário e apontar para ele.

### O gotcha do `--label` repetido

Na API do GitHub, dois `--label` filtram por issue que tem **todos** eles, não qualquer um. Como os
três labels são exclusivos entre si, `--label aicf:intent --label aicf:spec` devolve sempre vazio.
Para ver mais de um estado de uma vez a sintaxe é a de busca, com os nomes separados por vírgula
dentro de um `label:` só.

Medido no cenário exato, num repositório com **uma issue de cada label**: os três `--label` juntos
devolvem **0**, e a forma `--search` devolve **3**.

O mesmo em `denoland/deno`, que é público e reproduz a qualquer momento — `--label node:http` traz
2, `--label node:sqlite` traz 4, os dois flags juntos trazem 0, e
`--search "label:node:http,node:sqlite"` traz 6, a união exata:

```bash
gh issue list --repo denoland/deno --state open --label node:http --label node:sqlite --json number -q length
gh issue list --repo denoland/deno --state open --search "label:node:http,node:sqlite" --json number -q length
```

Os dois-pontos do nome do label não pedem aspas: `label:aicf:spec` funciona como está. O que quebra
a forma sem aspas é **espaço** no nome do label, que nenhum label `aicf:*` tem.

### O índice de label atrasa depois de um `edit`

**Confirmar troca de estado com `gh issue view`, nunca com `gh issue list`.** O filtro `--label` lê
um índice de busca eventualmente consistente, e logo depois de um `gh issue edit` ele ainda devolve
o estado **anterior** à troca — a issue some do label novo, ou aparece no antigo. Pior: a coluna de
labels que o `list` imprime vem do dado corrente, então a linha exibida combina um filtro velho com
um label novo e parece impossível.

Medido num repositório de teste, alternando o label da mesma issue e consultando em seguida: **4 de
6 rodadas** vieram defasadas. Não é raro o bastante para ignorar, e não é constante o bastante para
um `sleep` resolver.

```bash
gh issue edit <n> --remove-label aicf:intent --add-label aicf:spec
gh issue view <n> --json labels -q '[.labels[].name]|join(",")'   # autoritativo, imediato
```

O `view` é leitura direta da issue e não passa pelo índice. Vale para qualquer confirmação de
estado logo após uma escrita; para **listar** o que existe, o atraso é aceitável, porque ninguém
lista logo depois de editar.

## A linha `Processo`

No modo arquivo ela fica logo abaixo do título; no modo issue, é a **primeira linha do corpo**, no
mesmo formato. O título da issue é o título da demanda, sem o `# `.

```
Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (toca dois arquivos)
```

Referência externa continua entrando no fim da linha. **O número da própria issue não** — a demanda
*é* a issue, e repetir o número dentro dela é o segundo lugar guardando o mesmo estado.

## Criar os labels

No modo issue o `/aicf:setup` cria os três. Criação **idempotente**: label que já existe vira aviso,
não erro — daí o `|| true`.

```bash
gh label create aicf:backlog --color FBCA04 \
  --description 'Demanda incerta. Certeza, não urgência: o que é certo e sem prioridade já é aicf:intent.' || true
gh label create aicf:intent  --color 0E8A16 \
  --description 'Demanda decidida, ainda não entrevistada.' || true
gh label create aicf:spec    --color 1D76DB \
  --description 'Spec pronta para implementar.' || true
```

A descrição de `aicf:backlog` carrega o critério **certeza, não urgência**, que no modo arquivo
vivia no `ROADMAP.md` e no modo issue não teria outro lugar. Descrição de label no GitHub tem
**limite de 100 caracteres** — o que não couber fica de fora, e o critério inteiro está aqui.

**Criar o label é passo do setup, não da demanda.** `gh issue create --label` com label inexistente
falha em vez de criar; é a armadilha que esta seção existe para evitar.

## Adotar uma issue que já existe

`/aicf:criar-spec #12` e `/aicf:fechar-demanda #12` aceitam um número como alvo. Em vez de criar
issue nova, a skill **reescreve o corpo daquela** e ajusta o label. Issue que nunca teve label
`aicf:*` ganha um agora — é assim que uma issue de fora da governança entra nela.

```bash
gh issue edit 12 --body-file <arq> --add-label aicf:spec
```

Dois casos concretos, e os dois quebram sem adoção:

- **O `to-spec` do Matt cria issue nova, não edita uma existente.** Quem entrevista por ele com os
  dois apontando para o GitHub terminaria com duas issues para a mesma demanda. Com adoção:
  `to-spec` publica, `/aicf:criar-spec #<n>` adota — uma issue só.
- **Contribuição de fora.** Alguém abre uma issue crua propondo algo, e `/aicf:criar-spec #<n>` a
  transforma em spec no lugar onde nasceu, com o histórico da conversa junto. Sem adoção o aicf
  abriria uma issue paralela e a do contribuidor viraria duplicata.

No modo arquivo não há o que adotar: o equivalente já existe e é o `git mv` de `intents/` para
`specs/`.

## Quando o `gh` falha

Mídia issue configurada e `gh` indisponível — sem rede, token expirado, sem permissão — a skill
**mostra o erro e para**. Não grava em arquivo, não grava em rascunho: o usuário resolve o acesso e
retoma.

Gravar em `docs/projeto/` "só desta vez" é exatamente como um repositório acaba com governança em
duas mídias sem ninguém ter escolhido isso.

## Divergência com o tracker do Matt Pocock

O `/setup-matt-pocock-skills` grava em `docs/agents/issue-tracker.md` a resposta para **onde o
trabalho mora** — a mesma pergunta que a linha de mídia responde. Num repositório com as duas
coleções, as duas respostas existem e podem discordar.

O aicf **não delega e não depende**: a linha do `CLAUDE.md` é a única fonte da verdade dele, e o
modo issue funciona em repositório que nunca ouviu falar do Matt. Mas quando aquele arquivo existe:

- **No `/aicf:setup`**, lê-lo e propor o default a partir dele — "o tracker do Matt aponta para
  GitHub; usar issues aqui também?" — em vez de perguntar do zero o que já foi respondido ao lado.
- **Nas demais skills**, se as duas discordarem, **avisar uma vez** e seguir a linha do `CLAUDE.md`.
  Divergência é legítima — dá para querer o tracker dele em GitHub e o registro do aicf em arquivo
  —, mas precisa ser escolha, não descoberta tardia.

É o padrão que o método já usa duas vezes: o passo 3 do fechamento delega ADR e glossário ao
`/domain-modeling` e funciona sem ele; o `implementar-spec` oferece os caminhos das coleções
instaladas e só o aicf quando não há nenhuma.

**Os vocabulários de estado não se unificam.** Os três labels `aicf:*` classificam maturidade do
documento; os cinco do `/triage` classificam o que fazer em seguida. Eixos diferentes, e a mesma
issue pode carregar os dois — o prefixo existe para que não colidam. Nenhum dos dois lados enxerga
os labels do outro, e isso fica assim.

## O que não muda com a mídia

PRD, ADR, `CONTEXT.md` e `docs/referencias/` ficam em **arquivo nos dois modos**. Nenhum deles é
demanda: o PRD é documento vivo, revisado toda vez que uma decisão o contraria, e ADR é imutável por
definição. No modo issue, `docs/projeto/` continua existindo com o `PRD.md` dentro, e só ele.

Também não muda o **passo 3 do fechamento**: o que vale além da demanda — ADR, regra no `CLAUDE.md`,
doc em `docs/referencias/` — é promovido para o repositório nas duas mídias. É o que compensa o
preço assumido do modo issue, que o relatório em comentário de issue fechada some do `git clone`.

**Não existe modo misto.** A demanda inteira mora numa mídia só, relatório incluído.
