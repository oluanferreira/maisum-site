import json, threading, functools, http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'qa-artifacts'; OUT.mkdir(exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8124),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(320,720),(390,844),(768,1024),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  for route,name in [('/links/','links'),('/','home')]:
   page.goto('http://127.0.0.1:8124'+route,wait_until='networkidle')
   page.screenshot(path=str(OUT/f'{name}-{width}.png'),full_page=True)
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),f'Overflow {name} {width}'
   assert not errors,errors
   results.append({'page':name,'width':width,'overflow':False,'js_errors':errors.copy()})
  if width==390:
   button=page.locator('.menu-button');button.click();assert button.get_attribute('aria-expanded')=='true'
   button.click();assert button.get_attribute('aria-expanded')=='false'
   button.click();page.locator('.mobile-menu a[href="/links#ajuda"]').click();page.wait_for_url('**/links/#ajuda')
   assert page.locator('#ajuda').is_visible()
   page.go_back();button=page.locator('.menu-button');button.click();assert button.get_attribute('aria-expanded')=='true'
  page.close()
 page=browser.new_page(viewport={'width':390,'height':844})
 page.goto('http://127.0.0.1:8124/links/?affiliate=test_creator',wait_until='networkidle')
 assert 'affiliate=test_creator' in page.locator('[data-link="consumer"]').get_attribute('href')
 page.locator('[data-link="consumer"]').click();page.wait_for_url('**/?affiliate=test_creator')
 for a in page.locator('a[href*="pay.cakto.com.br"]').all(): assert 'affiliate=test_creator' in a.get_attribute('href')
 page.go_back();assert page.locator('[data-link="influencer"]').get_attribute('href').startswith('https://wa.me/')
 page.reload();assert 'affiliate=test_creator' in page.locator('[data-link="consumer"]').get_attribute('href')
 page.goto('http://127.0.0.1:8124/links/',wait_until='networkidle');page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Enter');assert page.evaluate('location.hash')=='#caminhos'
 # Validate real click destinations without contacting WhatsApp or sending a message.
 for audience in ['influencer','support-user','support-partner']:
  with page.expect_popup() as popup_info:
   page.context.route('https://wa.me/**',lambda route:route.fulfill(status=200,content_type='text/html',body='<p>Destination intercepted for QA</p>'))
   page.locator(f'[data-link="{audience}"]').click()
  popup=popup_info.value;popup.wait_for_load_state();assert popup.url.startswith('https://wa.me/5577999571376?text=');popup.close()
 # All routes remain functional without JavaScript.
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});np=nojs.new_page();np.goto('http://127.0.0.1:8124/links/');assert np.locator('[data-link]').count()==7;np.screenshot(path=str(OUT/'links-nojs.png'),full_page=True)
 browser.close()
server.shutdown()
(OUT/'browser-results.json').write_text(json.dumps({'responsive':results,'affiliate_roundtrip':True,'back_reload':True,'keyboard_skip':True,'whatsapp_clicks_intercepted':3,'nojs_links':7},indent=2))
print('PASS: responsive, local click flows, no-JS, keyboard, attribution, reload/back. Screenshots:',OUT)
