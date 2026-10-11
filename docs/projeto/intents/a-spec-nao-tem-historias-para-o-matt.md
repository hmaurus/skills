# A spec do aicf não tem histórias para o caminho do Matt

Processo — entrevista: a definir · implementação: a definir

Quando a spec sugere implementar pelo Matt Pocock (`to-tickets` ou `implement`), o
`/aicf:criar-spec` poderia ganhar uma seção **opcional** de histórias de usuário: a lista "Como
<papel>, quero <x>, para <y>" que o `to-spec` do Matt exige. O objetivo é a cobertura de
comportamento que o Matt busca, sem trocar a spec do aicf pela dele.

## O que já se sabe

- **Origem:** num projeto privado que consome estas skills, a mesma entrevista (`grill-with-docs`)
  gerou duas specs, uma pelo `/aicf:criar-spec` e outra pelo `to-spec`, para comparar. Das 35
  histórias do `to-spec`, **4** diziam algo que a prosa da spec do aicf deixava implícito ou só
  registrava num ADR ou na lista de testes: um efeito que *não* acontece, uma restrição de acesso
  por papel, a perda de acesso ao desativar, e uma regra de desenvolvedor escrita como
  necessidade. As outras 31 repetiam a prosa. Medição feita à mão; não há comando que a refaça.
- **O que o `to-spec` exige e proíbe** (Matt Pocock 1.3.1):
  - exige as histórias:
    `grep -c '^## User Stories' ~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/to-spec/SKILL.md` → 1;
  - proíbe caminho de arquivo, que a spec do aicf nomeia em "Arquivos e interfaces":
    `grep -c 'Do NOT include specific file paths' …/to-spec/SKILL.md` → 1;
  - não tem a seção Verificação ponta a ponta.

  Trocar o `/aicf:criar-spec` pelo `to-spec` perderia os caminhos, a Verificação, a linha
  `Processo` e o `git mv` do intent, que o `to-spec` não faz.
- **Quem consome a spec do Matt não depende das histórias.** `to-tickets` e `implement` não as
  citam:
  `grep -ci 'user stor' …/engineering/to-tickets/SKILL.md …/engineering/implement/SKILL.md` → 0 e 0.
  O `to-tickets` pede comportamento do ponto de vista de quem usa e critérios de aceite, e uma
  spec do aicf sem histórias já gerou 9 tickets no mesmo projeto privado. A seção não é
  requisito de compatibilidade: é ganho de cobertura.
- **Hoje o `/aicf:criar-spec` não fala em histórias:**
  `grep -c 'istórias' skills/criar-spec/SKILL.md` → 0.

## Em aberto para a entrevista

- **Gatilho:** só quando a sugestão de implementação é do Matt (`to-tickets`, `implement`), ou
  sempre que a demanda tem mais de um papel de usuário, qualquer que seja o caminho? O ganho
  observado veio dos papéis (quem pode, quem não pode), não do caminho.
- **Tamanho:** o `to-spec` pede uma lista "extremely extensive". Na amostra, 31 de 35 histórias
  só repetiam a prosa. Pedir só as que acrescentam (o que *não* acontece, o que cada papel não
  pode) mantém o ganho sem duplicar a Solução.
- **Lugar e forma:** seção própria ("Histórias") depois de Solução, ou dentro dela. Em pt-BR
  ("Como <papel>, quero…, para…").
- **Onde fica o critério:** no `/aicf:criar-spec`, que escreve a seção, pela regra "critério mora
  na skill que o aplica". Ver se o `implementar-spec` precisa saber dela.
- **Verificação:** o `/aicf:criar-spec` o agente invoca sozinho, então o teste de comportamento é
  obrigatório. Uma passada numa demanda com dois ou mais papéis e sugestão do Matt, conferindo a
  seção na spec gravada.
