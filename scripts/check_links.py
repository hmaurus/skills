#!/usr/bin/env python3
"""Confere se todo link relativo de markdown do repositório existe no disco.

Varre o texto inteiro, não linha a linha: link de markdown pode ter o rótulo
quebrado em duas linhas, e quatro deles existem aqui hoje.

Fora do escopo, por decisão da spec `nenhum-teste-acusa-link-morto`: âncoras
(`arquivo.md#secao`) — o destino conferido é o arquivo, nunca a seção.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Nos templates o link relativo fala do projeto que vai receber a cópia, não
# deste repositório. Ponto cego assumido: link quebrado dentro de um template
# passa batido.
DIRETORIOS_IGNORADOS = ("skills/setup/templates",)

# Placeholder de caminho (`../intents/<nome>.md`) não é link para arquivo.
DESTINOS_IGNORADOS = ("<", ">")

ESQUEMAS_EXTERNOS = ("http://", "https://", "mailto:")

LINK = re.compile(
    r"\[[^\]]*\]\(\s*([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\s*\)", re.DOTALL
)


def arquivos_markdown():
    for caminho in sorted(RAIZ.rglob("*.md")):
        relativo = caminho.relative_to(RAIZ).as_posix()
        if relativo.startswith(".git/"):
            continue
        if any(relativo.startswith(d + "/") for d in DIRETORIOS_IGNORADOS):
            continue
        yield caminho


def main():
    conferidos = 0
    quebrados = []

    for caminho in arquivos_markdown():
        texto = caminho.read_text(encoding="utf-8")
        for achado in LINK.finditer(texto):
            destino = achado.group(1)
            if destino.startswith("#"):
                continue
            if destino.lower().startswith(ESQUEMAS_EXTERNOS):
                continue
            if any(marca in destino for marca in DESTINOS_IGNORADOS):
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
