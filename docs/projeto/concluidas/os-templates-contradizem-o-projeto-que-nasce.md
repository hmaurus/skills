# Os templates contradizem o projeto que o setup acabou de criar

Processo — entrevista: nenhuma · implementação: aicf-direto

## Problema

Achado na passada do `/aicf:setup` da `0.23.0` que encerrou a Verificação 1 de
[o setup entrega projeto sem repositório](../concluidas/o-setup-entrega-projeto-sem-repositorio.md),
num diretório novo, modo arquivo. O roteiro rodou certo do começo ao fim; o que saiu errado foram
os **templates** que ele copia.

**1. A linha das coleções duplica os nomes.** O template traz:

```
**Coleções de skills de workflow instaladas:** nenhuma. _(Superpowers, Matt Pocock — são os caminhos que o `implementar-spec` pode oferecer além do aicf.)_
```

O parêntese usa como exemplo exatamente os valores que vão substituir o `nenhuma` ao lado. Detectadas
as duas coleções, o arquivo nasce com `Superpowers, Matt Pocock. _(Superpowers, Matt Pocock — …)_`, e
o agente gastou um comando a mais só para consertar o que ele próprio tinha acabado de escrever.

**2. O template manda `develop` num repositório que nasceu com `main`.** A seção `## Git` diz
"`develop` — branch de trabalho. `main` — produção". O `git init` cria uma branch só, o primeiro
commit do setup foi para ela, e o `CLAUDE.md` gerado descreve errado o repositório em que está. **Isto
é novo:** até a `0.22.0` o setup não criava repositório, e não havia o que contradizer.

**3. O roadmap nasce com um item já feito.** `- [ ] Repositório, branch de trabalho e CI mínimo`, em
`Próximas`, num projeto cujo repositório o setup acabou de criar. Mesma causa do item 2.

## Solução

Três correções nos templates, uma por item.

**1.** O parêntese deixa de citar os nomes, e o valor vira placeholder na forma que o template já usa
para o nome do projeto e para a mídia:

```
**Coleções de skills de workflow instaladas:** \<nenhuma | os nomes que o setup detectou\>. _(São os caminhos de entrevista e implementação que o `implementar-spec` pode oferecer além do aicf.)_
```

**2.** A seção `## Git` passa a descrever **uma branch só**, que é o que o `git init` entrega, com a
linha que diz o que fazer para ter outra coisa. Descrever um fluxo de duas branches num repositório
de uma é pior que descrever um fluxo simples que o usuário amplia.

**3.** O item do roadmap vira `- [ ] Repositório no GitHub e CI mínimo` — o repositório local já
existe, e o remoto é justamente o que o setup **não** cria no modo arquivo.

## Arquivos e interfaces

- `skills/setup/templates/claude-md.md` — itens 1 e 2.
- `skills/setup/templates/roadmap.md` — item 3.
- `.claude-plugin/plugin.json` e `CHANGELOG.md` — em par, pela regra de publicação.

O `SKILL.md` do setup **não** muda: o roteiro está certo, e foi ele que expôs os três.

## Fora de escopo

- **Perguntar a convenção de branch no setup.** Seria uma pergunta a mais num roteiro que acabou de
  perder a promessa de número, para um valor que o usuário edita em dez segundos no arquivo gerado.
- **Os outros placeholders do template.** Só os três itens acima apareceram; varrer o resto sem um
  sintoma é procurar problema.

## Verificação

1. Os três sumiram do que o setup copia:

   ```bash
   grep -c 'Superpowers, Matt Pocock' skills/setup/templates/claude-md.md  # 1 hoje, 0 depois
   grep -c 'develop' skills/setup/templates/claude-md.md                   # 1 hoje, 0 depois
   grep -c 'Repositório, branch de trabalho' skills/setup/templates/roadmap.md  # 1 hoje, 0 depois
   ```

   O primeiro grep mira **a linha**, não a palavra: `Superpowers` aparece duas vezes no template, e
   a outra é legítima — a regra que manda usar `systematic-debugging` em bug de causa desconhecida.
   Um `grep -c 'Superpowers'` devolveria `2` e `1`, e a condição de aceite apontaria para o lugar
   errado. Escrito depois de esta Verificação nascer com esse erro e o comando o pegar.

2. A substituição que o setup faz não duplica mais. Rodar a troca do item 1 sobre o template e
   conferir que `Superpowers` aparece **uma vez só** na linha resultante.

