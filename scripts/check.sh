#!/usr/bin/env bash
# Verificação deste repositório: links de markdown, formato do plugin e entrada
# da versão no changelog. Roda localmente antes de commitar, e é o mesmo script
# que o .github/workflows/ci.yml executa depois do push.
#
# Os três checks rodam sempre, mesmo se um falhar: quem rodou quer ver tudo o
# que está vermelho de uma vez.
set -uo pipefail

cd "$(dirname "$0")/.."

falhou=0

reprova() {
  echo "✗ $1"
  falhou=1
}

if ! command -v claude >/dev/null 2>&1; then
  echo "✗ claude não está instalado — o check de formato do plugin não roda."
  echo "  Instale com: npm i -g @anthropic-ai/claude-code"
  exit 1
fi

# A versão local é sempre a mais nova e é ela que descobre cedo uma exigência
# nova do formato de plugin; o CI usa uma versão pinada. Imprimir qual rodou é
# o que torna a divergência visível.
echo "Claude Code: $(claude --version)"
echo

echo "→ Links relativos de markdown"
python3 scripts/check_links.py || reprova "há link de markdown apontando para arquivo que não existe"
echo

echo "→ Formato do plugin (claude plugin validate --strict)"
claude plugin validate . --strict || reprova "o marketplace.json não passou no validate"
claude plugin validate skills --strict || reprova "o frontmatter de alguma skill não passou no validate"
echo

echo "→ A versão do plugin tem entrada no CHANGELOG.md"
versao=$(grep -m1 '"version"' .claude-plugin/plugin.json | sed 's/.*"version" *: *"\([^"]*\)".*/\1/')
if [ -z "$versao" ]; then
  reprova "não achei o campo version no .claude-plugin/plugin.json"
elif grep -q "^## $versao — " CHANGELOG.md; then
  echo "$versao tem entrada no changelog"
else
  reprova "a versão $versao não tem a linha '## $versao — <data>' no CHANGELOG.md"
fi
echo

if [ "$falhou" -eq 0 ]; then
  echo "Tudo verde."
fi
exit "$falhou"
