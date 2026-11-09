const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = readFileSync(path.join(__dirname, '../affiliate.js'), 'utf8');
const original = ['https://appmaisum.com.br/','https://appmaisum.com.br/links#ajuda','https://appmaisum.com.br/links/','https://pay.cakto.com.br/3e7t64x_1061003','https://pay.cakto.com.br/other','https://restaurante.appmaisum.com.br/cadastro','https://app.appmaisum.com.br','https://wa.me/5577999571376?text=teste','https://www.instagram.com/maisum.vca/'];
function run(query) {
  const location = new URL('https://appmaisum.com.br/links' + query);
  const links = original.map(href => ({href}));
  vm.runInNewContext(source, {URL, URLSearchParams, window: {location}, document: {querySelectorAll: () => links}});
  return links.map(a=>a.href);
}
test('organic visits never get an affiliate', ()=>assert.deepEqual(run(''),original));
test('valid explicit affiliate follows central → home → checkout, never other audiences', ()=>{
  const output=run('?affiliate=creator_123-Test');
  output.forEach((href,index)=>{
    if(index<4)assert.equal(new URL(href).searchParams.get('affiliate'),'creator_123-Test');
    else assert.equal(href,original[index]);
  });
  assert.equal(new URL(output[1]).hash,'#ajuda');
});
for (const query of ['?affiliate=', '?affiliate=one&affiliate=two', '?affiliate=a&affiliate=a', '?affiliate=%3Cscript%3E', '?affiliate=a%26b', '?affiliate='+ 'a'.repeat(129)]) {
  test('rejects invalid/ambiguous affiliate ' + query.slice(0,50), ()=>assert.deepEqual(run(query),original));
}
test('no unrelated query gets copied',()=>{const href=run('?affiliate=abc&utm_source=ig&email=private')[0];assert.equal(new URL(href).search,'?affiliate=abc');});
