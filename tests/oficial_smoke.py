import functools,http.server,json,threading,os,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('OFICIAL_QA_DIR',str(ROOT/'qa-artifacts'/'oficial')));OUT.mkdir(parents=True,exist_ok=True)
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8132),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
assert hashlib.sha256((ROOT/'oficial/assets/leo-gastronomia-v2.png').read_bytes()).hexdigest()=='36e44a4a48a498cb1e4bf6da52aafd8fb2dd107c63639e7ffa07a5b014f71d08','approved Léo asset changed'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for width,height in [(320,740),(390,844),(540,900),(768,1024),(1024,768),(1440,1000)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8132/',wait_until='networkidle');page.evaluate('document.fonts.ready')
  # Save the actual layout and screenshot before assertions, including failures.
  layout=page.evaluate("""() => ({viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth,overflowing:[...document.querySelectorAll('body *')].map(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);let parent=e.parentElement,clippedBy=null;while(parent){const p=getComputedStyle(parent);if(['hidden','clip','scroll','auto'].includes(p.overflowX)){clippedBy=parent.tagName.toLowerCase()+'.'+parent.className;break}parent=parent.parentElement}return {tag:e.tagName.toLowerCase(),class:e.className,id:e.id,left:r.left,right:r.right,width:r.width,cssWidth:s.width,maxWidth:s.maxWidth,minWidth:s.minWidth,overflowX:s.overflowX,clippedBy,visible:r.width>0&&r.height>0}}).filter(e=>e.visible&&(e.right>innerWidth+.5||e.left<-.5)).slice(0,100)})""")
  (OUT/f'layout-{width}x{height}.json').write_text(json.dumps(layout,indent=2))
  page.screenshot(path=str(OUT/f'initial-{width}x{height}.png'),full_page=True)
  assert layout['documentWidth']<=width,(width,'overflow',layout)

  assert page.evaluate("document.fonts.check('650 30px DM')"),'font'
  assert not errors,errors
  assert page.locator('h1').count()==1
  assert 1<=page.locator('.hero-art img').count()<=3
  assert page.locator('.hero-food-extras').count()==1
  assert page.locator('.hero-food-extras img').count()==1
  assert page.locator('.hero-food-extras img').get_attribute('alt')==''
  assert page.locator('.hero-promo').count()==1
  assert page.locator('.hero-promo-top img').get_attribute('src')=='/links/assets/black-friday-3d.webp'
  assert page.locator('.hero-promo').evaluate('(el)=>getComputedStyle(el).backgroundColor==="rgb(25, 26, 24)"')
  assert page.locator('.step-card').count()==3
  assert page.locator('.step-visual img').count()==3
  assert page.locator('.step-company img').get_attribute('src')=='/oficial/assets/steps-companhia.webp'
  assert 'ilustrativo' in page.locator('.step-phone-scene').inner_text().lower()
  assert page.locator('.hero-composition').count()==1
  assert page.locator('.hero-art .food-float, .hero-art .portrait-frame').count()==0
  assert page.locator('.hero-composition').evaluate('(img)=>getComputedStyle(img).objectFit==="contain"')
  assert page.locator('.hero-composition').get_attribute('src')=='/oficial/assets/leo-gastronomia-v2.webp'
  assert page.locator('.hero-composition').evaluate('(img)=>(getComputedStyle(img).maskImage||getComputedStyle(img).webkitMaskImage)!=="none"'),'base fade missing'
  if width<=850:
   editorial=page.evaluate("""()=>{const title=document.querySelector('.hero h1'),art=document.querySelector('.hero-art'),desc=document.querySelector('.hero-description');const t=title.getBoundingClientRect(),a=art.getBoundingClientRect(),d=desc.getBoundingClientRect();return {titleLeft:t.left,titleRight:t.right,titleTop:t.top,titleBottom:t.bottom,titleWidth:title.clientWidth,titleScroll:title.scrollWidth,artLeft:a.left,artRight:a.right,artTop:a.top,artBottom:a.bottom,descriptionTop:d.top}}""")
   assert editorial['titleRight']<=editorial['artLeft']+1,('hero title/art collision',width,editorial)
   assert editorial['titleScroll']<=editorial['titleWidth']+1,('title text overflows its own column',width,editorial)
   assert max(editorial['titleTop'],editorial['artTop'])<min(editorial['titleBottom'],editorial['artBottom']),('not side by side',width,editorial)
   assert editorial['artBottom']<=editorial['descriptionTop'],('art collides with description',width,editorial)
  assert page.locator('.hero-facts').inner_text().find('+50 experiências')>=0
  assert page.locator('.black-friday-offer').count()==1
  offer=page.locator('.black-friday-offer').inner_text()
  assert 'BLACK FRIDAY' in offer and 'no primeiro ano' in offer and 'taxa incluída' in offer
  assert 'Renovação anual' in offer and 'Condições no checkout' in offer
  assert '97,99' not in page.locator('body').inner_text()
  assert page.locator('.hero-price').inner_text().find('R$ 47,99')>=0
  assert page.locator('[data-checkout]').evaluate_all("els=>els.every(a=>a.href==='https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum')")
  assert page.locator('img:not([loading="lazy"])').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)'), 'missing hero image'
  assert page.locator('[data-checkout]').evaluate_all('(links)=>links.filter(a=>a.getBoundingClientRect().height>0).every(a=>a.getBoundingClientRect().height>=44)'), 'checkout touch size'
  assert page.locator('.hero-actions>a,.text-link').evaluate_all('(links)=>links.every(a=>a.getBoundingClientRect().height>=44)'), 'secondary action touch size'
  for image in page.locator('img[loading=\"lazy\"]').all():
   image.scroll_into_view_if_needed(); image.evaluate('(img) => img.decode()')
  page.evaluate('window.scrollTo(0,0)')
  page.screenshot(path=str(OUT/f'home-{width}x{height}.png'),full_page=True)
  if width==390:page.screenshot(path=str(OUT/'home-mobile-first-screen.png'))
  if width==1440:page.screenshot(path=str(OUT/'home-desktop-first-screen.png'))
  if width in (390,1440):
   page.locator('.how-section').screenshot(path=str(OUT/f'how-{width}.png'))
   page.locator('.hero-promo').screenshot(path=str(OUT/f'hero-promo-{width}.png'))
   page.evaluate('window.scrollTo(0,0)')
  if width<=850:
   page.locator('.menu-toggle').click();assert page.locator('#mobile-nav').is_visible()
   page.keyboard.press('Escape');assert not page.locator('#mobile-nav').is_visible()
  page.locator('.faq-list details').first.locator('summary').click();assert page.locator('.faq-list details').first.get_attribute('open') is not None
  results.append({'width':width,'height':height,'no_overflow':True,'js_errors':errors,'font_loaded':True,'hero_images_loaded':True,'hero_title_left_art_right':True,'base_fade':True});page.close()
 page=browser.new_page(viewport={'width':390,'height':844})
 for query,expected in [('?affiliate=creator_test','creator_test'),('?affiliate=one&affiliate=two',None),('?affiliate=bad%20name',None),('',None)]:
  page.goto('http://127.0.0.1:8132/'+query,wait_until='networkidle')
  for link in page.locator('[data-checkout], [data-catalog]').all():
   href=link.get_attribute('href')
   assert (f'affiliate={expected}' in href) if expected else ('affiliate=' not in href),href
   if link.get_attribute('data-checkout') is not None:assert 'coupon=blackmaisum' in href,href
 # Intercept the purchase destination before any checkout request is sent.
 checkout_requests=[]
 def checkout_intercept(route):
  checkout_requests.append(route.request.url)
  route.fulfill(status=200,content_type='text/html',body='<title>QA checkout interception</title>')
 page.route('https://pay.cakto.com.br/**',checkout_intercept)
 page.goto('http://127.0.0.1:8132/?affiliate=creator_test',wait_until='networkidle')
 page.locator('.hero-actions [data-checkout]').click();page.wait_for_url('https://pay.cakto.com.br/**')
 assert checkout_requests==['https://pay.cakto.com.br/3e7t64x_1061003?coupon=blackmaisum&affiliate=creator_test'],checkout_requests
 page.goto('http://127.0.0.1:8132/',wait_until='networkidle');page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844});np=nojs.new_page();np.goto('http://127.0.0.1:8132/',wait_until='networkidle');assert np.locator('.hero-actions [data-checkout]').is_visible();assert np.locator('.experience-card').count()==4;np.screenshot(path=str(OUT/'home-nojs.png'),full_page=True)
 browser.close()
server.shutdown();(OUT/'results.json').write_text(json.dumps({'responsive':results,'affiliate_organic_valid_duplicate_invalid':True,'no_js_content':True,'keyboard':True,'faq':True,'mobile_menu':True,'checkout_intercepted_without_payment':True},indent=2));print('PASS: six sizes, fonts, images, no overflow/JS errors, affiliate cases, no-JS, keyboard, FAQ, mobile menu.')
