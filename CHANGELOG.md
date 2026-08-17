# Changelog

## 0.3.0 — 2026-08-17

- `setup` passa a oferecer os **padrões de engenharia** (idioma, KISS/YAGNI, validação antes do commit, testes, acessibilidade, tratamento de credencial), perguntando se vão para o `CLAUDE.md` global da máquina ou o do projeto. O global nunca é sobrescrito: quando já existe, a skill mostra o que falta e propõe.

## 0.2.0 — 2026-08-17

- `setup` — cria a base de um projeto novo: `docs/projeto/` com PRD e checklist, as pastas de demandas e o `CLAUDE.md` raiz. Só invocável pelo usuário.
- README reposicionado: o plugin é a **camada de governança** que falta às coleções focadas na demanda individual, e funciona sozinho ou por cima delas.
- README em inglês.

## 0.1.0 — 2026-08-17

Primeira versão pública.

- `workflow-demanda` — o ciclo de uma demanda: quatro fases, os caminhos de cada uma (nativo, Superpowers, Matt Pocock), nomenclatura, formato do relatório e ritual de fechamento.
- `criar-spec` — a fase de entrevista no caminho nativo: interroga até não sobrar decisão em aberto e escreve a spec no repositório.
- `implementar-spec` — a fase de implementação no caminho nativo: lê a spec, implementa, verifica no projeto inteiro e conduz o fechamento.
