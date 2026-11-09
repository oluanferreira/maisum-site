# Central +UM

Central mobile-first em `/links`. Esta proposta não altera a homepage ou a página de oferta.

## Direção
Fotografia real, foco em descoberta e companhia, identidade laranja/creme do +UM, tipografia editorial e rotas com tratamento distinto. Navegação e destinos funcionam sem JavaScript; movimento respeita `prefers-reduced-motion`.

## Conteúdo e ativos
- Foto de pizza: ativo existente `/assets/pizzas.jpg`, apresentado no site oficial e na página pública de Pizzaria Vitória. Conferidos em 9 de novembro de 2026: https://appmaisum.com.br/parceiros/vitoria-da-conquista/pizzaria-vitoria
- Não apresenta preço de item, contagem de parceiros, avaliações ou percentual de comissão.
- Cadastro e login conferidos nos destinos oficiais `restaurante.appmaisum.com.br/cadastro` e `/login`.
- Font Bricolage Grotesque: Google Fonts, SIL Open Font License em `fonts/OFL.txt`. WOFF2 local com subconjunto latino; sem requisições externas de fontes.
- WhatsApp apenas prepara mensagens. O visitante precisa enviá-las. Nenhuma conversa é enviada pelo site.
- `affiliate` é repassado somente se explícito, único e válido. Não há armazenamento local ou afiliado padrão. A homepage existente faz o repasse ao checkout.

## Testes
`python -m unittest discover -s tests -v`
`node --test tests/central.test.cjs`
`python tests/browser_smoke.py` (requer Playwright/Chromium)

A suite confere que homepage, CSS principal, script principal e oferta permanecem byte a byte iguais à base original.
