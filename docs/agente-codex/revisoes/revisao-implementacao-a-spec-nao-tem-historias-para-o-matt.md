# Revisão da implementação — A spec não tem histórias para o Matt

Data: 2026-10-12. Base: `ff2b5947bfcb2bcd95254b44151601a3abf6be91`.
Alvo: [spec e relatório](../../projeto/concluidas/a-spec-nao-tem-historias-para-o-matt.md).

Resultado: nenhum bloqueio encontrado na revisão estática; uma sugestão P3 para
fortalecer o aceite do uso real. Os dois achados do
[parecer anterior](revisao-spec-a-spec-nao-tem-historias-para-o-matt.md) foram
atendidos no texto implementado: conferências separadas e remoção das instruções
contraditórias, com exceção expressa para o caminho da spec.

## P3 — O comando do uso real confere o formato, mas não a demanda correta

**Local:** Verificação 4, linhas 185–190 da spec.

O `grep -L` aceita qualquer nome sob `docs/projeto/specs/`. Um ticket com
`**Spec:** docs/projeto/specs/demanda-inexistente.md` passa sem ser listado,
mesmo quando esse arquivo não existe. Também passa se apontar para a spec de
outra demanda. Assim, o comando sozinho não prova a afirmação de que o caminho
é o real da demanda. A conferência do transcript continua necessária e reduz
o risco, mas deve confirmar qual spec foi lida, além de quando foi lida.

**Sugestão:** no uso real, comparar a linha inteira de cada ticket com
`**Spec:** <caminho exato da demanda>` e conferir que o arquivo existe. Confirmar
no transcript a leitura desse mesmo arquivo antes do primeiro teste. Encerra
quando o aceite rejeita tanto caminho inexistente quanto outra spec existente.

**Contraprova executada:** em diretório temporário, foi criado um ticket com a
linha acima; o padrão literal da Verificação 4 não o listou, e a existência do
alvo retornou falso. Nenhum arquivo de implementação foi alterado.

```python
from pathlib import Path
import subprocess
import tempfile

with tempfile.TemporaryDirectory() as directory:
    ticket = Path(directory) / '01-ticket.md'
    ticket.write_text('# 01: Ticket\n\n**Spec:** docs/projeto/specs/demanda-inexistente.md\n')
    result = subprocess.run(
        ['grep', '-L', r'^\*\*Spec:\*\* docs/projeto/specs/[a-z0-9-]*\.md', str(ticket)],
        capture_output=True, text=True,
    )
    print('Aceite lista ticket:', bool(result.stdout.strip()))
    print('Spec apontada existe:', Path('docs/projeto/specs/demanda-inexistente.md').exists())
```

## Validação e fechamento do parecer

Foram confrontados a spec, o relatório, `criar-spec`, `implementar-spec`,
`midia/arquivo.md`, o ADR 0008 e as instruções do projeto. Os desvios declarados
no relatório estão presentes na implementação, incluindo a quarta conferência
e a execução da operação depois da escolha do Matt.

Não foram repetidas as verificações por subagentes nem invocadas as skills do
Matt. O teste de uso real permanece aberto, como o relatório declara; cabe ao
titular encerrá-lo. Esta revisão não transforma evidência estática em evidência
de comportamento.

O ritual de `aicf:fechar-demanda` foi limitado ao parecer, respeitando a regra
que restringe a escrita do Codex a esta pasta. Nenhum arquivo da implementação
foi modificado, nenhuma demanda foi movida e nenhuma promoção foi aplicada.
O parecer será commitado separadamente; envio e CI ficam com o agente líder
ou titular.

`./scripts/check.sh` terminou em `Tudo verde.`, saída 0, com Claude Code
`2.1.296`, ambas as validações aprovadas e versão `0.38.0` no topo do changelog.
O parecer passou por `git diff --cached --check` antes do commit.
