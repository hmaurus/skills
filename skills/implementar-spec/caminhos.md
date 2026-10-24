# Critério dos caminhos de implementação

Lido pelo `criar-spec`, ao gravar a sugestão de caminho, e pelo `implementar-spec`, ao decidir o
caminho. Oferecer só os caminhos instalados: a linha "Coleções de skills de workflow instaladas"
do `CLAUDE.md` diz quais.

- **`aicf-direto`**: cabe numa sessão e o diff se descreve numa frase, sem decisão de abordagem.
- **`aicf-plan`**: cabe numa sessão, mas tem abordagem a decidir ou vários arquivos. O plano é
  aprovado antes de mexer no disco.
- **`subagent-driven-development`** (Superpowers): muitos passos acoplados, em sequência, numa
  sessão, quando acertar cada passo vale mais que o tempo. Cada tarefa é revisada antes da
  próxima. É serial, um implementador por vez: **não se sugere para ganhar velocidade**.
- **`to-tickets`** (Matt): fatias verticais com dependência entre elas, que podem atravessar
  sessões. A forma de executar os tickets se decide depois deles, no `implementar-spec`.
