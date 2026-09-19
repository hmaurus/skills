#!/usr/bin/env python3
"""Confere se todo link relativo de markdown do repositório existe no disco.

Duas decisões que o código sozinho não explica:

- **Varre o texto inteiro, não linha a linha.** Link de markdown pode ter o
  rótulo quebrado em duas linhas, e quatro deles existem aqui hoje.
- **Mascara código antes de procurar link.** Este é um repositório sobre
  escrever markdown com link relativo: link de exemplo dentro de bloco cercado
  ou de crase é ilustração, não link. Sem isso o primeiro exemplo novo deixaria
  o check vermelho por um não-defeito. A máscara troca o trecho por espaços,
  para que o número da linha continue certo.

Fora do escopo, por decisão da spec `nenhum-teste-acusa-link-morto`: âncoras
(`arquivo.md#secao`) — o destino conferido é o arquivo, nunca a seção. Ponto
cego conhecido: link de referência (`[rótulo][id]` com `[id]: destino` à
parte), forma que o repositório não usa hoje.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Nos templates o link relativo fala do projeto que vai receber a cópia, não
# deste repositório. Ponto cego assumido: link quebrado dentro de um template
# passa batido.
DIRETORIOS_IGNORADOS = ("skills/setup/templates",)

ESQUEMAS_EXTERNOS = ("http://", "https://", "mailto:")

CERCA = re.compile(r"^\s*(```|~~~)")
CRASES = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\s*\)")


def arquivos_markdown():
    for caminho in sorted(RAIZ.rglob("*.md")):
        relativo = caminho.relative_to(RAIZ).as_posix()
        if relativo.startswith(".git/"):
            continue
        if any(relativo.startswith(d + "/") for d in DIRETORIOS_IGNORADOS):
            continue
        yield caminho


def mascarar_codigo(texto):
    """Troca bloco cercado e código inline por espaços, preservando offsets."""
    linhas = texto.split("\n")
    dentro = False
    for i, linha in enumerate(linhas):
        if CERCA.match(linha):
            dentro = not dentro
            linhas[i] = " " * len(linha)
        elif dentro:
            linhas[i] = " " * len(linha)
    return CRASES.sub(lambda m: " " * len(m.group(0)), "\n".join(linhas))


def main():
    conferidos = 0
    quebrados = []

    for caminho in arquivos_markdown():
        texto = mascarar_codigo(caminho.read_text(encoding="utf-8"))
        for achado in LINK.finditer(texto):
            destino = achado.group(1)
            if destino.startswith("#"):
                continue
            if destino.lower().startswith(ESQUEMAS_EXTERNOS):
                continue
            alvo = destino.split("#", 1)[0]
            if not alvo:
                continue
            conferidos += 1
            base = RAIZ if alvo.startswith("/") else caminho.parent
            if (base / alvo.lstrip("/")).exists():
                continue
            linha = texto.count("\n", 0, achado.start()) + 1
            quebrados.append((caminho.relative_to(RAIZ).as_posix(), linha, destino))

    for arquivo, linha, destino in quebrados:
        print(f"  {arquivo}:{linha} -> {destino}", file=sys.stderr)

    print(f"{conferidos} links conferidos, {len(quebrados)} quebrados")
    return 1 if quebrados else 0


if __name__ == "__main__":
    sys.exit(main())
