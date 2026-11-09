"""Real browser QA. Checkout is always intercepted; no payment request is sent."""
import functools,http.server,json,threading,unicodedata
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'qa-artifacts/catalogo';OUT.mkdir(parents=True,exist_ok=True)
DATA=json.loads((ROOT/'experiencias/catalogo.json').read_text())
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8133),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();BASE='http://127.0.0.1:8133/experiencias/'
results=[];broken=[]
def visible_count(page):return page.locator('.experience-card:not([hidden])').count()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 context=browser.new_context(reduced_motion='reduce')
 for width,height in [(320,740),(390,844),(768,1024),(1440,1000)]:
  page=context.new_page();page.set_viewport_size({'width':width,'height':height});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE,wait_until='networkidle');page.evaluate('document.fonts.ready')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,'overflow')
  assert page.evaluate("document.fonts.check('650 30px DM')"),'font'
  assert visible_count(page)==27
  assert page.locator('.catalog-stats > strong').inner_text()=='+50'
  assert page.locator('.updated').count()==0
  assert 'parceiros gastronômicos' not in page.locator('.catalog-hero').inner_text()
  if width<=390:
   assert page.locator('#catalog-search').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')>=16
   assert page.locator('.experience-card').first.bounding_box()['y']<height-90, 'Discovery too far below the fold'
   assert page.locator('.header-buy').bounding_box()['height']>=44
  assert page.locator('#catalog-controls').is_visible()
  assert page.locator('.experience-card:not([data-category="comida"])').count()==0
  assert page.locator('[data-filter="beleza"], [data-filter="pet"]').count()==0
  assert page.locator('#results-count').inner_text().startswith('27 ')
  # All visible images must either decode or show the explicit fallback, never an unhandled broken asset.
  for img in page.locator('.card-photo img').all():
   img.scroll_into_view_if_needed()
   img.evaluate('(img)=>img.decode().catch(()=>null)')
  images=page.locator('.card-photo img').evaluate_all('(imgs)=>imgs.map(i=>({src:i.currentSrc||i.src,loaded:i.complete&&i.naturalWidth>0,fallback:i.closest(".experience-card").classList.contains("image-error")}))')
  assert all(i['loaded'] or i['fallback'] for i in images),images
  broken.extend(i['src'] for i in images if not i['loaded'])
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(OUT/f'catalogo-{width}x{height}.jpg'),full_page=True,quality=88)
  if width==390:page.screenshot(path=str(OUT/'catalogo-mobile-first-screen.png'))
  assert not errors,errors
  results.append({'width':width,'height':height,'no_overflow':True,'js_errors':errors,'images_loaded':sum(i['loaded'] for i in images),'fallback_images':sum(i['fallback'] for i in images),'gastronomy_only':True});page.close()
 page=context.new_page();page.set_viewport_size({'width':390,'height':844});page.goto(BASE,wait_until='networkidle')
 search=page.locator('#catalog-search');search.fill('acai');accent_count=visible_count(page);assert accent_count>0
 search.fill('açaí');assert visible_count(page)==accent_count
 search.fill('TATI');assert visible_count(page)==1
 search.fill('zzzz-sem-resultado-qa');assert visible_count(page)==0;assert page.locator('#empty-state').is_visible()
 page.locator('#empty-reset').click();assert visible_count(page)==27;assert search.input_value()==''
 search.fill('tati');page.locator('#reset-filters').click();assert visible_count(page)==27
 # Supported query state restores search/category without another click.
 page.goto(BASE+'?busca=acai',wait_until='networkidle');assert visible_count(page)==accent_count
 selected=next(x['id'] for x in DATA['items'] if x['name']=='Tati Burguer');anchor='#experiencia-'+selected
 page.goto(BASE+'?experiencia='+selected+anchor,wait_until='networkidle')
 expect(page.locator(anchor+' details')).to_have_attribute('open','');assert page.locator(anchor).evaluate('e=>e.classList.contains("highlighted")')
 page.screenshot(path=str(OUT/'catalogo-deep-link.png'))
 for query,expected in [('',None),('?affiliate=creator_test','creator_test'),('?affiliate=a&affiliate=b',None),('?affiliate=bad%20name',None),('?affiliate=valid_42&utm_source=qa&secret=do-not-forward','valid_42')]:
  page.goto(BASE+query,wait_until='networkidle')
  for href in page.locator('[data-checkout]').evaluate_all('(els)=>els.map(a=>a.href)'):
   u=urlparse(href);assert u.scheme=='https' and u.netloc=='pay.cakto.com.br' and u.path=='/3e7t64x_1061003'
   assert parse_qs(u.query)==({'coupon':['blackmaisum'],'affiliate':[expected]} if expected else {'coupon':['blackmaisum']}),href
  for href in page.locator('a.app-link').evaluate_all('(els)=>els.map(a=>a.href)'):assert 'affiliate=' not in href
 # Intercept and verify the exact destination before a request can reach the payment provider.
 intercepted=[]
 def checkout(route):
  intercepted.append(route.request.url);route.fulfill(status=200,content_type='text/html',body='<h1>Checkout intercepted for QA. No purchase.</h1>')
 page.route('https://pay.cakto.com.br/**',checkout)
 page.locator('.offer-card [data-checkout]').click();page.wait_for_url('https://pay.cakto.com.br/**')
 assert intercepted==['https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum&affiliate=valid_42'],intercepted
 # Simulated image outage must reveal the branded fallback and leave the card usable.
 fallback=context.new_page();fallback.route('https://pjewtzlrqtomilpivjai.supabase.co/storage/**',lambda route:route.abort())
 fallback.goto(BASE,wait_until='networkidle');first=fallback.locator('.experience-card').first;first.scroll_into_view_if_needed()
 expect(first).to_have_class(__import__('re').compile(r'.*image-error.*'));assert first.locator('.photo-fallback').is_visible()
 first.locator('summary').click();assert first.locator('details').get_attribute('open') is not None
 fallback.screenshot(path=str(OUT/'catalogo-image-fallback.png'));fallback.close()
 # Native details and complete content remain usable without JavaScript.
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
 np=nojs.new_page();np.goto(BASE,wait_until='networkidle');assert np.locator('.experience-card').count()==27;assert not np.locator('#catalog-controls').is_visible()
 np.locator('.experience-card').first.locator('summary').click();assert np.locator('.experience-card').first.locator('details').get_attribute('open') is not None
 assert np.locator('[data-checkout]').first.get_attribute('href')=='https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum'
 np.screenshot(path=str(OUT/'catalogo-nojs.png'))
 browser.close()
server.shutdown();(OUT/'results.json').write_text(json.dumps({'responsive':results,'accent_search':True,'empty_reset':True,'query_state':True,'deep_link':True,'affiliate_exact_checkout':True,'checkout_intercepted_no_purchase':True,'simulated_image_fallback':True,'no_js':True,'image_urls_using_fallback':sorted(set(broken))},indent=2))
print('PASS: catalog responsive, 27 gastronomy benefits, accent/empty/reset search, deep link, attribution, intercepted checkout, images/fallback and no-JS.')
