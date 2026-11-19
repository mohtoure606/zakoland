import asyncio, subprocess, time, json, os
from playwright.async_api import async_playwright
AXE=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','node_modules','axe-core','axe.min.js')).read()
PAGES=['index.html','builders.html','landowners.html','about.html','contact.html','privacy.html','terms.html','404.html']
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8766','-d',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/usr/bin/google-chrome')); pg=await b.new_page(); await pg.emulate_media(reduced_motion='reduce')
            for path in PAGES:
                await pg.goto('http://localhost:8766/'+path); await pg.add_script_tag(content=AXE)
                r=await pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa']}).then(r=>r.violations.map(v=>v.id+' ('+v.nodes.length+'): '+v.nodes.slice(0,2).map(n=>n.target.join(' ')).join(' | ')))")
                print(path, r if r else 'no violations')
            await b.close()
    finally: srv.terminate()
asyncio.run(main())
