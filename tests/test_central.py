import hashlib
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.assets=[];self.ids=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.links.append(a)
  if tag=='script' and 'src' in a:self.assets.append(a['src'])
  if tag=='img':self.assets.append(a['src'])
  if tag=='link' and a.get('rel') in ('stylesheet','icon','preload'):self.assets.append(a['href'])
class CentralTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=(ROOT/'links/index.html').read_text();cls.doc=Document(cls.source)
  cls.links={a['data-link']:a for a in cls.doc.links if 'data-link' in a}
 def test_all_audiences_and_verified_destinations(self):
  expected={'consumer':'/#experiencias','app':'https://app.appmaisum.com.br','register':'https://restaurante.appmaisum.com.br/cadastro','partner-login':'https://restaurante.appmaisum.com.br/login'}
  self.assertEqual(set(self.links),set(expected)|{'influencer','support-user','support-partner'})
  for key,url in expected.items():self.assertEqual(self.links[key]['href'],url)
 def test_distinct_whatsapp_messages(self):
  messages=[]
  for key,marker in [('influencer','influenciador'),('support-user','usuário'),('support-partner','lojista')]:
   a=self.links[key];url=urlparse(a['href']);message=parse_qs(url.query)['text'][0]
   self.assertEqual(url.netloc,'wa.me');self.assertEqual(url.path,'/5577999571376');self.assertIn(marker,message)
   self.assertTrue({'noopener','noreferrer'} <= set(a['rel'].split()));self.assertEqual(a['target'],'_blank');messages.append(message)
  self.assertEqual(len(set(messages)),3);self.assertIn('comissão',messages[0]);self.assertIn('link de divulgação',messages[0])
 def test_assets_and_local_navigation_exist(self):
  self.assertEqual(len(self.doc.ids),len(set(self.doc.ids)))
  for asset in self.doc.assets:self.assertTrue((ROOT/asset.lstrip('/')).is_file(),asset)
  for a in self.doc.links:
   if a['href'].startswith('#'):self.assertIn(a['href'][1:],self.doc.ids)
 def test_content_is_truthful_and_semantic(self):
  self.assertIn('Cadastro sujeito à aprovação.',self.source);self.assertIn('condições combinadas antes da divulgação.',self.source)
  self.assertNotRegex(re.sub(r'<[^>]+>','',self.source),r'\d+%')
  self.assertEqual(self.source.count('<h1>'),1)
  self.assertIn('lang="pt-BR"',self.source);self.assertIn('name="viewport"',self.source)
 def test_homepage_and_sales_files_unchanged(self):
  expected={'index.html': 'c7034102f1658cbb569cec70dbbd6096ce75f0144d88aacd4ef25e8a8f333010', 'styles.css': '8d343d3d4ec53e22192dac92403dff2d3218ed368a22d902968a5fbde9be64a5', 'script.js': '2e52f57efc7daa958047142134f1a6e656f44415cb1e15db3cd3c3a1e1f63051', 'oferta/index.html': '5746b863cc85a8d405c833a2348d07e08a72283c964334fbb6b34c8b4dd5e816'}
  for path,digest in expected.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest,path)
if __name__=='__main__':unittest.main()
