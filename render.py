import asyncio,sys,json,time
from playwright.async_api import async_playwright
f,W,H,css,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5]
preview = len(sys.argv)>6
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--autoplay-policy=no-user-gesture-required'])
        kw=dict(viewport={'width':W,'height':H})
        if not preview: kw['record_video_dir']='rec/'+out; kw['record_video_size']={'width':W,'height':H}
        ctx=await b.new_context(**kw)
        t0=time.monotonic()
        pg=await ctx.new_page()
        await pg.goto('file:///home/claude/kamasastra/'+f)
        await pg.add_style_tag(content=css)
        await pg.evaluate("""()=>{window.__log=[];const a=__player.audio;
          ['playing','waiting','ended'].forEach(ev=>a.addEventListener(ev,()=>window.__log.push({e:ev,i:__player.i,t:performance.now(),c:a.currentTime})));}""")
        await pg.wait_for_timeout(1500)
        if preview:
            await pg.evaluate("document.getElementById('startOv').style.display='none'")
            for k in [0,5]:
                await pg.evaluate(f"__player.go({k})"); await pg.wait_for_timeout(2500)
                await pg.screenshot(path=f'/tmp/{out}-p{k}.png')
            await b.close(); return
        click_wall=time.monotonic()-t0
        nav=await pg.evaluate("performance.now()")
        await pg.evaluate('__player.setPlaying(true)')
        n=await pg.evaluate("document.querySelectorAll('.scene').length")
        while True:
            await pg.wait_for_timeout(1000)
            done=await pg.evaluate(f"__player.i==={n-1}&&__player.audio.ended")
            if done: break
        await pg.wait_for_timeout(1500)
        log=await pg.evaluate("window.__log")
        end=await pg.evaluate("performance.now()")
        await ctx.close(); await b.close()
        # offset: video t=0 approx context start; page perf t=nav corresponds to wall click_wall
        json.dump({'log':log,'nav':nav,'click_wall':click_wall,'end':end},open(f'rec/{out}.json','w'))
asyncio.run(main())
