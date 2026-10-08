# Revisão da implementação — O agente não oferece o caminho do Matt

Data: 2026-10-07. Comparação: `git diff ef005fe...a7d14ad`.
Base: `ef005feac9fc70b4bf3dd05bd1c0b1835cfbff97`.
Alvo: `a7d14ad3a279006fb48cef942ea0aab3815e13b4`.
Spec: [demanda concluída](../../projeto/concluidas/o-agente-nao-oferece-o-caminho-do-matt.md).

Commits conferidos com `git log ef005fe..a7d14ad --oneline`:

- `debde95` — feat: o agente oferece o caminho do Matt.
- `c5de9d3` — fix: o setup e a ajuda avisam que divergir tira o Matt.
- `a7d14ad` — docs(projeto): conclui o agente não oferece o caminho do Matt.

A skill `mattpocock-skills:code-review` orientou dois subagentes independentes,
um para Standards e outro para Spec. A base foi identificada pelo commit da
revisão anterior. O parecer é consultivo; o Codex não alterou a implementação.

## Standards

**Um achado documental P3 — vincular a conferência nos READMEs.**

[README.md](../../../README.md), linha 150, e
[README.en.md](../../../README.en.md), linha 152, acrescentam que o
`grill-with-docs` grava termos no glossário e decisões em ADR, sem comando de
conferência nesse texto. A regra em
[.claude/CLAUDE.md](../../../.claude/CLAUDE.md), linha 27, exige:
“Afirmação sobre ferramenta de terceiro carrega o comando que a confere, no
texto que a propõe”.

A spec e o CHANGELOG têm evidência, mas os READMEs não a apresentam nem a
vinculam. O leitor desses arquivos não recebe a conferência junto da afirmação,
como a regra local exige. Acrescentar a conferência reproduzível que prova o
encadeamento `grill-with-docs` → `domain-modeling` e os dois registros, ou uma
referência explícita ao trecho que traz essa conferência. Encerra quando as duas
versões do README oferecerem esse vínculo.

A evidência foi relida no cache do Matt `1.3.1` indicado pela spec:

```bash
rg -n 'Call the Skill|Create files lazily|Offer ADRs|Update GLOSSARY' \
  ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/grill-with-docs/SKILL.md \
  ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/domain-modeling/SKILL.md
```

O resultado mostra o wrapper carregando `grilling` e `domain-modeling`, a
criação dos registros e as seções de atualização do glossário e oferta de ADRs.
O achado é de rastreabilidade documental, não de falha no fluxo implementado.
Não foi encontrada outra violação documental ou heurística relevante.

## Spec

**Nenhum achado.** A comparação implementa os requisitos da spec: oferta e
critérios do Matt, entrevista por `grilling` e `domain-modeling`, passagem pelo
`criar-spec`, leitura dos ADRs, item Testes e aplicação por `/tdd`, comandos com
spec e ticket, alinhamento obrigatório do tracker e fechamento da demanda após
o último ticket.

Os atalhos de entrada permanecem conforme a decisão explícita da terceira
revisão; não foram tratados como lacunas. Os ajustes adicionais no setup, na
linha do `brainstorming` dos READMEs e nas notas de sessão são coerentes com o
fluxo solicitado e estão explicados no relatório de implementação.

Revisão estática: nenhuma skill dos fluxos foi invocada, nem foi comprovada
oferta, passagem de fase ou retomada em sessão nova. As verificações 3 e 4
continuam corretamente registradas como dependentes do uso real pelo titular.

## Validação e fechamento do parecer

Os quatorze `grep -c` da Verificação 1 foram executados com os padrões e arquivos
escritos na spec. Resultado na ordem:
`1, 0, 0, 1, 1, 3, 1, 1, 1, 0, 0, 3, 0, 3`.
Todos atendem aos valores de depois; são verificações de texto, não de
comportamento do agente.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, Claude Code `2.1.293`,
171 links conferidos e nenhum quebrado, os dois `Validation passed` e versão
`0.37.0` no topo do changelog, antes da criação deste parecer.

O CI do alvo foi conferido com
`gh run list --workflow=ci.yml --limit 3 --json headSha,status,conclusion,url`:
`a7d14ad` está `completed success`, no
[run 37712971582](https://github.com/hmaurus/skills/actions/runs/37712971582).
Esse run valida a implementação revisada; não valida o commit posterior deste
parecer.

**Publicação pendente:** `gh release view v0.37.0 --json tagName,targetCommitish,body,url`
retornou `release not found` nesta revisão. A entrega do trecho de migração nas
notas da release ainda depende da publicação pelo titular ou agente líder.
Isso é uma pendência de publicação, separada dos achados dos dois eixos.

O fechamento de `aicf:fechar-demanda` aplica-se somente ao parecer, respeitando
a restrição do Codex. Não houve alteração da demanda concluída nem promoção de
conhecimento fora deste diretório. O parecer vai em commit próprio, com
`./scripts/check.sh` e `git diff --cached --check` antes do commit. Seu envio e
a conferência do CI ficam com o titular ou agente líder; nenhum push faz parte
desta revisão.

Resultado por eixo: Standards — um P3 documental sobre o vínculo da evidência
nos READMEs; Spec — nenhum achado.
