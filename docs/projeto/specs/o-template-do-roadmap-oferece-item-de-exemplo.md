# O template do roadmap entrega item de exemplo sob um cabeçalho que diz "decidido"

Processo — entrevista: criar-spec · implementação: a definir · sugestão: aicf-direto (texto em quatro arquivos, sem decisão de abordagem em aberto)

## Problema

O `skills/setup/templates/roadmap.md` traz duas linhas prontas sob `## Próximas`, cabeçalho cuja
própria legenda diz **"Decidido, ainda sem arquivo"**:

```
- [ ] Repositório no GitHub e CI mínimo
- [ ] `PRD.md` preenchido
```

Quem recebe a cópia não tem como distinguir exemplo de decisão: o formato é idêntico ao de um item
real, e o cabeçalho afirma que o que está ali foi decidido
(`sed -n '/^## Próximas/,/^## /p' skills/setup/templates/roadmap.md | grep -c '^- \[ \]'` → `2`).

**Aconteceu neste repositório.** O `docs/projeto/ROADMAP.md` e o template nasceram no mesmo commit
(`git log --oneline --diff-filter=A -1 -- docs/projeto/ROADMAP.md skills/setup/templates/roadmap.md`
→ `a6276e7`), com os mesmos dois itens. A linha de CI — na época
`Repositório, branch de trabalho e CI mínimo` — sobreviveu quatro versões como item decidido sem
nunca ter sido decidida, e só caiu quando a entrevista de
[nenhum teste acusa link morto](../concluidas/nenhum-teste-acusa-link-morto.md) foi atrás da origem
dela. A outra linha coincidia com uma pendência real daqui, o que escondeu o defeito: metade do
exemplo virou verdade por acaso.

A demanda [os templates contradizem o projeto que nasce](../concluidas/os-templates-contradizem-o-projeto-que-nasce.md)
(`e21a18b`) mexeu nessa linha e decidiu **mantê-la** reescrita, porque o remoto é o que o setup não
cria no modo arquivo. Esta spec reverte aquela decisão: o argumento prova que o item é *plausível*,
não que o projeto o *decidiu* — projeto em modo arquivo pode nunca querer GitHub.

Os dois itens também repetem o que o próprio método já faz:

- `PRD.md` preenchido é o passo 4 do fechamento do `setup` (`skills/setup/SKILL.md`, "Sugerir
  `/aicf:criar-prd`").
- A primeira leva real de `Próximas` é escrita pelo `criar-prd`, no passo 2 do "Ao terminar"
  (`skills/criar-prd/SKILL.md`: "isso é o primeiro `ROADMAP.md`"). A seção vazia tem dono, e ele é
  justamente o próximo passo que o setup sugere.

## Solução

1. **`## Próximas` do template fica só com a legenda.** As duas linhas saem, sem marcador de
   exemplo no lugar: a seção fica igual à do `docs/projeto/ROADMAP.md` deste repositório hoje.
2. **A regra de templates generaliza.** O princípio do `.claude/rules/templates.md` deixa de ser
   "template não traz valor de configuração escrito por extenso" e passa a ser **"template não
   afirma o que o projeto não decidiu"**, com os dois casos já pagos como formas dele:
   - valor de configuração vai no marcador `\<...\>` — o caso da `0.17.0` (linha
     `**Mídia do registro:**`), que já está no arquivo e fica, encurtado se couber;
   - conteúdo de exemplo vai marcado como exemplo (`> - ...`, como no Backlog) ou não vai — o caso
     deste item, em duas ou três frases.

   A conferência do fim do arquivo cresce na mesma medida: ler o template procurando linha de
   configuração com valor decidido **e item em seção que o cabeçalho declara decidida**.
3. **A verificação do setup acompanha.** A linha
   `grep -n 'Repositório' docs/projeto/ROADMAP.md  # "Repositório no GitHub e CI mínimo"` do
   `docs/referencias/verificacao-do-setup.md` troca pelo comando que confere a seção vazia no
   projeto gerado:
   `sed -n '/^## Próximas/,/^## /p' docs/projeto/ROADMAP.md | grep -c '^- \[ \]'  # 0`.
4. **Versão `0.29.2`**, com entrada no `CHANGELOG.md` — é mudança no que o plugin copia para o
   projeto do usuário.

## Arquivos e interfaces

| Arquivo | Mudança |
| --- | --- |
| `skills/setup/templates/roadmap.md` | as duas linhas de `## Próximas` saem |
| `.claude/rules/templates.md` | princípio generalizado, com os dois casos |
| `docs/referencias/verificacao-do-setup.md` | o `grep 'Repositório'` vira a contagem da seção vazia |
| `.claude-plugin/plugin.json`, `CHANGELOG.md` | `0.29.2` |
| `docs/projeto/concluidas/nenhum-teste-acusa-link-morto.md` | **já feito ao gravar esta spec:** o link para esta demanda passou de `intents/` para `specs/` |

## Fora de escopo

- **Marcar o exemplo em vez de tirar** (`> - [ ] ...`). Ensinaria o formato, mas o formato já está
  no `workflow-demanda`, e quem escreve a primeira linha é o `criar-prd`, que o conhece.
- **Legenda que aponta o `criar-prd`.** O vazio se explica pelo fluxo do setup, que já sugere o
  `criar-prd` como próximo passo; a frase a mais seria mais uma coisa a envelhecer no template.
- **Os outros quatro templates.** Lidos na entrevista, nenhum tem o defeito: `prd.md` e
  `claude-md.md` usam `>` ou `> A preencher.` para a legenda, `readme.md` e `claude-md.md` usam o
  marcador `\<...\>`, e `preferencias.md` é conteúdo adotado de propósito, não exemplo.
- **Mudar o `SKILL.md` do setup ou do `criar-prd`.** O fluxo já está certo; o defeito é só o que o
  template afirma.

## Verificação

1. `sed -n '/^## Próximas/,/^## /p' skills/setup/templates/roadmap.md | grep -c '^- \[ \]'` → `0`
   (hoje `2`).
2. `grep -c 'Repositório no GitHub' skills/setup/templates/roadmap.md docs/referencias/verificacao-do-setup.md`
   → `0` nos dois (hoje `1` nos dois).
3. `grep -c 'não decidiu' .claude/rules/templates.md` → `1` ou mais (hoje `0`).
4. `./scripts/check.sh` → `Tudo verde.`, com a `0.29.2` no topo do `CHANGELOG.md`.

**O comportamento do setup não se verifica nesta sessão:** a skill tem
`disable-model-invocation: true`. Como ele copia o template sem reescrever, o passo 1 cobre o
conteúdo; a passada do setup que confirma o projeto gerado fica com o titular, pelo comando novo
do `docs/referencias/verificacao-do-setup.md` (modo arquivo), que é onde essa condição de aceite
mora.

## Origem

Achado da entrevista de *nenhum teste acusa link morto*, em 2026-09-19, ao procurar de onde vinha
a linha de CI do roadmap. A spec dela deixou a correção do template **fora do escopo**, e o
fechamento abriu esta intent. Entrevistada em 2026-09-24.
