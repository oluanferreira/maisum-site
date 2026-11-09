"""Render the approved public catalog snapshot to an accessible static page."""
import json,html,collections,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
e=html.escape
public=json.loads((ROOT/'experiencias/catalogo.json').read_text())
items=public['items']
arrow='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
cardlist=[]
for i,a in enumerate(items):
 rid='experiencia-'+a['id']
 search=' '.join([a['partner'],a['name'],a['category_label'],a['address'] or '',a['description']])
 rules=''.join('<li>'+e(r)+'</li>' for r in a['rules']) or '<li>Confira dias e horários diretamente na plataforma +UM.</li>'
 reuse=f'<p><strong>Intervalo de uso no parceiro:</strong> {a["reuse_days"]} dias. O intervalo é por estabelecimento, não por prato.</p>' if a['reuse_days'] else '<p>Confira o intervalo de reutilização na plataforma +UM.</p>'
 ptitle='Valor de referência do item' if a['price_cents'] else 'Valor do item'
 cardlist.append(f'''<article class="experience-card" id="{rid}" data-id="{e(a['id'])}" data-category="{a['category']}" data-search="{e(search,quote=True)}">
<div class="card-photo"><span class="photo-fallback" aria-hidden="true">+um</span><img src="{e(a['photo'],quote=True)}" alt="{e(a['name'])} · {e(a['partner'])}" width="640" height="480" loading="lazy" decoding="async"><span class="category-badge">{a['category_label']}</span></div>
<div class="card-body"><p class="partner-name">{e(a['partner'])}</p><h2>{e(a['name'])}</h2><p class="card-description">{e(a['description'])}</p><div class="card-price"><span>{ptitle}</span><strong>{e(a['price_label'])}</strong></div>
<details><summary>Ver benefício e regras <span aria-hidden="true">+</span></summary><div class="card-details"><p>{e(a['description'])}</p><h3>Quando usar</h3><ul>{rules}</ul>{reuse}<p>Uso sujeito ao limite diário e à disponibilidade do parceiro. As regras podem mudar.</p><h3>Onde fica</h3><p>{e(a['address'] or 'Consulte o endereço na plataforma +UM.')} · Vitória da Conquista</p><a href="{e(a['app_url'],quote=True)}" target="_blank" rel="noopener noreferrer" class="app-link">Conferir no app +UM {arrow}</a></div></details></div></article>''')
htmlfile=(ROOT/'experiencias/template.html').read_text().replace('<!-- EXPERIENCE_CARDS -->','\n'.join(cardlist))
(ROOT/'experiencias/index.html').write_text(htmlfile)
print(f'Rendered {len(items)} benefits from {public["partner_count"]} partners.')
