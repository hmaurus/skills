# Revisão da spec — A spec não tem histórias para o Matt

Data: 2026-10-12. Parecer consultivo sobre a
[spec](../../projeto/specs/a-spec-nao-tem-historias-para-o-matt.md).
Base: `63c9de0c5d5a30957e1b8712ff102de34adb7d6f`.
Identificação: `sha256sum docs/projeto/specs/a-spec-nao-tem-historias-para-o-matt.md`
→ `ae333fbc80f63a0348015e569bfaa6253db4e3c5fa1d9f4ee67e6c9fedf5a6ff`.

Resultado: dois achados P2 a resolver antes da implementação. A inclusão das
seções e a chamada de uma receita comum pelos dois pontos de entrada são
coerentes com o problema. As lacunas estão no contrato da convenção do tracker.
P2 significa correção necessária nos cenários descritos, sem urgência operacional.

## 1. P2 — Conferir as duas obrigações, não apenas a pasta da spec

**Local:** spec, linhas 67–71 e 159–162.

A operação considera a convenção presente por
`grep -c 'docs/projeto/specs' docs/agents/issue-tracker.md`. Entretanto, a solução
exige duas coisas independentes: localização da spec e referência `**Spec:**`
em cada ticket. Um tracker editado manualmente para corrigir apenas a localização
passa nessa conferência, mas não manda escrever a referência. A segunda chamada
deixa de propor a correção justamente no cenário que precisa dela.

**Consequência:** o aicf entrega `/implement <ticket>` sem a spec no argumento,
enquanto o ticket ainda pode nascer sem vínculo com ela. A retomada em sessão
limpa volta a depender de descoberta por iniciativa do agente.

**Ajuste sugerido:** a receita deve conferir separadamente a localização canônica,
a obrigação de preencher `**Spec:**` com o caminho real da demanda e a ausência
da localização antiga. Completar apenas o que falta, preservando a configuração
restante. Acrescentar à Verificação 3 a contraprova com tracker parcialmente
convertido: localização correta, obrigação de referência ausente. Esse caso deve
propor edição; só o tracker com ambas as obrigações deve passar sem alteração.

**Evidência executada:** numa cópia temporária de `issue-tracker-local.md` do Matt,
foi substituída somente a localização `.scratch/<feature-slug>/spec.md` por
`docs/projeto/specs/<nome>.md`. O `grep -c` proposto devolveu `1`, e
`'**Spec:**' in text` em Python devolveu `False`. Nenhum arquivo do projeto foi
alterado pela contraprova.

Encerra quando o aceite estático e o cenário de comportamento distinguirem
tracker parcial de tracker completamente alinhado.

## 2. P2 — Resolver expressamente as instruções que contradizem a convenção

**Local:** spec, linhas 39–46, 61–63 e 107–108.

O `to-tickets` determina, depois dos templates, `avoid specific file paths`.
A nova linha `**Spec:** docs/projeto/specs/<nome>.md` é um caminho específico no
ticket. A spec manda acrescentá-la no tracker, mas não define que ela é uma
exceção àquela proibição. O template local também começa diretamente com o
título e `What to build`, sem essa referência.

Além disso, trocar apenas `The spec is ...` deixa no tracker a abertura
`Issues and specs for this repo live as markdown files in .scratch/` e a operação
genérica de publicação que manda criar arquivo em `.scratch/<feature-slug>/`.
O objetivo declarado de eliminar instruções contraditórias não fica atendido
pela troca de uma linha.

**Consequência:** o agente recebe ordens incompatíveis sobre a referência nos
tickets e sobre o destino das specs. Pode omitir a linha ao seguir a restrição
do `to-tickets`; fora do fluxo normal, uma skill que publica spec ainda encontra
instrução explícita para usar `.scratch/`.

**Ajuste sugerido:** escrever na receita o texto da exceção: a referência à spec
canônica é obrigatória em cada ticket e é permitida mesmo quando o template da
skill exclui caminhos de implementação. Ajustar a abertura e restringir a
operação de publicação em `.scratch/` aos registros que continuam ali, preservando
as operações de wayfinding. Incluir essas alterações no limite de escrita
registrado pelo ADR. A Verificação 4 deve conferir que o valor é o caminho real
da demanda, sem os marcadores `<nome>`.

Isso não exige editar as skills do Matt. A receita local deve explicar a exceção
e eliminar a contradição na configuração que ela já está autorizada a modificar.
Encerra com texto explícito e tickets gerados que preservem a referência no uso
real previsto pela spec.

**Conferência executada no clone pinado:**

```bash
rg -n 'avoid specific file paths|local-ticket-template' /tmp/matt-historias-review/skills/engineering/to-tickets/SKILL.md
sed -n '1,22p' /tmp/matt-historias-review/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md
```

## Validação e limites

Foram lidas as skills locais `criar-spec`, `implementar-spec`, a receita da mídia,
as instruções do projeto, o ADR 0004 e a nota sobre o Matt. No Matt, foram lidos
`to-spec`, `to-tickets`, `implement` e o setup com seu tracker local.
Nenhuma skill de entrevista ou implementação foi executada: esta é uma revisão
estática, e as verificações comportamentais seguem para a implementação e o uso
real pelos responsáveis definidos na spec.

As contagens de antes das Verificações 1 e 5 foram executadas com os padrões
escritos na spec. Resultados: `0, 0, 1, 1, 0, 0`, conforme o previsto.
Na Verificação 3, o primeiro `grep` está sem arquivo ou entrada definida;
completar com `docs/agents/issue-tracker.md` para não depender de stdin.

As fontes externas foram conferidas no cache instalado `1.3.1` e no clone:

```bash
git clone --quiet --depth 1 --branch v1.3.1 https://github.com/mattpocock/skills.git /tmp/matt-historias-review
git -C /tmp/matt-historias-review rev-parse HEAD
```

O HEAD retornou `24fe0ef7737efae15c87225755e9f6f5965e4888`. O `cmp` do
`to-tickets` com o cache apontou diferença na linha 63, sobre relações nativas
entre issues. Os achados acima usam os trechos conferidos no clone, que também
estão presentes no cache: template local e restrição de caminhos.

O fechamento de `aicf:fechar-demanda` aplica-se somente ao parecer, respeitando a
restrição de escrita do Codex. A spec permanece aberta e intacta. Nenhuma
promoção de conhecimento ou mudança de implementação foi feita. O commit contém
somente este parecer; envio e conferência do CI ficam com o titular ou agente líder.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, com Claude Code
`2.1.296`, 181 links conferidos e nenhum quebrado, ambas as validações do plugin
aprovadas e versão `0.37.0` no topo do changelog. O whitespace do parecer é
conferido com `git diff --cached --check` antes do commit.
