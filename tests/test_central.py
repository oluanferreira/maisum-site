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
  expected={'app':'https://app.appmaisum.com.br/login','consumer':'/experiencias','passport':'https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum','register':'https://restaurante.appmaisum.com.br/cadastro'}
  self.assertEqual(set(self.links),set(expected)|{'influencer','support-user','support-partner'})
  for key,url in expected.items():self.assertEqual(self.links[key]['href'],url)
 def test_black_friday_offer(self):
  self.assertIn('route passport black-friday',self.source)
  for copy in ['BLACK FRIDAY +UM','1 ano inteiro','R$ 47,99','no primeiro ano','black-friday-3d.webp']:self.assertIn(copy,self.source)
  self.assertNotIn('R$ 97',self.source)
  self.assertNotIn('hero-host',self.source)
  self.assertNotIn('Gastronomia em Conquista',self.source)
  self.assertNotIn('passport-terms',self.source)
 def test_account_block_removed(self):
  for removed in ['Já faço parte','ACESSE SUA CONTA','Minha conta +UM','Painel do parceiro','Sou assinante','Sou estabelecimento','https://restaurante.appmaisum.com.br/login']:
   self.assertNotIn(removed,self.source)
 def test_account_access_is_easy_to_find(self):
  self.assertEqual(self.source.count('Acessar minha conta'),1)
  self.assertIn('account-access',self.links['app']['class'])
  self.assertLess(self.source.index('Acessar minha conta'),self.source.index('<h1>'))
 def test_contact_number_caption_removed(self):
  self.assertNotIn('(77) 99957-1376',self.source)
  self.assertNotIn('Fale com o +UM.',self.source)
  self.assertNotIn('class="phone-number"',self.source)
 def test_distinct_whatsapp_messages(self):
  messages=[]
  for key,marker in [('influencer','influenciador'),('support-user','cliente'),('support-partner','lojista')]:
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
  for title in ['Explorar<br>experiências','Cadastrar meu<br>estabelecimento','Parceria para<br>influenciadores','Como podemos ajudar?']:self.assertIn(title,self.source)
  self.assertIn('lang="pt-BR"',self.source);self.assertIn('name="viewport"',self.source)
 def test_copy_uses_brand_promise_and_customer_language(self):
  from urllib.parse import unquote
  self.assertIn('<h1>Escolha um.<br>Ganhe <em>+um.</em></h1>',self.source)
  self.assertIn('Sou cliente',self.source)
  self.assertNotIn('usuário',unquote(self.source).lower())
  self.assertNotIn('usuaria',unquote(self.source).lower())
  self.assertNotIn('O que você',self.source)
 def test_legacy_sales_files_unchanged(self):
  expected={'styles.css': '8d343d3d4ec53e22192dac92403dff2d3218ed368a22d902968a5fbde9be64a5', 'script.js': '2e52f57efc7daa958047142134f1a6e656f44415cb1e15db3cd3c3a1e1f63051', 'oferta/index.html': '5746b863cc85a8d405c833a2348d07e08a72283c964334fbb6b34c8b4dd5e816'}
  for path,digest in expected.items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest,path)
if __name__=='__main__':unittest.main()
