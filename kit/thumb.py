"""Thumbnail Kamasastra 1280x720 (JPG < 2 MB).
Pemakaian: python3 kit/thumb.py out.jpg "BESAR" "baris atas" "baris bawah" [warna_aksen] [tanda]
  BESAR  : angka/kata utama (mis. "186/1.231")
  tanda  : teks papan yang dipegang Si Lontar (mis. "?" atau "!")
"""
import sys, os, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import lontar_svg

out, big, top, bottom = sys.argv[1:5]
acc = sys.argv[5] if len(sys.argv) > 5 else '#b5523b'
sign = sys.argv[6] if len(sys.argv) > 6 else '?'
fs = 210 if len(big) <= 6 else (160 if len(big) <= 9 else 120)
html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800;9..144,900&family=Space+Mono:wght@700&display=swap" rel="stylesheet">
<style>
*{{margin:0;box-sizing:border-box}}
body{{width:1280px;height:720px;overflow:hidden;background:radial-gradient(ellipse at 35% 40%,#4a2f28,#1f1513 70%);font-family:Fraunces,serif;position:relative}}
.brand{{position:absolute;top:40px;left:60px;font:700 28px "Space Mono",monospace;letter-spacing:10px;color:#d9a441}}
.top{{position:absolute;top:110px;left:60px;width:850px;font-weight:800;font-size:64px;line-height:1.05;color:#f4ecd8}}
.big{{position:absolute;top:250px;left:52px;font-weight:900;font-size:{fs}px;line-height:1;color:{acc};text-shadow:0 8px 0 rgba(0,0,0,.35);letter-spacing:-2px}}
.bottom{{position:absolute;bottom:56px;left:60px;font-weight:800;font-size:58px;color:#1f1513;background:#d9a441;padding:6px 26px 12px;border-radius:14px;transform:rotate(-2deg)}}
svg{{position:absolute;right:40px;bottom:10px;width:330px;height:560px}}
</style></head><body>
<div class="brand">KAMASASTRA</div><div class="top">{top}</div><div class="big">{big}</div><div class="bottom">{bottom}</div>
<svg viewBox="-10 -60 120 160"><g>{lontar_svg()}</g>
<g transform="translate(58 -40)"><path d="M0 70 l-4 -10" stroke="#a8834a" stroke-width="4"/><rect x="-6" y="-4" width="56" height="44" rx="5" fill="#f4ecd8" stroke="#a8834a" stroke-width="2.5"/>
<text x="22" y="30" text-anchor="middle" font-family="Fraunces,serif" font-weight="900" font-size="34" fill="#b5523b">{sign}</text></g></svg>
</body></html>'''

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': 1280, 'height': 720})
        await pg.set_content(html); await pg.wait_for_timeout(800)
        await pg.screenshot(path=out, type='jpeg', quality=90)
        await b.close()
asyncio.run(main())
print(out, os.path.getsize(out) // 1024, 'KB')
