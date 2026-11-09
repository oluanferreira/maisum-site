"""Static regressions; run with python -m unittest discover -s tests -v."""
import unittest
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs
ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.links = []; self.ids = []; self.assets = []; self.scripts = []; self.meta = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a': self.links.append(attrs)
        if tag == 'script' and 'src' in attrs: self.scripts.append(attrs['src']); self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') in ('stylesheet', 'icon'): self.assets.append(attrs['href'])
        if tag == 'meta': self.meta.append(attrs)
class CentralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hub_text = (ROOT/'links/index.html').read_text()
        cls.home_text = (ROOT/'index.html').read_text()
        cls.hub = Document(cls.hub_text); cls.home = Document(cls.home_text)
        cls.links = {a['data-link']: a for a in cls.hub.links if 'data-link' in a}
    def test_expected_audiences_and_routes(self):
        self.assertEqual(set(self.links), {'consumer','app','register','partner-login','influencer','support-user','support-partner'})
        for name, url in {'consumer':'/', 'app':'https://app.appmaisum.com.br', 'register':'https://restaurante.appmaisum.com.br/cadastro', 'partner-login':'https://restaurante.appmaisum.com.br/login'}.items():
            self.assertEqual(self.links[name]['href'], url)
    def test_whatsapp_number_messages_and_external_safety(self):
        messages=[]
        for name, marker in [('influencer','influenciador'),('support-user','usuário'),('support-partner','lojista')]:
            link = self.links[name]; url=urlparse(link['href']); messages.append(parse_qs(url.query)['text'][0])
            self.assertEqual(url.netloc,'wa.me');self.assertEqual(url.path,'/5577999571376')
            self.assertIn(marker,messages[-1]); self.assertEqual(link['target'],'_blank')
            self.assertTrue({'noopener','noreferrer'} <= set(link['rel'].split()))
        self.assertEqual(len(set(messages)),3)
        self.assertIn('comissão',messages[0]);self.assertIn('link de divulgação',messages[0])
    def test_no_unsupported_commercial_promises(self):
        self.assertIn('Cadastro sujeito à aprovação.',self.hub_text)
        self.assertIn('Condições e comissão combinadas antes da divulgação.',self.hub_text)
        self.assertNotRegex(re.sub(r'<[^>]+>', '', self.hub_text),r'\d+%')
        self.assertNotIn('Quero fazer parte',self.home_text)
    def test_home_routes_and_checkout_unchanged(self):
        links=[a['href'] for a in self.home.links]
        self.assertIn('/links',links);self.assertIn('/links#ajuda',links)
        self.assertIn('https://restaurante.appmaisum.com.br/cadastro',links)
        self.assertIn('https://restaurante.appmaisum.com.br/login',links)
        checkout=[a for a in links if 'pay.cakto.com.br' in a]
        self.assertEqual(len(checkout),3)
        self.assertEqual(set(checkout),{'https://pay.cakto.com.br/3e7t64x_1061003'})
    def test_assets_ids_fragments_and_seo(self):
        for doc in [self.home,self.hub]:
            self.assertEqual(len(doc.ids),len(set(doc.ids)))
            for asset in doc.assets: self.assertTrue((ROOT/asset.lstrip('/')).is_file(),asset)
            for link in doc.links:
                href=link['href']
                if href.startswith('#'): self.assertIn(href[1:],doc.ids)
                if href.startswith('/links#'): self.assertIn(href.split('#')[1],self.hub.ids)
            self.assertEqual(doc.scripts.count('/affiliate.js'),1)
        self.assertIn('https://appmaisum.com.br/links',(ROOT/'sitemap.xml').read_text())
        ET.parse(ROOT/'sitemap.xml')
        self.assertIn('name="viewport"',self.hub_text)
if __name__=='__main__': unittest.main()
