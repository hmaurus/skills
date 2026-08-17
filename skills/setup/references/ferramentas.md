# Catálogo de ferramentas — para a entrevista do setup

Material de consulta do agente. **Não despejar esta lista no usuário.** Perguntar categoria por
categoria; explicar para que serve só quando ele não souber ou pedir; sugerir opções só depois
de ele dizer que ainda não usa nada.

A recomendação marcada com ★ é o default deste kit — o que os projetos que originaram o método
usam. Não é a melhor para todo mundo: onde a escolha depende do caso, o texto diz de quê.

---

## Sempre perguntar

Estas quatro afetam quase qualquer projeto, e o agente vai esbarrar nelas na primeira semana.

### Gerenciador de senhas

**Para que serve, no contexto do agente:** o `.env` guarda credencial da máquina de quem
desenvolve. O que não cabe lá — senha de painel, chave de produção, credencial compartilhada
entre máquinas — precisa de um cofre. Os cofres têm CLI, então o agente consegue **ler um campo
específico sem o valor passar pelo chat**, o que não acontece quando o usuário cola a chave na
conversa.

| Opção         | Diferença                                                                 |
| ------------- | ------------------------------------------------------------------------- |
| ★ Bitwarden   | CLI `bw`, plano gratuito generoso, organização para separar cofre pessoal do de trabalho |
| 1Password     | CLI `op` com integração direta em `.env` (`op://` como valor); pago        |
| Só `.env`     | funciona sozinho numa máquina só. Some quando a máquina morre, e não dá para compartilhar |

**Se ele não usa nenhum:** não empurrar. Registrar "só `.env`" e seguir — a regra de nunca
colar credencial no chat vale igual.

### Hospedagem e deploy

**Para que serve:** onde a aplicação roda e como o código chega lá. Define mais coisa do que
parece: runtime disponível, se há servidor de longa duração, como as variáveis de ambiente são
configuradas, o que o agente pode automatizar.

| Opção            | Diferença                                                                    |
| ---------------- | ---------------------------------------------------------------------------- |
| ★ Cloudflare Workers | runtime na borda, banco e storage como binding nativo (D1, R2, KV), CLI `wrangler` completa. Exige código compatível com o runtime — nem toda lib de Node roda |
| Vercel           | caminho mais curto para Next.js, deploy por push, preview por PR             |
| Fly.io / Railway | container de longa duração; escolha quando o app precisa de processo persistente ou de imagem própria |
| VPS              | controle total, custo previsível, e todo o trabalho de manutenção é seu       |

### Banco de dados

**Para que serve:** onde o dado vive. A pergunta prática não é qual banco, é **serverless ou
persistente** — o primeiro cobra por uso e dorme, o segundo não.

| Opção          | Diferença                                                                     |
| -------------- | ----------------------------------------------------------------------------- |
| ★ Neon         | Postgres serverless, branch de banco por PR, escala a zero. Latência maior no primeiro acesso após dormir |
| Supabase       | Postgres com auth, storage e realtime no mesmo pacote — menos peça para montar |
| Turso / D1     | SQLite distribuído; ótimo para leitura na borda, limitado em escrita concorrente |
| Postgres local + Docker | zero custo, zero dependência externa; alguém precisa cuidar de backup e do deploy do banco |

Perguntar também se há **Postgres local compartilhado entre projetos** — é comum, e muda como
as portas e o `DATABASE_URL` são configurados.

### CI

**Para que serve:** rodar os checks e os testes em máquina limpa a cada push, para o "na minha
máquina funciona" morrer cedo. Sem isso, o agente afirma que passou baseado na própria máquina.

| Opção            | Diferença                                                     |
| ---------------- | ------------------------------------------------------------- |
| ★ GitHub Actions | integrado ao repositório, `gh` CLI permite ao agente acompanhar o run |
| GitLab CI        | equivalente, se o repositório está lá                         |
| Nenhum           | válido no começo. Registrar como tal, para o agente não presumir que existe |

---

## Perguntar só se o projeto pedir

Não interrogar sobre estas de saída. Perguntar quando a descrição do projeto indicar que fazem
falta — app com login, com cobrança, com envio de email.

### Autenticação

Login, sessão, senha, OAuth. Errar aqui custa caro, e é a área onde escrever do zero mais
raramente compensa.

★ **Better Auth** (biblioteca, o dado fica no seu banco) · **Clerk** (serviço, UI pronta, cobra
por usuário ativo) · **Auth.js** (padrão do ecossistema Next) · **Supabase Auth** (se o banco já
é Supabase).

### Pagamento

★ **Stripe** (referência internacional, documentação e API excelentes) · **Pagar.me** ou
**Mercado Pago** (Brasil: PIX, boleto, parcelamento em 12x — que o Stripe não faz no país) ·
**Paddle** (atua como merchant of record e cuida de imposto sobre venda internacional).

Regra que vale para todos: **valor em centavos**, sempre inteiro, nunca `float`.

### Email transacional

Confirmação de cadastro, recuperação de senha, recibo. Servidor SMTP próprio cai em spam — use
serviço com reputação e verificação de domínio.

★ **Resend** (API simples, templates em React) · **Postmark** (entregabilidade forte, mais
caro) · **AWS SES** (barato em volume, configuração mais trabalhosa).

### Erros e observabilidade

Sem isso, você descobre o erro quando o usuário reclama. Com isso, o agente lê o stack trace
real de produção em vez de adivinhar.

★ **Sentry** (erro, release, performance; MCP oficial permite ao agente consultar) ·
**Axiom** / **Better Stack** (foco em log e uptime).

### Analytics

★ **GA4** (gratuito, exportação para BigQuery, mas amostragem e pouca privacidade) ·
**PostHog** (evento e funil de produto, com replay de sessão) · **Plausible** / **Umami** (leve,
sem cookie, sem banner de consentimento).

### Mídia e conteúdo

Vídeo, imagem, áudio — só se o projeto tiver.

**Bunny Stream** ou **Mux** (hospedagem de vídeo com player e legenda) · **Cloudflare R2** ou
**S3** (arquivo grande; R2 não cobra egresso) · **faster-whisper** local (transcrição gratuita,
roda na GPU da própria máquina).

---

## Como registrar

Uma linha por ferramenta em uso, na seção `## Stack e serviços` do `CLAUDE.md` do projeto:

```
- **Hospedagem:** Cloudflare Workers — deploy por push na `main` via GitHub Actions
- **Banco:** Neon (Postgres) — `DATABASE_URL`
- **Senhas:** Bitwarden, organização `<nome>` — CLI `bw`
- **Pagamento:** Stripe — `STRIPE_SECRET_KEY`
```

**Nome da variável, nunca o valor.** É esse registro que evita o agente perguntar de novo a cada
sessão, e é ele que diz onde procurar quando uma credencial precisar ser rotacionada.

Categoria que o projeto não usa não vira linha. Lista de "não usamos X" é ruído.