3. `./scripts/check.sh` termina em `Tudo verde.` e sai com 0.

4. A confirmação ponta a ponta é a **Verificação 2** da demanda anterior — a passada do ramo issue,
   que ainda não rodou —, onde o `CLAUDE.md` gerado tem que nascer sem duplicação e sem `develop`.
   Do titular, pelo `disable-model-invocation: true`.


## Relatório de implementação (2026-09-20)

**Status** — concluído. As três condições da Verificação 1 rodaram e passaram, e a Verificação 2
também. A confirmação ponta a ponta — o `CLAUDE.md` de um projeto novo nascendo sem duplicação e sem
`develop` — é a Verificação 4, que viaja junto da passada do ramo issue da demanda anterior e é do
titular, pelo `disable-model-invocation: true`.

**Causa raiz** — duas causas, não uma. A duplicação da linha das coleções é antiga e independente:
o parêntese foi escrito como exemplo (`Superpowers, Matt Pocock`) para um campo cujo valor real é
exatamente esse, e ninguém tinha rodado o setup com as duas coleções instaladas até agora. As outras
duas nasceram **com a `0.23.0`**: descrever `develop`/`main` e listar "Repositório" como pendência
eram afirmações inofensivas enquanto o setup não criava repositório nenhum, e viraram contradição no
dia em que ele passou a criar. Mudança que faz o entorno ficar errado sem tocar nele.

**Arquivos alterados**

| Arquivo | O quê |
| --- | --- |
| `skills/setup/templates/claude-md.md` | o valor das coleções vira placeholder e o parêntese deixa de citar nomes; `## Git` passa a descrever `main` como única branch |
| `skills/setup/templates/roadmap.md` | `Repositório, branch de trabalho e CI mínimo` → `Repositório no GitHub e CI mínimo` |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.23.1`, em par |
| `CLAUDE.md` | a regra do comando que um doc escreve ganha a emenda do passo 3 |

O `skills/setup/SKILL.md` **não** mudou: o roteiro rodou certo do começo ao fim, e foi ele que
expôs os três.

**Commits**

| Sha | O quê |
| --- | --- |
| `0701811` | a demanda nasce pronta para implementar, sem entrevista |
| `e21a18b` | as três correções, mais versão e CHANGELOG |

**Validação**

- `./scripts/check.sh` — `Tudo verde.`, com `107 links conferidos, 0 quebrados`.
- Verificação 1 — os três greps devolvem `0`, e devolviam `1` em `eef23df`
  (`git show eef23df:skills/setup/templates/claude-md.md | grep -c 'Superpowers, Matt Pocock'`).
- Verificação 2 — a substituição do placeholder pelos dois nomes produz a linha com `Superpowers`
  aparecendo **uma vez**.
- **Sem revisão de código externa**, e a razão: a mudança é ajuste de texto em três linhas, que é o
  limiar que o próprio ritual usa para dispensá-la, e a Verificação 2 já executa a substituição em
  vez de julgá-la à vista.

**Escopo efetivo** — igual à spec. Nada além dos dois templates e do par versão/CHANGELOG.

**Lições**

- **O comando de uma condição de aceite mira o trecho que muda, não o assunto.** A Verificação 1
  nasceu prevendo `grep -c 'Superpowers'` em `1`, e eram `2`: a segunda ocorrência é a regra que
  manda usar `systematic-debugging` em bug de causa desconhecida, e ela fica. Um grep pela palavra
  teria apontado para `2 → 1` e a condição de aceite descreveria o lugar errado. Quem pegou foi o
  próprio comando, rodado antes de a spec fechar. Promovido ao `CLAUDE.md` — é a terceira ocorrência
  da mesma família, e a primeira em que o comando foi executado e ainda assim estava mal mirado.
- **A passada real é o único teste que existe para uma skill.** As três correções estavam no
  repositório desde antes da `0.23.0` — duas delas viraram defeito por causa dela — e nem o
  `check.sh`, nem a revisão por subagente da demanda anterior, nem quatro leituras do template as
  pegaram. O que pegou foi rodar o comando num diretório vazio e ler o arquivo que saiu.

**Saída do passo 3** — a emenda no `CLAUDE.md`, e nada mais: nenhum ADR (as três decisões são
reversíveis editando uma linha), nenhuma demanda nova, nenhuma tornada obsoleta.
