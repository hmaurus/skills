#!/usr/bin/env bash
# Verificação deste repositório: links de markdown, formato do plugin e entrada
# da versão no changelog. Roda localmente antes de commitar, e é o mesmo script
# que o .github/workflows/ci.yml executa depois do push.
#
# Os três checks rodam sempre, mesmo se um falhar: quem rodou quer ver tudo o
# que está vermelho de uma vez.
set -u

# readlink -f resolve symlink: chamado por atalho em ~/bin, o script ainda acha
# o repositório, em vez de rodar no diretório errado e culpar os arquivos.
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1

falhou=0

reprova() {
  echo "✗ $1"
  falhou=1
}

# Dependência ausente falha com o próprio nome, nunca com a acusação do check
# que ela impediu de rodar.
for programa in claude python3; do
  if ! command -v "$programa" >/dev/null 2>&1; then
    echo "✗ $programa não está instalado — a verificação não roda."
    [ "$programa" = claude ] && echo "  Instale com: npm i -g @anthropic-ai/claude-code"
    exit 1
  fi
done

# A versão local é sempre a mais nova e é ela que descobre cedo uma exigência
# nova do formato de plugin; o CI usa uma versão pinada. Imprimir qual rodou é
# o que torna a divergência visível.
echo "Claude Code: $(claude --version)"
echo

echo "→ Links relativos de markdown"
python3 scripts/check_links.py || reprova "há link de markdown apontando para arquivo que não existe"
echo

# O alvo `.` valida os dois manifestos de .claude-plugin/ (plugin.json e
# marketplace.json); o alvo `skills` valida o frontmatter das skills.
echo "→ Formato do plugin (claude plugin validate --strict)"
claude plugin validate . --strict || reprova "os manifestos de .claude-plugin/ não passaram no validate"
claude plugin validate skills --strict || reprova "o frontmatter de alguma skill não passou no validate"
echo

echo "→ A versão do plugin tem entrada no CHANGELOG.md"
versao=$(grep -m1 '"version"' .claude-plugin/plugin.json | sed 's/.*"version" *: *"\([^"]*\)".*/\1/')
topo=$(grep -m1 '^## ' CHANGELOG.md | sed 's/^## \([^ ]*\) .*/\1/')
if [ -z "$versao" ]; then
  reprova "não achei o campo version no .claude-plugin/plugin.json"
elif [ "$versao" != "$topo" ]; then
  # Exigir o topo, e não uma linha qualquer, é o que pega o bump esquecido: a
  # versão antiga tem entrada no changelog e passaria em "existe em algum lugar".
  reprova "a versão $versao não é a entrada do topo do CHANGELOG.md (lá está $topo)"
else
  echo "$versao é a entrada do topo do changelog"
fi
echo

if [ "$falhou" -eq 0 ]; then
  echo "Tudo verde."
fi
exit "$falhou"
