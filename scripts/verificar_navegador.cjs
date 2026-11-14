// Teste opcional de interface e gravação local. Requer playwright e Chromium.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const build=process.env.SEMINARIO_BUILD || path.join(root,'.build');
const wait=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const durations=JSON.parse(fs.readFileSync(path.join(build,'audio_durations.json'),'utf8'));
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext({viewport:{width:1280,height:720},recordVideo:{dir:path.join(build,'video'),size:{width:1280,height:720}}});
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  const video=page.video();
  await page.goto('http://127.0.0.1:8501');
  await page.waitForSelector('#f-Amount');
  async function scene(index,action){
    const start=Date.now();await action();
    console.log('Cena '+(index+1)+' / 6');
    await wait(Math.max(100,durations[index]*1000-(Date.now()-start)));
  }
  await scene(0,async()=>{});
  await scene(1,async()=>{
    await page.locator('#predict').click();await page.waitForSelector('#result .score');
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('.workspace').getBoundingClientRect().top+scrollY-15));
  });
  await scene(2,async()=>{
    await page.locator('#preset').selectOption('3');await page.locator('#predict').click();
    await page.waitForFunction(()=>document.querySelector('#result').innerText.includes('revisão'));
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('.workspace').getBoundingClientRect().top+scrollY-15));
  });
  await scene(3,async()=>{
    await page.locator('#preset').selectOption('6');await page.locator('#predict').click();
    await page.waitForFunction(()=>document.querySelector('#result').innerText.includes('Sem alerta'));
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('.workspace').getBoundingClientRect().top+scrollY-15));
    await wait(durations[3]*500);
    await page.locator('#preset').selectOption('8');await page.locator('#predict').click();
    await page.waitForFunction(()=>document.querySelector('#result').innerText.includes('revisão'));
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('.workspace').getBoundingClientRect().top+scrollY-15));
  });
  await scene(4,async()=>{
    await page.locator('[data-tab=evidencias]').click();
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('#evidencias').getBoundingClientRect().top+scrollY-15));
    await wait(durations[4]*500);
    await page.locator('#test-metrics').scrollIntoViewIfNeeded();
  });
  await scene(5,async()=>{
    await page.locator('[data-tab=limites]').click();
    await page.evaluate(()=>window.scrollTo(0,document.querySelector('#limites').getBoundingClientRect().top+scrollY-15));
    await wait(durations[5]*700);
    const qr=fs.readFileSync(path.join(root,'entrega_final/divulgacao/qr_projeto.png')).toString('base64');
    await page.setContent('<html lang="pt-BR"><body style="margin:0;background:#f5f2eb;color:#183441;font-family:Arial;padding:100px 90px;display:flex;gap:70px;align-items:center"><div><p style="font-size:15px;letter-spacing:2px;color:#145a73">FIB · INTELIGÊNCIA ARTIFICIAL II · GRUPO 3</p><h1 style="font-size:54px">Caçador de Fraudes</h1><p style="font-size:25px;line-height:1.5">Código, experimentos e instruções para executar a aplicação.</p><p style="font-size:19px">github.com/lipeinacio/random_forest</p><p style="font-size:14px;margin-top:60px">Demonstração educacional · Narração sintética</p></div><img alt="QR para o repositório" style="width:245px;height:245px" src="data:image/png;base64,'+qr+'"></body></html>');
  });
  console.log('Erros JavaScript: '+JSON.stringify(errors));
  if(errors.length)throw new Error('Falha JavaScript');
  await context.close();
  const recorded=await video.path();
  fs.copyFileSync(recorded,path.join(build,'prototipo_raw.webm'));
  // Verificação responsiva e upload em uma sessão sem gravação.
  const mobile=await browser.newPage({viewport:{width:390,height:844}});
  await mobile.goto('http://127.0.0.1:8501');await mobile.waitForSelector('#f-Amount');
  const over=await mobile.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(over)throw new Error('Rolagem horizontal na tela inicial móvel');
  await mobile.screenshot({path:path.join(build,'mobile.png'),fullPage:true});
  await mobile.locator('details.batch summary').click();
  await mobile.locator('#csv').setInputFiles(path.join(root,'demo/demo_final.csv'));
  await mobile.locator('#upload').click();
  await mobile.waitForFunction(()=>document.querySelector('#batch-results').innerText.includes('10 transações'));
  console.log('Interface, upload, exemplos e viewport móvel verificados.');
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
