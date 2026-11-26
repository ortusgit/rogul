"""Cetakan Kamasastra: animasi bersambung 16:9.
Pemakaian (dari folder topik): python3 ../kit/anim_page.py out.html "Judul halaman" [--noaudio]
Aturan: adegan digambar di viewBox 800x380 (area grafis); 15% bawah layar khusus subtitle.
Transisi dibaca dari atribut data-tr tiap adegan (pan|travel|zoom|rise|iris), bawaan pan.
"""
import re, sys, glob, base64, os, subprocess, html as H, json

out = sys.argv[1]
title = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 'Kamasastra'
noaudio = '--noaudio' in sys.argv
SHORT = '--short' in sys.argv
SRC = next((a.split('=',1)[1] for a in sys.argv if a.startswith('--src=')), 'scenes.html')
HEAD = next((a.split('=',1)[1] for a in sys.argv if a.startswith('--head=')), '')
VBY = next((int(a.split('=')[1]) for a in sys.argv if a.startswith('--vby=')), 0)
src = open(SRC, encoding='utf-8').read()
KIT = os.path.dirname(os.path.abspath(__file__))
anim_css = open(os.path.join(KIT, 'anim.css'), encoding='utf-8').read()
anim_css += """  .active .ring89{stroke-dasharray:565.5;stroke-dashoffset:565.5;animation:ring89 1.8s ease-out .4s forwards}
  @keyframes ring89{to{stroke-dashoffset:62}}
"""
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import lontar_svg
LONTAR = lontar_svg()
pita = open(os.path.join(KIT, 'pita.svg'), encoding='utf-8').read()

SHIFT = {'pan': 3.5, 'travel': 15, 'zoom': 1.5, 'rise': 1.5, 'iris': 1.5}

VB = f'viewBox="75 {VBY} 650 380"' if SHORT else f'viewBox="0 {VBY} 800 380"'
blocks = re.findall(r'<div class="scene".*?</svg>\s*</div>', src, re.S)
TR = [(re.search(r'data-tr="(\w+)"', b) or [None, 'pan'])[1] for b in blocks]
scenes = []
full = re.compile(r'<rect width="800" height="(?:450|380)" fill="([^"]+)"/>')
for k, b in enumerate(blocks):
    bgs = full.findall(b)
    bg = bgs[-1] if bgs else '#2f201c'
    b = full.sub('', b)
    b = re.sub(r' data-tr="\w+"', '', b).replace('<div class="scene"', f'<div class="scene" data-bg="{bg}" data-tr="{TR[k]}"', 1)
    b = b.replace('viewBox="0 0 800 450"', VB).replace('viewBox="0 0 800 380"', VB)
    scenes.append(b)

def chunks(t):
    parts = re.findall(r'[^.?!:]+[.?!:]*', t)
    res = []
    for p in (x.strip() for x in parts if x.strip()):
        if len(p) > (140 if SHORT else 90) and ',' in p:
            cs = [m.start() for m in re.finditer(',', p)]
            c = min(cs, key=lambda i: abs(i - len(p) / 2))
            res += [p[:c + 1].strip(), p[c + 1:].strip()]
        else:
            res.append(p)
    # gabungkan potongan sangat pendek dengan berikutnya
    out = []
    for p in res:
        if out and len(out[-1]) < (40 if SHORT else 22) and len(out[-1]) + len(p) < (150 if SHORT else 90):
            out[-1] += ' ' + p
        else:
            out.append(p)
    return out

texts = [H.unescape(re.search(r'data-text="([^"]*)"', b).group(1)) for b in blocks]
CH = [chunks(t) for t in texts]

if noaudio:
    VO = '[]'
else:
    files = sorted(glob.glob('audio/' + ('short' if SHORT else 'adegan') + '-*.mp3')); assert len(files) == len(blocks)
    os.makedirs('audio/web', exist_ok=True); uris = []
    for f in files:
        sm = 'audio/web/' + os.path.basename(f)
        if not os.path.exists(sm):
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-ac', '1', '-b:a', '64k', sm], check=True)
        uris.append('data:audio/mpeg;base64,' + base64.b64encode(open(sm, 'rb').read()).decode())
    VO = json.dumps(uris)


