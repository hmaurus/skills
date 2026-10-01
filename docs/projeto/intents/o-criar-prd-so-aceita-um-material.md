# O criar-prd só aceita um material de partida

Processo — entrevista: a definir · implementação: a definir

## Problema

O `/aicf:criar-prd` recebe um argumento só, `[arquivo ou texto de contexto]`: um caminho é lido como
arquivo, e qualquer outra coisa vira o próprio material. Projeto que chega à entrevista com vários
insumos — a ideia inicial, um levantamento de dores, o PRD de uma pesquisa anterior, uma lista de
hipóteses — não tem forma prevista de passá-los juntos.

O contorno que funciona hoje é mandar ler por texto, como em
`/aicf:criar-prd Leia todos os arquivos de docs/insumos/ antes da primeira pergunta.`. O agente
obedece, mas isso está fora do contrato da skill: pela letra, a frase é o material, não uma
instrução de leitura. Caso real: o VillaTT, em 2026-09-30, com quatro insumos vindos de um projeto
de pesquisa arquivado.

## O que se quer

O argumento aceita um ou mais materiais, misturados:

- **arquivo** — lido inteiro, como hoje;
- **pasta** — lidos todos os arquivos de texto dentro dela;
- **texto** — o próprio material, como hoje.

O `argument-hint` cita os tipos entre parênteses sem fechar a lista, para não parecer que o resto é
recusado. A regra que já vale para o material único continua valendo para cada um: ler tudo antes
da primeira pergunta, e **o que o material afirma se confirma com o usuário** — vários insumos não
viram vários PRDs decididos.

## A decidir na entrevista

- **"Repositório" entra como tipo?** A sessão já roda dentro de um repositório, então "o repositório"
  é a pasta `.` e não precisa de nome próprio; outro repositório local também é uma pasta. Sobra o
  repositório remoto (URL do GitHub), que exigiria `gh` e não parece valer o custo. A hipótese é não
  entrar.
- **Pasta lida recursivamente?** E o que fica de fora: binário, imagem, `node_modules`, arquivo
  enorme. Pasta grande pode estourar o contexto; talvez listar e perguntar acima de um limite.
- **Ordem e conflito entre materiais.** Quando dois insumos se contradizem, a entrevista pergunta —
  mas mostrar a contradição antes da primeira pergunta ou no ponto em que ela aparece?
- **Pasta convencional.** Se vale o setup ou o `criar-prd` sugerirem `docs/insumos/` como lugar
  padrão, para que a invocação sem argumento já encontre o material.
- **O `criar-spec` precisa do mesmo?** Ele não recebe argumento hoje.
