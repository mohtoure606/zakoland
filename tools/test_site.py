import asyncio, subprocess, time, re, os, sys
from playwright.async_api import async_playwright
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); SITE=ROOT+'/docs'; OUT=ROOT+'/shots'; os.makedirs(OUT,exist_ok=True)
PAGES=['index.html','builders.html','landowners.html','about.html','contact.html','privacy.html','terms.html','404.html']
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8765','-d',SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome'))
            # icons + og
            pg=await b.new_page(viewport={'width':1200,'height':630})
            await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(300)
            og='''<html><head><style>@font-face{font-family:A;src:url(http://localhost:8765/assets/fonts/archivo-var.woff2)}body{margin:0;width:1200px;height:630px;position:relative;overflow:hidden;background:#161513;font-family:A}
            img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 70%}.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,19,18,.25),rgba(20,19,18,0) 40%,rgba(20,19,18,.35))}
            .t{position:absolute;left:0;right:0;top:64px;display:flex;justify-content:center}.t img{width:240px}.h{position:absolute;left:0;right:0;text-align:center;bottom:70px;color:#F4EFE6;font-size:64px;font-weight:540;font-stretch:112%;letter-spacing:-.02em;line-height:1.05}.s{color:#E7D7C1;font-size:24px;font-stretch:118%;margin-top:18px;letter-spacing:.03em;font-weight:500}</style></head>
            <body><img class=bg src="http://localhost:8765/assets/photo/hero-1280.jpg"><div class=sh></div><div class=t><img src="http://localhost:8765/assets/img/zako-lockup-white.svg"></div>
            <div class=h>Land. Opportunity. Vision.<div class=s>Residential Land Investment &amp; Acquisition</div></div></body></html>'''
            await pg.set_content(og); await pg.wait_for_timeout(800)
            await pg.screenshot(path=SITE+'/assets/img/og-image.jpg', type='jpeg', quality=85)
            for size,name in [(32,'favicon-32.png'),(180,'apple-touch-icon.png')]:
                await pg.set_viewport_size({'width':size,'height':size})
                await pg.set_content(f'<html><body style="margin:0;background:transparent"><img src="http://localhost:8765/assets/img/favicon.svg" style="width:{size}px;height:{size}px;display:block"></body></html>'); await pg.wait_for_timeout(200)
                await pg.screenshot(path=SITE+'/assets/img/'+name, omit_background=True)
            await pg.close()
            report=[]
            for vw,vh,tag in [(1440,900,'d'),(820,1180,'t'),(390,844,'m')]:
                ctx=await b.new_context(viewport={'width':vw,'height':vh},reduced_motion='reduce')
                pg=await ctx.new_page(); errs=[]; bad=[]
                pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
                pg.on('pageerror',lambda e: errs.append(str(e)))
                pg.on('response',lambda r: bad.append(f'{r.status} {r.url}') if r.status>=400 else None)
                for path in PAGES:
                    await pg.goto('http://localhost:8765/'+path)
                    await pg.evaluate('(async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)})()')
                    await pg.wait_for_timeout(700)
                    ov=await pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
                    title=await pg.title()
                    await pg.screenshot(path=f'{OUT}/{tag}-{path[:-5]}.png', full_page=True)
                    report.append(f'{tag} {path}: title="{title}" overflowX={ov}')
                report.append(f'{tag} console errors: {errs}'); report.append(f'{tag} bad responses: {bad}')
                await ctx.close()
            # link check
            import html.parser
            links=set()
            for path in PAGES:
                s=open(f'{SITE}/{path}').read()
                for h in re.findall(r'href="([^"]+)"',s)+re.findall(r'src="([^"]+)"',s):
                    if h.startswith(('http','mailto','#')): continue
                    f=h.split('#')[0]
                    if f and not os.path.exists(f'{SITE}/{f}'): links.add(f'{path} -> {h}')
                for h in re.findall(r'href="([a-z0-9-]+\.html)#([a-z0-9-]+)"',s):
                    t=open(f'{SITE}/{h[0]}').read()
                    if f'id="{h[1]}"' not in t: links.add(f'missing anchor {path} -> {h[0]}#{h[1]}')
            report.append(f'broken links: {sorted(links)}')
            # form preview behaviour
            ctx=await b.new_context(viewport={'width':1200,'height':900}); pg=await ctx.new_page()
            await pg.goto('http://localhost:8765/builders.html#criteria')
            await pg.click('button[type=submit]'); await pg.wait_for_timeout(200)
            report.append('empty submit valid?: '+str(await pg.evaluate('document.querySelector("#criteria form").checkValidity()')))
            await pg.fill('#b-company','Test Co'); await pg.fill('#b-name','Test'); await pg.fill('#b-email','t@example.com')
            await pg.click('label.chip:has(input[value=Lehi])'); await pg.check('#criteria input[name=consent]')
            await pg.click('button[type=submit]'); await pg.wait_for_timeout(200)
            report.append('valid submit status: '+(await pg.inner_text('#criteria .status')))
            await ctx.close(); await b.close()
            print('\n'.join(report))
    finally:
        srv.terminate()
asyncio.run(main())
