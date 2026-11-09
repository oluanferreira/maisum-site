import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa-artifacts';OUT.mkdir(exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8124),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width,height in [(320,740),(390,844),(540,900),(768,1024),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8124/links/',wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert page.evaluate("document.fonts.check('600 30px Bricolage')"),'Font not loaded'
  assert not errors,errors
  assert page.locator('[data-link]').count()==7
  assert page.locator('[data-link="consumer"]').bounding_box()['height']>=60
  if width<=390:assert page.locator('[data-link="consumer"]').bounding_box()['y']<height,'Primary CTA below first screen'
  page.screenshot(path=str(OUT/f'central-{width}.png'),full_page=True)
  page.locator('.bottom-nav a[href="#ajuda"]').click();assert page.evaluate('location.hash')=='#ajuda'
  page.locator('.bottom-nav a[href="#parcerias"]').click();assert page.evaluate('location.hash')=='#parcerias'
  page.go_back();assert page.evaluate('location.hash')=='#ajuda'
  page.locator('.bottom-nav a[href="#explorar"]').click();assert page.evaluate('location.hash')=='#explorar'
  results.append({'width':width,'overflow':False,'font_loaded':True,'js_errors':errors,'anchor_back_navigation':True});page.close()
 page=browser.new_page(viewport={'width':390,'height':844})
 page.goto('http://127.0.0.1:8124/links/?affiliate=test_creator',wait_until='networkidle')
 page.locator('[data-link="consumer"]').click();page.wait_for_url('**/?affiliate=test_creator#experiencias')
 for a in page.locator('a[href*="pay.cakto.com.br"]').all():assert 'affiliate=test_creator' in a.get_attribute('href')
 page.go_back();page.reload();assert 'affiliate=test_creator' in page.locator('[data-link="consumer"]').get_attribute('href')
 page.goto('http://127.0.0.1:8124/links/');page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement');page.keyboard.press('Enter');assert page.evaluate('location.hash')=='#explorar'
 page.context.route('https://wa.me/**',lambda route:route.fulfill(status=200,content_type='text/html',body='<p>Intercepted for QA</p>'))
 for audience in ['influencer','support-user','support-partner']:
  with page.expect_popup() as info:page.locator(f'[data-link="{audience}"]').click()
  popup=info.value;popup.wait_for_load_state();assert popup.url.startswith('https://wa.me/5577999571376?text=');popup.close()
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});np=nojs.new_page();np.goto('http://127.0.0.1:8124/links/');assert np.locator('[data-link]').count()==7;np.locator('.bottom-nav a[href="#ajuda"]').click();assert np.url.endswith('#ajuda');np.screenshot(path=str(OUT/'central-nojs.png'),full_page=True)
 browser.close()
server.shutdown();(OUT/'results.json').write_text(json.dumps({'responsive':results,'affiliate_roundtrip':True,'whatsapp_intercepted':3,'no_js':True,'keyboard':True},indent=2));print('PASS: 5 viewports, no overflow/errors, font, anchors/back, affiliate checkout, no-JS, keyboard, WhatsApp destinations.')
