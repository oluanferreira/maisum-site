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
 def test_exact_app_purchase_entry_on_all_three_pages(self):
  for file,expected_count in [('index.html',5),('links/index.html',1),('experiencias/index.html',3),('experiencias/template.html',3)]:
   with self.subTest(file=file):
    hrefs=Links((ROOT/file).read_text()).hrefs
    self.assertFalse(any('pay.cakto.com.br' in href for href in hrefs))
    urls=[urlsplit(h) for h in hrefs if '/checkout/black-friday' in h]
    self.assertEqual(len(urls),expected_count)
    for u in urls:
     self.assertEqual((u.scheme,u.netloc,u.path),('https','app.appmaisum.com.br','/checkout/black-friday'))
     self.assertEqual(parse_qs(u.query),{})
 def test_single_introductory_price_and_no_fabricated_deadline(self):
  for file in ['index.html','links/index.html','experiencias/template.html']:
   with self.subTest(file=file):
    source=(ROOT/file).read_text(); text=re.sub(r'<[^>]+>',' ',source)
    required=['Black Friday','primeiro ano']
    if file!='links/index.html':required+=['Renovação anual','checkout']
    for copy in required:self.assertIn(copy.lower(),text.lower())
    self.assertRegex(text,r'47\s*,99')
    for stale in ['R$ 97','R$ 0,99','97,99']: self.assertNotIn(stale,text)
    self.assertNotRegex(text.lower(),r'últimas vagas|vagas limitadas|tempo limitado|só hoje|somente hoje|acaba em|até meia-noite')
 def test_annual_benefits_message(self):
  for file in ['index.html','links/index.html','experiencias/template.html']:
   text=re.sub(r'<[^>]+>',' ',(ROOT/file).read_text()).lower()
   self.assertIn('1 ano inteiro',text,file)
if __name__=='__main__': unittest.main()
