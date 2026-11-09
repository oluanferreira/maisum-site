const {test}=require('node:test');const assert=require('node:assert/strict');const vm=require('node:vm');const fs=require('node:fs');const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../links/central.js'),'utf8');
const original=['https://appmaisum.com.br/','https://appmaisum.com.br/#experiencias','https://appmaisum.com.br/links#ajuda','https://app.appmaisum.com.br','https://restaurante.appmaisum.com.br/cadastro','https://wa.me/5577999571376?text=teste'];
function run(query){const links=original.map(href=>({href}));vm.runInNewContext(source,{URL,URLSearchParams,location:new URL('https://appmaisum.com.br/links'+query),window:{},document:{querySelectorAll:()=>links}});return links.map(a=>a.href);}
test('organic remains unattributed',()=>assert.deepEqual(run(''),original));
test('explicit affiliate only follows official home and retains section',()=>{const out=run('?affiliate=creator_123-Test');out.forEach((h,i)=>i<2?assert.equal(new URL(h).searchParams.get('affiliate'),'creator_123-Test'):assert.equal(h,original[i]));assert.equal(new URL(out[1]).hash,'#experiencias');});
for(const query of ['?affiliate=','?affiliate=a&affiliate=b','?affiliate=a&affiliate=a','?affiliate=%3Cscript%3E','?affiliate=a%26b','?affiliate='+'a'.repeat(129)])test('rejects invalid or duplicate '+query.slice(0,50),()=>assert.deepEqual(run(query),original));
test('does not copy unrelated or personal parameters',()=>assert.equal(new URL(run('?affiliate=abc&email=private&utm_source=ig')[0]).search,'?affiliate=abc'));
