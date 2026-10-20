# Os padrões de engenharia

`templates/preferencias.md` é um corpo de seções (`## Idioma`, `## Implementação`, …) feito
para ser colado dentro de um `CLAUDE.md`, não para virar arquivo próprio.

**Completar o global, ou No global:**

1. Se o global não existe, criar com o conteúdo do template.
2. Se existe, **não sobrescrever e não anexar direto**: mostrar quais seções do template ainda
   não têm equivalente lá e propor acrescentar só essas. Aquele arquivo vale para todos os
   projetos da máquina — inclusive os que não usam este método. Mexer nele sem confirmação
   é fora de escopo desta skill.

**Acrescentar no projeto, ou No projeto:** colar no `CLAUDE.md` da raiz, depois de "Processos de
desenvolvimento", as seções que o global não tem — todas, quando não há global com padrões.

Havendo global com padrões, **padrão que já vale por ele não se repete no projeto**: cópia
reduzida da regra global enfraquece a regra.
