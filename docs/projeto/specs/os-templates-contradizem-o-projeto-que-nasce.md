# Os templates contradizem o projeto que o setup acabou de criar

Processo — entrevista: nenhuma · implementação: a definir · sugestão: aicf-direto (três correções de uma linha cada, sem decisão de abordagem)

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
