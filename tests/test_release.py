"""Production entry pages, navigation and metadata contract."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = ['index.html', 'links/index.html', 'experiencias/index.html']

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

class ReleaseContract(unittest.TestCase):
    def test_public_metadata(self):
        for path in PAGES:
            text = (ROOT / path).read_text()
            self.assertIn('content="index,follow"', text, path)
            self.assertNotIn('noindex', text, path)
            self.assertNotIn('Prévia de criação', text, path)
            self.assertNotIn('sujeita à aprovação visual', text, path)
        urls = {n.text for n in ET.parse(ROOT / 'sitemap.xml').iter()
                if n.tag.endswith('}loc')}
        for route in ['', 'links', 'experiencias']:
            self.assertIn('https://appmaisum.com.br/' + route, urls)

    def test_local_links_assets_and_anchors(self):
        for path in PAGES:
            source = ROOT / path
            for tag, attrs in Document(source.read_text()).nodes:
                for key in ('href', 'src'):
                    if key not in attrs:
                        continue
                    url = urlsplit(attrs[key])
                    if url.scheme or url.netloc:
                        continue
                    if not url.path:
                        target = source
                    else:
                        value = unquote(url.path)
                        target = ROOT / value.lstrip('/') if value.startswith('/') else source.parent / value
                        if target.is_dir():
                            target = target / 'index.html'
                        elif not target.is_file() and not target.suffix:
                            target = target.with_suffix('.html')
                    self.assertTrue(target.is_file(), (path, attrs[key]))
                    if url.fragment and target.suffix == '.html':
                        ids = {a.get('id') for _, a in Document(target.read_text()).nodes}
                        self.assertIn(unquote(url.fragment), ids, (path, attrs[key]))

    def test_purchase_entry_and_separate_accounts(self):
        count = 0
        for path in PAGES:
            for tag, attrs in Document((ROOT / path).read_text()).nodes:
                if tag == 'a' and ('data-checkout' in attrs or '/checkout/black-friday' in attrs.get('href', '')):
                    count += 1
                    self.assertEqual(attrs['href'], 'https://app.appmaisum.com.br/checkout/black-friday')
        self.assertEqual(count, 9)
        text = (ROOT / 'index.html').read_text()
        self.assertIn('href="https://app.appmaisum.com.br/login"', text)
        self.assertIn('href="https://restaurante.appmaisum.com.br/login"', text)

if __name__ == '__main__':
    unittest.main()
