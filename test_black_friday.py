"""Campaign contract across the complete purchase journey, without network access."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self, source): super().__init__(); self.hrefs=[]; self.feed(source)
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if tag=='a' and 'href' in a: self.hrefs.append(a['href'])
class BlackFridayContract(unittest.TestCase):
 def test_exact_checkout_coupon_on_all_three_pages(self):
  for file in ['index.html','links/index.html','experiencias/index.html']:
   with self.subTest(file=file):
    urls=[urlsplit(h) for h in Links((ROOT/file).read_text()).hrefs if 'pay.cakto.com.br' in h]
    self.assertTrue(urls)
    for u in urls:
     self.assertEqual((u.scheme,u.netloc,u.path),('https','pay.cakto.com.br','/3e7t64x_1061003'))
     self.assertEqual(parse_qs(u.query),{'coupon':['blackmaisum']})
 def test_single_introductory_price_and_no_fabricated_deadline(self):
  for file in ['index.html','links/index.html','experiencias/template.html']:
   with self.subTest(file=file):
    source=(ROOT/file).read_text(); text=re.sub(r'<[^>]+>',' ',source)
    for required in ['Black Friday','primeiro ano','Renovação anual','checkout']:
     self.assertIn(required.lower(),text.lower())
    self.assertRegex(text,r'47\s*,99')
    for stale in ['R$ 97','R$ 0,99','97,99']: self.assertNotIn(stale,text)
    self.assertNotRegex(text.lower(),r'últimas vagas|só hoje|somente hoje|acaba em|até meia-noite')
 def test_annual_benefits_message(self):
  for file in ['index.html','links/index.html','experiencias/template.html']:
   text=re.sub(r'<[^>]+>',' ',(ROOT/file).read_text()).lower()
   self.assertIn('1 ano inteiro',text,file)
if __name__=='__main__': unittest.main()
