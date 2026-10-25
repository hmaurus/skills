# A comparação com os vizinhos envelheceu no pós-demanda

Processo — entrevista: a definir · implementação: a definir

Uma pesquisa em fonte primária de 2026-10-25 releu o que Superpowers, Matt Pocock, Spec Kit e
OpenSpec fazem depois da implementação. As frases do `README.md` sobre o Superpowers e o Matt não
estão erradas, mas deixam de fora o que mudou desde a
[pesquisa de 2026-09-19](../../referencias/governanca-nos-frameworks-vizinhos.md): o Superpowers
passou a relatar as decisões que toma sozinho, e os mantenedores do Matt e do Spec Kit recusaram
de forma explícita o registro pós-demanda. A recusa é decisão de escopo, não descuido, e o README
hoje deixa isso implícito.

Os comandos usam `$R` como pasta dos clones, nestes shas:

| Repositório | sha | Versão |
| --- | --- | --- |
| `obra/superpowers` | `2ce8aa1` | 7.0.1 |
| `mattpocock/skills` | `5beb35b` | 1.3.1 |
| `github/spec-kit` | `67e0f72` | 1.2.4.dev0 |
| `Fission-AI/OpenSpec` | `6d04a1b` | 1.15.0 |

## O que mudou ou faltou

- **O Superpowers relata as decisões e depois apaga o arquivo.** O README diz que ele "revisa o
  código contra o plano a cada tarefa, mas não atualiza o plano nem a spec com o que mudou"
  (`grep -n 'não atualiza o plano nem a spec' README.md`). Isso continua certo. O que falta: o
  `subagent-driven-development` anota cada decisão tomada sem o humano como `Ruling:` num arquivo
  de controle, junta as linhas na mensagem final sob "Rulings I made" e apaga o arquivo: *"the git
  history is the record now"*.
  Conferir: `sed -n 31,46p $R/superpowers/skills/subagent-driven-development/references/final-review.md`.
  O mantenedor não recusa a ideia de manter spec e plano atualizados: na
  [#921](https://github.com/obra/superpowers/issues/921), aberta, escreveu *"we want something
  here"*; a #1841 e a #2249 foram fechadas como duplicatas dela.
  Conferir: `gh issue view 921 -R obra/superpowers --json state,comments --jq '.state'`.
- **O Matt recusou exatamente o registro pós-demanda.** A
  [#1134](https://github.com/mattpocock/skills/issues/1134) pedia um arquivo de notas de
  implementação com decisões e desvios; fechada como "not planned", com resposta gerada por IA na
  triagem: ele só muda skill diante de falha observada, e isso cabe no `CLAUDE.md` de cada um. Na
  [#508](https://github.com/mattpocock/skills/issues/508), em 2026-10-24, ele mesmo: *"every team
  has their own process here so I'm not sure I want to mandate anything"*.
  Conferir: `gh issue view 1134 -R mattpocock/skills --json state,stateReason`;
  `gh issue view 508 -R mattpocock/skills --comments | grep -n 'every team'`.
- **O Spec Kit declara o pós-entrega como escolha do time e recusou pôr no núcleo.**
  `docs/concepts/spec-persistence.md`: *"Spec Kit intentionally leaves teams in control of what
  happens to spec.md, plan.md, and tasks.md after a feature is delivered."* A
  [#4940](https://github.com/github/spec-kit/issues/4940) pedia esse passo no núcleo e foi fechada
  como "not planned"; o catálogo da comunidade tem extensões para isso (`reconcile`,
  `retrospective`, `intent`, `sync`).
  Conferir: `sed -n 1,30p $R/spec-kit/docs/concepts/spec-persistence.md`;
  `grep -nE '"id": "(reconcile|retrospective|intent|sync)"' $R/spec-kit/extensions/catalog.community.json`.
- **O OpenSpec atualiza os artefatos durante a implementação.** O `apply` sugere atualizar o design
  quando a implementação mostra que o caminho não serve, e o `archive` guarda a pasta da mudança. A
  seção "Por que este" do README não cita o OpenSpec nem o Spec Kit.
  Conferir: `grep -n 'suggest updating artifacts' $R/OpenSpec/src/core/templates/workflows/apply-change.ts`.

## O que já se sabe

- A regra do `.claude/CLAUDE.md` vale aqui: cada frase nova sobre ferramenta de terceiro roda o
  comando que a confere, no clone do sha pinado, antes de ir para o arquivo.
- O pitch do README tem demanda própria:
  [o pitch do README põe na frente o que o titular ainda não validou](o-pitch-do-readme-poe-na-frente-o-que-nao-foi-validado.md).
  Se ela tirar "O que saiu de fato?" da abertura, parte desta comparação muda de lugar ou sai.

## Perguntas para a entrevista

- A seção "Por que este" passa a citar OpenSpec e Spec Kit, ou continua só com Superpowers, Matt,
  GSD e BMAD?
- Dizer que a ausência é decisão de escopo dos mantenedores, com o link da recusa, ou só descrever
  o que cada um faz?
- A pesquisa de 2026-09-19 em `docs/referencias/` ganha um adendo com estes achados, ou vira uma
  pesquisa nova?
