# O `validate` do Claude Code 2.1.292 reprova o `CLAUDE.md` da raiz

Processo — entrevista: a definir · implementação: a definir

O `./scripts/check.sh` sai com 1 na máquina de quem desenvolve, com o repositório intacto, e o CI
continua verde. Enquanto isso durar, o check local é vermelho sempre, e uma falha de verdade passa
no meio. Vem antes de [o Matt renomeou o glossário](../intents/o-matt-renomeou-o-glossario.md), por
escolha do usuário: aquela demanda vai precisar do check confiável.

## O que já se sabe

- **A causa é um aviso novo do validador.** Com o Claude Code 2.1.292, `claude plugin validate . --strict`
  (linha 44 do `scripts/check.sh`) devolve:

  ```
  ❯ root: CLAUDE.md at the plugin root is not loaded as project context. To ship context with your plugin, use a skill (skills/<name>/SKILL.md) instead.
  ✘ Validation failed (--strict treats warnings as errors)
  ```

  O `--strict` trata aviso como erro. O `claude plugin validate skills --strict`, da linha 45, passa.
- **O CI passa porque fixa uma versão anterior:** `npm i -g @anthropic-ai/claude-code@2.1.278`
  (linha 26 do `.github/workflows/ci.yml`), que não tem o aviso.
- **Não é efeito de nenhuma mudança do repositório.** Em 2026-10-06, com as mudanças do commit
  `920851a` desfeitas (`git stash`), o check saiu com 1 do mesmo jeito.
- **Por que o aviso aparece aqui:** o `marketplace.json` declara o plugin `aicf` com
  `"source": "./"`, então a raiz do repositório é a raiz do plugin, e o `CLAUDE.md` de quem
  desenvolve o aicf fica nela. O aviso é verdadeiro — o arquivo não chega a quem instala o plugin —,
  mas aqui não se pretende que chegue.
- **A regra do repositório já prevê o fim:** quando o check local reprovar com uma versão mais nova
  que a do `ci.yml`, subir o pin (seção de verificação do `CLAUDE.md`). Subir o pin hoje deixaria o
  CI vermelho também; o pin sobe junto com o conserto.

## Em aberto para a entrevista

- **Como o aviso deixa de reprovar.** Caminhos vistos, sem avaliação:
  - o plugin passar a morar numa subpasta (`"source": "./plugin"`, por exemplo), separando o
    repositório do plugin — muda o caminho de tudo que o plugin publica;
  - o `check.sh` ler `--json` e ignorar só esse aviso, mantendo o `--strict` para o resto. No
    `--json` o aviso vem com `"code": null`, então o filtro casaria pela mensagem — e quebra
    quando o texto do validador mudar;
  - tirar o `--strict` da linha 44 — perde os avisos que hoje pegam campo desconhecido e metadado
    faltando.
- **Se o `AGENTS.md` da raiz entra no mesmo raciocínio**, embora o validador não reclame dele hoje.
