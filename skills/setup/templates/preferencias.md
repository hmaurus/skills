## Idioma

Código em inglês (variáveis, funções, classes, entidades). Comunicação com o usuário e documentação em português — commits, issues, mensagens de erro, comentários. Termos técnicos e identificadores ficam na forma original.

Manter a acentuação correta. Nunca trocar caractere acentuado pelo equivalente ASCII.

## Dependências e documentação

Preferir versões estáveis mais recentes. **Antes de usar a API de uma biblioteca externa, consultar a documentação oficial** — ou um MCP de documentação, como o Context7. Conhecimento de treino envelhece; documentação, não. Em dúvida entre versões, perguntar.

## Implementação

- **KISS/YAGNI:** evitar abstração desnecessária e over-engineering.
- **Gerenciador de pacotes:** respeitar o que o projeto declara (campo `packageManager`, lockfile presente). Nunca misturar `npm`, `yarn` e `pnpm` no mesmo repositório — gera lockfile e `node_modules` divergentes.
- **Documentação de código só para o que a assinatura não diz:** unidade (centavos, epoch ms), pré-condição, efeito colateral, `@throws`, `@deprecated`. Nunca parafrasear a assinatura.
- **Cabeçalho de arquivo só para contrato que o código não mostra:** fronteira de runtime, restrição de import, quem pode escrever no quê, posição no pipeline.

## Validação

Antes de commitar: lint + format + typecheck **no projeto inteiro, nunca só nos arquivos tocados**. Rodar via script do `package.json`, nunca o binário cru. Após o push, verificar o CI em vez de presumir que passou.

## Testes

- Unitário e de integração primeiro; E2E para fluxo crítico.
- Cobertura alta onde a falha custa dinheiro ou dado: pagamento, autenticação, migration. Percentual global não é meta.

## Design

- **Acessibilidade:** WCAG 2.2 AA.
- **Responsivo:** mobile-first, alvo de toque de 44px.
- **Performance:** medir com dado de campo na região do público, não score de laboratório.
- Animação sutil, sem bloquear o fluxo.

## Segurança

- Nunca commitar `.env` — apenas `.env.example`.
- Validar as variáveis de ambiente na inicialização, com schema.
- **Credencial nunca entra no chat nem em output.** O usuário salva no `.env` (ou no gerenciador de senhas) e avisa só o nome da variável; o agente lê via `process.env` ou `grep` ancorado (`^NOME_DA_VAR`, nunca padrão largo). Conferir com booleano — existe? tem o prefixo esperado? —, nunca imprimir o valor. Motivo: o chat persiste em transcript no disco e trafega pela infraestrutura do provedor; o `.env` fica só na máquina.
- Se uma credencial vazar por engano, rotacionar no provedor imediatamente. É rápido, e a chave antiga morre em segundos.
