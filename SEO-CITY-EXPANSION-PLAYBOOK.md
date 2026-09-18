# Playbook SEO por Cidade — +UM

## Objetivo

Toda nova cidade do +UM deve nascer com uma estrutura pública que ajude Google, buscadores locais e sistemas de IA a entenderem:

1. que o +UM opera naquela cidade;
2. quais experiências e parceiros são reais;
3. que o +UM pertence à categoria 2 por 1 / pague 1 e ganhe 1;
4. que também pode responder a intenções como tour gastronômico, roteiro gastronômico, clube de benefícios e experiências para casal;
5. como o +UM se diferencia de outras marcas da categoria.

Vitória da Conquista é a cidade-base e serve como referência para próximas expansões.

---

## 1. Regra de ativação

Nunca publicar uma cidade só para capturar tráfego.

Uma cidade só recebe páginas locais indexáveis quando:

- existe operação +UM real;
- há ao menos parceiros/experiências confirmados;
- a página pode mostrar conteúdo específico daquela praça;
- existe destino real para conversão/catálogo.

Se ainda não houver operação, trabalhar a consulta dentro de páginas nacionais/editoriais, não em uma landing local falsa.

---

## 2. Estrutura obrigatória por cidade

Para uma cidade com slug `{cidade}`:

- `/guias/{cidade}/` — hub local;
- `/guias/{cidade}/tour-gastronomico/`;
- `/guias/{cidade}/restaurantes-2-por-1/`;
- futuramente `/guias/{cidade}/experiencias-para-casal/`;
- futuramente `/guias/{cidade}/onde-comer-gastando-menos/`;
- diretório de parceiros/experiências da praça quando houver dados estruturados suficientes.

Páginas nacionais permanecem compartilhadas:

- `/guias/como-funciona-pague-1-ganhe-1/`;
- `/guias/apps-2-por-1-brasil/`;
- `/guias/brasil-em-dobro-alternativas/`;
- `/guias/compre-e-ganhe-alternativas/`.

---

## 3. Clusters que toda cidade deve avaliar

### Marca + local

- +UM {cidade}
- MaisUm {cidade}
- +UM restaurantes {cidade}
- +UM experiências {cidade}

### Benefício

- restaurante 2 por 1 {cidade}
- pague 1 ganhe 1 {cidade}
- dois pelo preço de um {cidade}
- prato em dobro {cidade}
- promoção para casal {cidade}

### Tour / descoberta

- tour gastronômico {cidade}
- roteiro gastronômico {cidade}
- circuito gastronômico {cidade}
- passaporte gastronômico {cidade}
- clube gastronômico {cidade}
- tour de restaurantes {cidade}
- experiência gastronômica {cidade}

### Ocasião

- onde comer {cidade}
- onde sair a dois {cidade}
- experiências para casal {cidade}
- lugares diferentes para conhecer {cidade}
- o que fazer no fim de semana {cidade}

### Concorrência

Pesquisar quais marcas realmente operam ou são buscadas na região.

Exemplos nacionais/categoria:
- Brasil em Dobro;
- operações regionais "Em Dobro";
- Compre & Ganhe;
- outros clubes, passaportes e tours relevantes daquela praça.

Não copiar páginas de concorrentes. Criar conteúdo comparativo factual e útil.

---

## 4. Pacote técnico por página

Toda página local deve ter:

- title único;
- description única;
- canonical;
- H1 alinhado à intenção;
- resposta direta no início;
- texto específico da cidade;
- links para experiências/parceiros reais;
- BreadcrumbList;
- WebPage/Article schema quando aplicável;
- FAQ somente quando houver perguntas respondidas visivelmente;
- links internos para o hub da cidade e para o catálogo;
- data de atualização quando houver conteúdo volátil;
- entrada no sitemap.

---

## 5. Estrutura editorial

### Primeiros 10 segundos

Responder a intenção imediatamente.

Exemplo:

> Procura restaurante 2 por 1 em {cidade}? O +UM reúne experiências locais em que, conforme a regra do parceiro, você paga por um item e ganha outro.

### Corpo

1. definição;
2. contexto da cidade;
3. como funciona;
4. exemplos atuais;
5. regras;
6. links para parceiros;
7. dúvidas relacionadas;
8. CTA.

Não criar texto genérico trocando apenas o nome da cidade.

---

## 6. Grafo local de entidades

Para cada cidade:

`+UM ↔ cidade ↔ parceiro ↔ experiência ↔ categoria ↔ benefício 2 por 1`

Cada parceiro prioritário deve, quando possível:

- ter página pública única no +UM;
- mencionar cidade e categoria;
- informar experiência e regras;
- usar imagem real;
- linkar Instagram/site oficial;
- receber um kit para mencionar/linkar o +UM nos próprios canais.

---

## 7. Concorrentes e "Em Dobro"

Objetivo: capturar demanda já educada por outras marcas sem induzir o usuário a erro.

Modelo de página:

1. o que é a marca pesquisada;
2. como funciona;
3. em que região opera segundo fonte atual;
4. categoria 2 por 1;
5. diferenças factuais;
6. +UM como alternativa apenas onde houver presença real;
7. disclaimer de independência;
8. fontes oficiais.

Nunca:
- usar logo de concorrente;
- sugerir afiliação;
- usar marca concorrente no domínio;
- inventar cidade/preço/regra;
- gerar dezenas de páginas doorway.

---

## 8. Checklist de lançamento de uma nova cidade

### Antes do SEO local
- [ ] operação comercial confirmada
- [ ] catálogo real da cidade
- [ ] parceiros prioritários definidos
- [ ] cidade/UF padronizadas
- [ ] URLs oficiais dos parceiros
- [ ] fotos e experiências confirmadas

### Publicação
- [ ] criar config da cidade em `seo/cities/`
- [ ] criar hub local
- [ ] criar página 2 por 1
- [ ] criar página tour gastronômico
- [ ] adicionar links internos
- [ ] adicionar sitemap
- [ ] atualizar Organization/Service areaServed quando apropriado
- [ ] validar canonical/schema
- [ ] testar indexabilidade

### Autoridade
- [ ] kit de lançamento para parceiros
- [ ] posts "Agora somos +UM"
- [ ] links de parceiros para páginas oficiais
- [ ] vídeos locais respondendo buscas
- [ ] menções editoriais locais legítimas

### Monitoramento
- [ ] Search Console por consultas da cidade
- [ ] impressões não-branded
- [ ] páginas indexadas
- [ ] referências em IA
- [ ] conversões orgânicas
- [ ] revisar conteúdo e parceiros mensalmente

---

## 9. Cidade-base

Implementação inicial:

- Vitória da Conquista, BA
- slug: `vitoria-da-conquista`
- hub: `/guias/vitoria-da-conquista/`
- tour: `/guias/vitoria-da-conquista/tour-gastronomico/`
- 2 por 1: `/guias/vitoria-da-conquista/restaurantes-2-por-1/`

Usar essa implementação como padrão estrutural, não como conteúdo para copiar literalmente.
