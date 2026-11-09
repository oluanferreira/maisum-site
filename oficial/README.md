# +UM — Homepage oficial, prévia

## Jornada e direção
- Home: promessa 2 por 1, presença real de Léo, quatro exemplos, funcionamento, oferta anual e dúvidas.
- `/experiencias`: catálogo público e fichas. Links usam `?experiencia=<benefit_id>#experiencia-<benefit_id>` para integração com a v5.
- Checkout direto e secundário para descoberta. Afiliação passa apenas quando explícita, única e válida na URL atual. Sem storage, cookies ou atribuição orgânica.
- Creme, laranja e carvão; DM Sans e Cormorant. A composição de Léo aparece uma única vez na página. As quatro fichas de exemplo mantêm fotografias dos itens já usados no site.

## Fatos
- Luan confirmou que existem mais de 50 experiências. Os 32 registros operacionais são ofertas/benefícios, alguns abrangendo cardápios completos. Não usar 32 como total de experiências.
- Todas as experiências são 2 por 1, conforme esclarecimento de Luan. Condições e intervalos variam por parceiro.
- Checkout verificado em 09/11/2026: https://pay.cakto.com.br/3e7t64x_1061003 ; R$ 97,00/ano + R$ 0,99 de serviço, R$ 97,99 à vista, renovação anual. Parcelamento pode ter acréscimos.
- Quatro ofertas selecionadas usam IDs, nomes, valores e parceiros do snapshot operacional de 09/11/2026. A página aponta a necessidade de conferir a ficha atual.

## Composição de Léo
A imagem `assets/leo-gastronomia-v2.png` é uma composição publicitária gerada a partir de um frame real sorrindo de Léo Tavares e três referências reais de pratos. O frame de referência é `leo-sorrindo-reel-2025.jpg`, extraído pelo responsável de fotografia. Foram preservados os elementos visuais reconhecíveis do chapéu de faixa vermelha, óculos, barba grisalha, camiseta azul e gesto da mão. A imagem não é uma fotografia documental e não é idêntica em pixels ao frame original. A semelhança e a composição final precisam da aprovação visual de Luan.

O arquivo RGBA tem 1254×1254 pixels. É exibido por inteiro com `object-fit: contain`, sem recortar cabeça, corpo ou pratos. A legenda fica fora da imagem. O retrato de 2023 e os dois cards sobrepostos foram removidos da apresentação do hero; não usar o retrato anterior como versão final.

## Integração
Alterados somente `index.html`, novos `oficial/` e `tests/oficial_smoke.py`. `styles.css`, `script.js`, `/oferta`, `/links`, `/experiencias`, guias e páginas de parceiros não foram alterados nesta branch. Reutiliza as fontes locais já existentes em `/links/fonts/`.

A prévia tem `noindex,nofollow`. Não promover para produção antes de revisar imagem, oferta, condições e navegação integrada. Não há mudanças de domínio, DNS, checkout ou pagamentos.

## QA
`python tests/oficial_smoke.py` com Playwright e Chromium instalados. Gera screenshots e resultados em `qa-artifacts/oficial`, ou em `OFICIAL_QA_DIR` se definido. Cobre 320, 390, 540, 768, 1024 e 1440px, fontes, imagens, overflow, console, uma composição inteira de Léo, +50, checkout, afiliação válida/duplicada/inválida/ausente, menu, FAQ, teclado e conteúdo sem JavaScript.