SHORT_CSS = """
  #stage{width:100vw;height:177.78vw;max-height:calc(100vh - 10px);max-width:calc((100vh - 10px)*9/16)}
  #far{width:400cqw}
  .scene{top:21%;height:32.84%}
  #band{display:none}
  #top{position:absolute;left:0;right:0;top:6.5%;text-align:center;z-index:6}
  #top .brand{font:700 3.4cqw "Space Mono",monospace;letter-spacing:1cqw;color:var(--gold)}
  #top h1{margin:2cqw 5cqw 0;font:800 9cqw/1.08 Fraunces,serif;color:var(--cream)}
  #sub{top:59%;bottom:auto;transform:translateX(-50%);max-width:86cqw;font:800 5.6cqw/1.32 Nunito,system-ui,sans-serif}
  .year{font-size:3.6cqw;top:2cqw;left:3cqw;padding:.6cqw 2cqw;border-radius:1.6cqw}
  #plane{width:30cqw}
  @keyframes fly2{0%{opacity:1;transform:translate(-32cqw,70cqw) rotate(-14deg)}50%{transform:translate(35cqw,48cqw) rotate(4deg)}100%{opacity:1;transform:translate(104cqw,56cqw) rotate(12deg)}}
  #vig{background:radial-gradient(ellipse at 50% 40%,transparent 55%,rgba(0,0,0,.4))}
"""

# lapisan parallax jauh: debu/bintang + bukit samar
import random
random.seed(4)
dots = ''.join(f'<circle cx="{random.uniform(0,4800):.0f}" cy="{random.uniform(0,900):.0f}" r="{random.choice([2,3,3,4,6])}" fill="#f4ecd8" opacity="{random.uniform(.15,.5):.2f}"/>' for _ in range(260))
hills = ''.join(f'<path d="M{x} 1080 q300 -{h} 600 0z" fill="#000" opacity=".18"/>' for x, h in [(i * 420 - 200, 180 + (i * 97) % 160) for i in range(13)])
far = f'<svg viewBox="0 0 4800 1080" preserveAspectRatio="none">{dots}{hills}</svg>'

page = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Nunito:wght@500;700;800&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
<style>
  :root{{--bg:#1f1513;--cream:#f4ecd8;--gold:#d9a441;--brick:#b5523b;--teal:#3aa6a0;--muted:#b9a99a}}
  *{{box-sizing:border-box}}
  html,body{{margin:0;background:#120c0b;color:var(--cream);font-family:Nunito,system-ui,sans-serif}}
  #mk{{height:10px;background:#000}}
  #stage{{position:relative;width:100vw;height:56.25vw;max-height:calc(100vh - 10px);max-width:calc((100vh - 10px)*16/9);margin:0 auto;overflow:hidden;
         background:#2f201c;transition:background-color 1.2s ease;container-type:inline-size}}
  #far{{position:absolute;top:0;left:0;width:250cqw;height:100%;transition:transform 1.3s cubic-bezier(.6,0,.3,1);will-change:transform}}
  #far svg{{width:100%;height:100%;display:block}}
  .scene{{position:absolute;left:0;top:0;width:100%;height:84.45%;opacity:0;pointer-events:none}}
  .scene.active,.scene.out{{opacity:1}}
  .scene>svg{{width:100%;height:100%;display:block;transform-origin:50% 45%}}
  .scene.active>svg{{animation:camPush 18s ease-out both}}
  @keyframes camPush{{from{{transform:scale(1)}}to{{transform:scale(1.07)}}}}
  /* transisi masuk/keluar */
  .scene.in-pan{{animation:panIn 1.2s cubic-bezier(.6,0,.3,1) both}} .scene.out-pan{{animation:panOut 1.2s cubic-bezier(.6,0,.3,1) both}}
  .scene.in-travel{{animation:panIn 1.5s cubic-bezier(.6,0,.3,1) both}} .scene.out-travel{{animation:panOutFar 1.5s cubic-bezier(.6,0,.3,1) both}}
  .scene.in-zoom{{animation:zoomIn2 1.1s cubic-bezier(.5,0,.3,1) both}} .scene.out-zoom{{animation:zoomOut2 1.1s cubic-bezier(.5,0,.3,1) both}}
  .scene.in-rise{{animation:riseIn 1.1s cubic-bezier(.6,0,.3,1) both}} .scene.out-rise{{animation:riseOut 1.1s cubic-bezier(.6,0,.3,1) both}}
  .scene.in-iris{{animation:irisIn 1.2s ease-in-out both;z-index:3;background:var(--sbg)}} .scene.out-iris{{animation:hold 1.2s linear both}}
  @keyframes panIn{{from{{transform:translateX(75%)}}to{{transform:none}}}}
  @keyframes panOut{{to{{transform:translateX(-75%);opacity:0}}}}
  @keyframes panOutFar{{to{{transform:translateX(-110%)}}}}
  @keyframes zoomIn2{{from{{transform:scale(.55);opacity:0}}to{{transform:none;opacity:1}}}}
  @keyframes zoomOut2{{to{{transform:scale(2.2);opacity:0}}}}
  @keyframes riseIn{{from{{transform:translateY(70%)}}to{{transform:none}}}}
  @keyframes riseOut{{to{{transform:translateY(-70%);opacity:0}}}}
  @keyframes irisIn{{from{{clip-path:circle(0% at 50% 50%)}}to{{clip-path:circle(75% at 50% 50%)}}}}
  @keyframes hold{{0%,92%{{opacity:1}}100%{{opacity:0}}}}
  .year{{position:absolute;top:2.4cqw;left:2.6cqw;font-family:"Space Mono",monospace;font-size:1.7cqw;background:var(--gold);color:var(--bg);
        padding:.3cqw 1cqw;border-radius:.8cqw;transform:translateY(-6cqw);transition:transform .6s cubic-bezier(.3,1.5,.5,1) .9s;z-index:2}}
  .scene.active .year{{transform:none}}
  /* lapisan atas */
  #vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(0,0,0,.38));z-index:5}}
  .lmouth{{transform-box:fill-box;transform-origin:center}}
  #stage.talking .scene.active:not(.out) .lmouth,#stage.talking #plane .lmouth{{animation:talk .2s ease-in-out infinite alternate}}
  .active .lbody{{animation:lbob 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}}
  .active .peek{{animation:peek .9s cubic-bezier(.3,1.5,.5,1) both}}.active .peek.d1{{animation-delay:.4s}}.active .peek.d2{{animation-delay:1.2s}}.active .peek.d3{{animation-delay:2s}}
  @keyframes peek{{from{{transform:translateY(140px)}}to{{transform:none}}}}
  .active .wave{{transform-box:fill-box;transform-origin:0% 100%;animation:wave .5s ease-in-out infinite alternate}}
  @keyframes wave{{from{{transform:rotate(-20deg)}}to{{transform:rotate(25deg)}}}}
  #band{{position:absolute;left:0;right:0;bottom:0;height:15.55%;background:linear-gradient(rgba(0,0,0,.05),rgba(0,0,0,.35));border-top:.15cqw solid rgba(244,236,216,.08);z-index:4}}
  @keyframes talk{{to{{transform:scaleY(.25)}}}}
  @keyframes lbob{{50%{{transform:translateY(-4%) rotate(-3deg)}}}}
  @keyframes hop{{from{{transform:translateY(0) rotate(-6deg)}}to{{transform:translateY(-14%) rotate(6deg)}}}}
  #sub{{position:absolute;left:50%;bottom:7.78%;transform:translate(-50%,50%);max-width:86cqw;width:max-content;z-index:8;text-align:center;
        font:800 1.95cqw/1.25 Nunito,system-ui,sans-serif;color:#fff8e8;background:none;padding:0 1cqw;
        text-shadow:0 .12cqw .2cqw rgba(0,0,0,.6);transition:opacity .25s}}
  #sub:empty{{opacity:0}}
  #plane{{position:absolute;left:0;top:0;width:13cqw;z-index:6;opacity:0;pointer-events:none}}
  #stage.flying #plane{{animation:fly2 1.5s cubic-bezier(.4,0,.4,1) both}}
  @keyframes fly2{{0%{{opacity:1;transform:translate(-12cqw,30cqw) rotate(-14deg)}}50%{{transform:translate(45cqw,8cqw) rotate(4deg)}}100%{{opacity:1;transform:translate(104cqw,16cqw) rotate(12deg)}}}}
  .active .eyes{{transform-box:fill-box;transform-origin:center;animation:blinkE 3.6s infinite}}
  @keyframes blinkE{{0%,90%,100%{{transform:none}}94%{{transform:scaleY(.1)}}}}
  {anim_css}
  .controls{{display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap;padding:12px}}
  .controls button{{font:700 14px Nunito,sans-serif;border:0;border-radius:999px;padding:8px 14px;cursor:pointer;background:var(--cream);color:var(--bg)}}
  .controls .ghost{{background:transparent;color:var(--cream);border:1.5px solid #5a423b}}
  .dot{{width:10px;height:10px;padding:0!important;background:#5a423b!important}} .dot.on{{background:var(--gold)!important}}
  footer{{color:var(--muted);font-size:12px;text-align:center;padding:0 12px 20px;line-height:1.6}}
  {SHORT_CSS if SHORT else ''}
  @media (prefers-reduced-motion:reduce){{*{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition:none!important}}}}
</style>
</head>
<body>
<div id="mk"></div>
<div id="stage">
  {HEAD}
  <div id="far">{far}</div>
  {''.join(scenes)}
  <svg id="plane" viewBox="-60 -70 180 130"><g transform="translate(42 -40) scale(.62)">{LONTAR}</g><path d="M4 30 L116 6 L60 54 L50 36z" fill="#f4ecd8"/><path d="M50 36 L116 6 L44 30z" fill="#d9b77a"/><path d="M4 30 q-30 6 -60 2" stroke="#f4ecd8" stroke-width="2" stroke-dasharray="6 6" fill="none" opacity=".7"/></svg>
  <div id="vig"></div>
  <div id="band"></div>
  <div id="sub" aria-live="polite"></div>
</div>
<div class="controls">
  <button class="ghost" id="prev">◀ Mundur</button><button id="play">▶ Putar</button><button class="ghost" id="next">Lanjut ▶</button>
  <div id="dots" style="display:flex;gap:5px;flex-wrap:wrap;justify-content:center;width:100%"></div>
</div>
<footer>Kamasastra · animasi edukasi · Sumber lengkap di adegan Daftar Pustaka. Draf menunggu tinjauan ahli.</footer>
<script>
const VO={VO};
const CH={json.dumps(CH, ensure_ascii=False)};
const SHIFT={json.dumps(SHIFT)};const SHORT={'true' if SHORT else 'false'};
{{
  const scenes=[...document.querySelectorAll('.scene')];
  const stage=document.getElementById('stage'), sub=document.getElementById('sub'), far=document.getElementById('far'), mk=document.getElementById('mk');
  const playBtn=document.getElementById('play'), dotsEl=document.getElementById('dots');
  const audio=new Audio();audio.preload='auto';
  let i=-1, playing=false, raf=null, nextT=null, playT=null, off=0, outT=null;
  const cum=CH.map(c=>{{let s=0;const tot=c.reduce((a,x)=>a+x.length,0);return c.map(x=>{{const v=s/tot;s+=x.length;return v}})}});
  scenes.forEach((_,k)=>{{const d=document.createElement('button');d.className='dot';d.setAttribute('aria-label','Adegan '+(k+1));d.onclick=()=>go(k);dotsEl.appendChild(d)}});
  const dots=[...dotsEl.children];
  const ov=document.createElement('button');ov.id='startOv';ov.textContent='▶ Putar dengan suara';
  ov.style.cssText='position:absolute;inset:0;margin:auto;width:max-content;height:max-content;padding:.7em 1.4em;border:0;border-radius:999px;background:#d9a441;color:#1f1513;font:800 '+(SHORT?'5cqw':'2cqw')+' Nunito,sans-serif;cursor:pointer;z-index:20';
  stage.appendChild(ov);ov.onclick=()=>setPlaying(true);
  function showSub(){{
    const d=audio.duration||0,c=audio.currentTime||0,ch=CH[i];
    let j=0; if(d){{const f=Math.min(1,c/(d*0.93)); for(let n=0;n<ch.length;n++) if(f>=cum[i][n]) j=n;}}
    if(sub.textContent!==ch[j]) sub.textContent=ch[j];
  }}
  function loop(){{cancelAnimationFrame(raf);const st=()=>{{showSub();if(playing)raf=requestAnimationFrame(st)}};raf=requestAnimationFrame(st)}}
  audio.addEventListener('playing',()=>stage.classList.add('talking'));
  audio.addEventListener('pause',()=>stage.classList.remove('talking'));
  audio.addEventListener('ended',()=>{{
    stage.classList.remove('talking');
    if(!playing)return;
    setTimeout(()=>{{if(playing)sub.textContent=''}},250);
    if(i<scenes.length-1) nextT=setTimeout(()=>go(i+1),400);
    else {{playing=false;playBtn.textContent='↺ Ulangi';}}
  }});
  function go(k){{
    clearTimeout(nextT);clearTimeout(playT);clearTimeout(outT);
    k=(k+scenes.length)%scenes.length;
    const prev=i; i=k;
    const tr=prev<0?'zoom':scenes[k].dataset.tr;
    scenes.forEach(s=>s.className=s.className.replace(/\\b(in|out)-\\w+|\\bout\\b|\\bactive\\b/g,'').trim());
    if(prev>=0&&prev!==k){{scenes[prev].classList.add('active','out','out-'+tr);
      const p=prev; outT=setTimeout(()=>{{if(p!==i)scenes[p].classList.remove('active','out','out-'+tr)}},1600);}}
    void scenes[k].offsetWidth;
    scenes[k].classList.add('active','in-'+tr);scenes[k].style.setProperty('--sbg',scenes[k].dataset.bg);
    stage.style.backgroundColor=scenes[k].dataset.bg;
    off+= (prev<0?0:SHIFT[tr]); far.style.transform='translateX(-'+((SHORT?off*2.4:off)%(SHORT?280:140))+'cqw)';
    stage.classList.add('moving'); setTimeout(()=>stage.classList.remove('moving'),1200);
    if(tr==='travel'){{stage.classList.remove('flying');void stage.offsetWidth;stage.classList.add('flying');}}
    dots.forEach((d,n)=>d.classList.toggle('on',n===k));
    mk.style.background=(k%2)?'#fff':'#000';
    if(window.__log)window.__log.push({{e:'go',i:k,t:performance.now()}});
    audio.pause(); if(VO.length){{audio.src=VO[k];}}
    sub.textContent='';
    if(playing){{playT=setTimeout(()=>{{audio.play().catch(()=>setPlaying(false));loop();}},350);}}
    else sub.textContent=CH[k][0];
  }}
  function setPlaying(p){{
    ov.style.display='none';
    if(p&&i===scenes.length-1&&audio.ended){{playing=true;playBtn.textContent='⏸ Jeda';go(0);return;}}
    playing=p;playBtn.textContent=p?'⏸ Jeda':'▶ Putar';
    if(p){{ if(audio.ended){{go(i);return;}} audio.play().catch(()=>{{playing=false;playBtn.textContent='▶ Putar'}});loop(); }}
    else{{audio.pause();clearTimeout(nextT);clearTimeout(playT);}}
  }}
  playBtn.onclick=()=>setPlaying(!playing);
  document.getElementById('next').onclick=()=>go(i+1);
  document.getElementById('prev').onclick=()=>go(i-1);
  document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight')go(i+1);else if(e.key==='ArrowLeft')go(i-1);else if(e.key===' '){{e.preventDefault();setPlaying(!playing)}}}});
  window.__player={{go,setPlaying,audio,get i(){{return i}}}};
  go(0);
}}
</script>
</body>
</html>'''
open(out, 'w', encoding='utf-8').write(page)
print(out, round(os.path.getsize(out) / 1e6, 2), 'MB', 'max chunk', max(len(x) for c in CH for x in c))
