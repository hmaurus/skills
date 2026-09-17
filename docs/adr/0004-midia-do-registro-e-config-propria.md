# 0004 — A mídia do registro é configuração própria, lida em runtime

Data: 2026-09-17 · Status: aceita · Versão: `0.17.0`

## Decisão

**Onde a demanda mora é escolha do projeto — arquivos em `docs/projeto/` ou issues do GitHub —, e a
escolha é uma linha do `CLAUDE.md` do próprio projeto:**

```
**Mídia do registro:** arquivos em `docs/projeto/`
**Mídia do registro:** issues (GitHub)
```

**Linha ausente significa arquivo.** As skills ficam neutras de mídia e leem essa linha em runtime;
os comandos concretos vivem num lugar só, `skills/workflow-demanda/references/midia.md`.

O aicf **lê** `docs/agents/issue-tracker.md` do conjunto do Matt Pocock quando ele existe — para
propor o default no setup e para avisar de divergência —, mas **não delega e não depende** dele.

Três coisas passam a ser interface pública, das quais outro projeto pode depender: a linha do
`CLAUDE.md` com seus dois valores; os labels `aicf:backlog`, `aicf:intent` e `aicf:spec`; e a linha
`Processo` como primeira linha do corpo da issue.

## Por quê

O método já oferecia três caminhos de entrevista e quatro de implementação, e declarava que "a
implementação é roteiro, não trilho". A mídia do registro era o último trilho único: quem preferia
issue tracker customizava por fora, sem suporte e sem documentação.

A alternativa séria era **não ter config própria** e usar o `docs/agents/issue-tracker.md` do Matt
como fonte, já que ele responde a mesma pergunta. Descartada: feature central do aicf não pode
depender do formato de um plugin de terceiro, que pode mudar sem aviso e quebrar em silêncio um
repositório que já funcionava, e quem quer só o aicf não deve precisar instalar outra coleção.

O `CLAUDE.md` foi escolhido em vez de um arquivo de config novo porque **não é mecanismo novo**: ele
já carrega inteiro em toda sessão, já é onde o método guarda configuração de projeto — a linha
"Coleções de skills de workflow instaladas" que o `implementar-spec` lê —, e o usuário troca a mídia
editando uma linha.

O default é arquivo por duas razões, e a segunda é a mais forte: é o modo que um usuário novo
entende sem explicação, e é o único que funciona com zero setup — repositório local, sem remote, sem
`gh`, sem login, sem fornecedor.

## Consequências

- **Não existe modo misto.** A demanda inteira mora numa mídia só, relatório incluído. O preço está
  assumido: relatório em comentário de issue fechada some do `git clone` e é menos achável anos
  depois. O que compensa é o passo 3 do fechamento, que promove para o repositório o que vale além
  da demanda — e que não muda com a mídia.
- **Não há migração.** Trocar a mídia vale do ponto em diante; o que já está em arquivo fica onde
  está, e demanda nova nasce na mídia nova. Código de migração para um evento que acontece no máximo
  uma vez por projeto não se paga.
- **Só GitHub via `gh`.** Linear, Jira, GitLab e markdown local ficam de fora até alguém pedir —
  abstração antecipando o futuro é gatilho de revisão do lema. Uma terceira mídia entra como coluna
  nova no `midia.md`, não como condicional espalhada pelas skills.
- **No modo issue não existe `ROADMAP.md`**, e não há substituto: ele só fazia sentido onde criar
  arquivo custa mais que ter a ideia. O critério "certeza, não urgência" passa a viver na descrição
  do label `aicf:backlog` — que tem limite de 100 caracteres.
- **Nenhuma das duas mídias detecta estado errado.** Pasta errada e label errado seguem
  indistinguíveis de pasta certa e label certo. O [0003](0003-um-item-um-lugar.md) já tinha tirado a
  detecção por duplicação; esta demanda não a reintroduz por outro nome.
- **Mídia issue com `gh` indisponível é parada, não fallback.** Gravar em arquivo "só desta vez" é
  como um repositório acaba com governança em duas mídias sem ninguém ter escolhido isso.
- Reverter significaria voltar a mídia para dentro de cinco skills, dois templates e os dois
  READMEs, e quebrar quem já depende dos três labels e da linha de config.
