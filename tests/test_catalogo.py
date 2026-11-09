"""Static catalog contract. Runs without browser or third-party dependencies."""
import collections,html,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Elements(HTMLParser):
 def __init__(self,source):super().__init__();self.nodes=[];self.feed(source)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
class CatalogContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.page=(ROOT/'experiencias/index.html').read_text();cls.data=json.loads((ROOT/'experiencias/catalogo.json').read_text());cls.dom=Elements(cls.page)
 def test_catalog_identity_and_counts(self):
  items=self.data['items'];self.assertEqual(len(items),27);self.assertEqual(self.data['benefit_count'],27);self.assertEqual(len({x['partner'] for x in items}),20)
  self.assertEqual(collections.Counter(x['category'] for x in items),{'comida':27})
  ids=[x['id'] for x in items];self.assertEqual(len(set(ids)),27)
  for value in ids:self.assertRegex(value,r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
 def test_rendered_card_count_and_detail_anchors(self):
  cards=[a for t,a in self.dom.nodes if t=='article' and 'experience-card' in a.get('class','').split()];self.assertEqual(len(cards),27)
  self.assertEqual({a['data-id'] for a in cards},{x['id'] for x in self.data['items']})
  for a in cards:self.assertEqual(a['id'],'experiencia-'+a['data-id'])
  self.assertEqual(sum(t=='details' for t,a in self.dom.nodes),31)
 def test_zero_unknown_prices_not_free(self):
  unknown=0
  for item in self.data['items']:
   if not item['price_cents']:unknown+=1;self.assertEqual(item['price_label'],'Consulte o valor')
   else:self.assertGreater(item['price_cents'],0);self.assertTrue(item['price_label'].startswith('R$'))
  self.assertGreater(unknown,0);self.assertNotRegex(self.page,r'R\$\s*(?:&nbsp;)?0,00')
 def test_safe_verified_links_and_assets(self):
  checkouts=[a['href'] for t,a in self.dom.nodes if t=='a' and 'data-checkout' in a];self.assertGreaterEqual(len(checkouts),3)
  self.assertEqual(set(checkouts),{'https://pay.cakto.com.br/3e7t64x_1061003'})
  for t,a in self.dom.nodes:
   if 'src' in a and a['src'].startswith('/'):self.assertTrue((ROOT/a['src'][1:]).is_file(),a['src'])
   if t=='a' and a.get('target')=='_blank':self.assertIn('noopener',a.get('rel',''))
  for item in self.data['items']:
   self.assertEqual(item['app_url'],'https://app.appmaisum.com.br/share/dishes/'+item['id'])
   self.assertTrue(item['photo'].startswith('https://pjewtzlrqtomilpivjai.supabase.co/storage/v1/object/public/'))
 def test_truthful_offer_and_scope(self):
  text=html.unescape(re.sub('<[^>]+>',' ',self.page))
  for required in ['+50','experiências','27 benefícios','20','R$ 97','R$ 0,99','R$ 97,99','Renovação anual','09/11/2026','por estabelecimento, não por prato','todo o cardápio']:self.assertIn(required,text)
  self.assertNotIn('27 experiências',text)
  self.assertNotIn('data-filter="beleza"',self.page);self.assertNotIn('data-filter="pet"',self.page)
  self.assertIn('noindex,nofollow',self.page)
 def test_accessibility_and_nojs_structure(self):
  self.assertEqual(sum(t=='h1' for t,a in self.dom.nodes),1)
  ids=[a['id'] for t,a in self.dom.nodes if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for t,a in self.dom.nodes:
   if t=='img':self.assertTrue(a.get('alt'));self.assertIn('width',a);self.assertIn('height',a)
  form=next(a for t,a in self.dom.nodes if a.get('id')=='catalog-controls');self.assertIn('hidden',form)
  self.assertIn('aria-live="polite"',self.page)
  self.assertIn('photo-fallback',self.page)
if __name__=='__main__':unittest.main()
