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
 for width,height in [(320,740),(390,844),(390,400),(540,900),(768,1024),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8124/links/',wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert page.evaluate("document.fonts.check('650 30px DM')"),'Font not loaded'
  assert not errors,errors
  assert page.evaluate("async()=>{const i=new Image();i.src='/links/assets/brand-3d.png';await i.decode();return i.naturalWidth>0}"), '3D artwork not loaded'
  assert page.locator('[data-link]').count()==6
  assert page.locator('.hero-host, .passport-terms').count()==0
  assert page.locator('.black-friday-art').count()==1
  assert page.locator('.black-friday-art').evaluate('(img)=>img.complete && img.naturalWidth>0'), 'Black Friday artwork missing'
  assert page.locator('.accounts').count()==0
  assert page.locator('.passport.black-friday').count()==1
  assert page.locator('[data-link="passport"]').get_attribute('href')=='https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum'
  assert 'R$ 47,99' in page.locator('.passport').inner_text()
  assert 'no primeiro ano' in page.locator('.passport').inner_text()
  assert page.locator('[data-link="app"], [data-link="partner-login"]').count()==0
  assert page.locator('[data-link="consumer"]').bounding_box()['height']>=60
  if width<=390 and height>=700:
   assert page.locator('[data-link="passport"] .route-action').bounding_box()['y']+page.locator('[data-link="passport"] .route-action').bounding_box()['height']<height,'Purchase action below first screen'
  assert page.locator('[data-link]').evaluate_all('(links)=>links.every(a=>a.getBoundingClientRect().height>=44)'), 'Touch target too small'
  assert page.locator('img').evaluate_all('(images)=>images.filter(i=>i.loading!=="lazy").every(i=>i.complete && i.naturalWidth>0)'), 'Missing eager image'
  page.locator('[data-link="consumer"]').scroll_into_view_if_needed();page.locator('.discovery-art').evaluate('(i)=>i.decode()');page.evaluate('scrollTo(0,0)')
  page.screenshot(path=str(OUT/f'central-{width}x{height}.png'),full_page=True)
  if width==390 and height==844:page.screenshot(path=str(OUT/'central-mobile-first-screen.png'))
  results.append({'width':width,'height':height,'overflow':False,'font_loaded':True,'js_errors':errors,'image_assets_loaded':True});page.close()
 page=browser.new_page(viewport={'width':390,'height':844})
 page.goto('http://127.0.0.1:8124/links/?affiliate=test_creator',wait_until='networkidle')
 page.locator('[data-link="consumer"]').click();page.wait_for_url('**/experiencias/?affiliate=test_creator')
 for a in page.locator('a[href*="pay.cakto.com.br"]').all():assert 'affiliate=test_creator' in a.get_attribute('href')
 page.go_back();page.reload();assert 'affiliate=test_creator' in page.locator('[data-link="consumer"]').get_attribute('href')
 page.goto('http://127.0.0.1:8124/links/');page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement');page.keyboard.press('Enter');assert page.evaluate('location.hash')=='#links'
 page.context.route('https://wa.me/**',lambda route:route.fulfill(status=200,content_type='text/html',body='<p>Intercepted for QA</p>'))
 for audience in ['influencer','support-user','support-partner']:
  with page.expect_popup() as info:page.locator(f'[data-link="{audience}"]').click()
  popup=info.value;popup.wait_for_load_state();assert popup.url.startswith('https://wa.me/5577999571376?text=');popup.close()
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});np=nojs.new_page();np.goto('http://127.0.0.1:8124/links/');assert np.locator('[data-link]').count()==6;np.screenshot(path=str(OUT/'central-nojs.png'),full_page=True)
 browser.close()
server.shutdown();(OUT/'results.json').write_text(json.dumps({'responsive':results,'affiliate_roundtrip':True,'whatsapp_intercepted':3,'no_js':True,'keyboard':True},indent=2));print('PASS: 6 viewports, no overflow/errors, font, affiliate checkout, no-JS, keyboard, WhatsApp destinations.')
