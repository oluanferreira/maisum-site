import functools,http.server,json,threading,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('OFICIAL_QA_DIR',str(ROOT/'qa-artifacts'/'oficial')));OUT.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8132),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width,height in [(320,740),(390,844),(540,900),(768,1024),(1024,768),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8132/',wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'overflow')
  assert page.evaluate("document.fonts.check('650 30px DM')"),'font'
  assert not errors,errors
  assert page.locator('h1').count()==1
  assert page.locator('.leo-portrait').count()==1
  assert page.locator('.hero-facts').inner_text().find('+50 experiências')>=0
  assert page.locator('[data-checkout]').evaluate_all("els=>els.every(a=>a.href==='https://pay.cakto.com.br/3e7t64x_1061003')")
  assert page.locator('img:not([loading="lazy"])').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)'), 'missing hero image'
  assert page.locator('[data-checkout]').evaluate_all('(links)=>links.filter(a=>a.getBoundingClientRect().height>0).every(a=>a.getBoundingClientRect().height>=44)'), 'checkout touch size'
  for image in page.locator('img[loading=\"lazy\"]').all():
   image.scroll_into_view_if_needed(); image.evaluate('(img) => img.decode()')
  page.evaluate('window.scrollTo(0,0)')
  page.screenshot(path=str(OUT/f'home-{width}x{height}.png'),full_page=True)
  if width==390:page.screenshot(path=str(OUT/'home-mobile-first-screen.png'))
  if width==1440:page.screenshot(path=str(OUT/'home-desktop-first-screen.png'))
  if width<=850:
   page.locator('.menu-toggle').click();assert page.locator('#mobile-nav').is_visible()
   page.keyboard.press('Escape');assert not page.locator('#mobile-nav').is_visible()
  page.locator('.faq-list details').first.locator('summary').click();assert page.locator('.faq-list details').first.get_attribute('open') is not None
  results.append({'width':width,'height':height,'no_overflow':True,'js_errors':errors,'font_loaded':True,'hero_images_loaded':True});page.close()
 page=browser.new_page(viewport={'width':390,'height':844})
 for query,expected in [('?affiliate=creator_test','creator_test'),('?affiliate=one&affiliate=two',None),('?affiliate=bad%20name',None),('',None)]:
  page.goto('http://127.0.0.1:8132/'+query,wait_until='networkidle')
  for link in page.locator('[data-checkout], [data-catalog]').all():
   href=link.get_attribute('href')
   assert (f'affiliate={expected}' in href) if expected else ('affiliate=' not in href),href
 page.goto('http://127.0.0.1:8132/',wait_until='networkidle');page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});np=nojs.new_page();np.goto('http://127.0.0.1:8132/',wait_until='networkidle');assert np.locator('.hero-actions [data-checkout]').is_visible();assert np.locator('.experience-card').count()==4;np.screenshot(path=str(OUT/'home-nojs.png'),full_page=True)
 browser.close()
server.shutdown();(OUT/'results.json').write_text(json.dumps({'responsive':results,'affiliate_organic_valid_duplicate_invalid':True,'no_js_content':True,'keyboard':True,'faq':True,'mobile_menu':True},indent=2));print('PASS: six sizes, fonts, images, no overflow/JS errors, affiliate cases, no-JS, keyboard, FAQ, mobile menu.')
