# A entrada de quem chega: o setup se apresenta, e a documentação se divide em duas

Processo — entrevista: a definir · implementação: a definir

## Problema

O material de entrada do aicf está escrito para quem **já sabe o que é isso**. Três sintomas
verificáveis:

**1. O `/aicf:setup` não se apresenta.** A skill abre em "Perguntar, em pergunta aberta: 1. Nome do
projeto". Quem roda o comando pela primeira vez começa a responder perguntas antes de saber o que
está sendo montado, para que serve, ou o que vai mudar no jeito de trabalhar. O fim tem quatro
passos ("Ao terminar"), mas eles apontam para outras skills — nenhum aponta para o `README.md` como
o lugar de voltar quando quiser reler como o método funciona.

**2. O `README.md` explica o produto pela comparação com produtos que o leitor talvez não conheça.**
A segunda seção inteira ("Onde ele entra", ~25% do arquivo) é uma análise comparativa contra
Superpowers e Matt Pocock — posicionamento excelente para quem já usa as duas coleções, e um muro
para quem está começando, que encontra `brainstorming`, `grill-with-docs`,
`subagent-driven-development` e `to-tickets` citados como se fossem óbvios, antes de qualquer
"como eu começo". O primeiro parágrafo abre com "governança", "planejamento macro" e "agnóstico
quanto ao caminho de implementação".

**3. Comando útil aparece de passagem, sem o leitor saber que existe.** O `grilling` do Matt — que
contesta a ideia antes de você escrevê-la — é citado **uma vez**, dentro do passo 2 de "Começando
um projeto novo", numa linha de lista. Quem não leu aquele parágrafo específico não sabe que a
ferramenta existe. Não há diagrama nenhum no arquivo.

**4. A tabela de skills mistura duas coisas que o leitor precisa distinguir.** Das seis skills, só
duas são invocadas pelo usuário (`setup` e `criar-prd`, marcadas `disable-model-invocation: true`);
as outras quatro o agente carrega sozinho ao reconhecer a intenção. A tabela lista as seis em pé de
igualdade, então o iniciante acha que precisa decorar e digitar seis comandos, quando precisa de
dois.

## Solução pretendida

Dividir a documentação por **quem precisa dela**, não por assunto:

- **`README.md` — para quem chega.** O que o método faz e no que ajuda, em linguagem comum; o
  passo a passo do ciclo, de preferência em **diagrama**; e só os comandos que o **usuário** de
  fato digita. A comparação com as outras coleções desce para o fim, ou sai para o manual: ela
  responde "por que este e não aquele", pergunta de quem já está decidindo entre ferramentas, não
  de quem está entendendo a primeira.
- **`MANUAL.md` (ou `TUTORIAL.md`) — para quem já usa.** O detalhe: as skills que o agente invoca
  sozinho, os caminhos de entrevista e implementação, as convenções de governança, a comparação
  com Superpowers e Matt Pocock, e os comandos vizinhos que valem conhecer — com uma linha dizendo
  **para que serve cada um**, que é o que falta hoje no caso do `grilling`.
- **`/aicf:setup` se apresenta e se despede.** Abertura curta antes da primeira pergunta: o que o
  método faz e o que vai ser criado. Fechamento com o passo a passo do que fazer em seguida,
  apontando o `README.md` como o lugar de voltar.

## O que decidir na entrevista

- **`MANUAL.md` ou `TUTORIAL.md`?** São coisas diferentes: manual é referência para consulta,
  tutorial é percurso guiado do começo ao fim. O conteúdo listado acima é referência — o nome
  provavelmente é manual, mas vale confirmar se o que falta não é justamente um percurso.
- **Que diagrama, e em quê.** Mermaid renderiza nativamente no GitHub e é versionável em texto,
  o que casa com o resto do repositório. Um diagrama só do ciclo (demanda → entrevista →
  implementação → fechamento), ou um segundo mostrando os caminhos de cada fase? Diagrama demais
  vira outro muro.
- **Quanto do `README.en.md` acompanha.** Ele existe e vai divergir. Traduzir tudo dobra o custo
  de manutenção de cada mudança futura.
- **A apresentação do setup fica na skill ou num arquivo à parte?** Se ficar na skill, ela é lida
  em toda invocação e engorda o contexto; se sair, é mais um arquivo para manter em dia — e o
  repositório já pagou para aprender que índice e cópia envelhecem
  ([o índice envelhece sem avisar](../specs/concluidas/o-indice-envelhece-sem-avisar.md), entregue
  na `0.14.0`). O que existe hoje contra isso é o passo 5 do fechamento, que confere pares
  seção↔pasta: um arquivo de apresentação solto não tem par nenhum e ficaria fora dele.

## Restrição

**A apresentação não pode virar mais um muro.** O defeito diagnosticado é excesso de contexto
antes da primeira ação útil; abrir o `/aicf:setup` com três parágrafos sobre governança seria o
mesmo erro em lugar novo. O alvo é o leitor saber, em poucas linhas, o que está prestes a ganhar —
e começar.
