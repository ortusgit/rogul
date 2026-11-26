import re, html, sys
sys.path.insert(0,'../kit')
from kit import lontar, F, M, CREAM, GOLD, BRICK
src=open('scenes.html').read()
blocks={re.search(r'data-id="([^"]+)"',b).group(1):b for b in re.findall(r'<!-- \d+ [^>]*-->\n\s*<div class="scene".*?</svg>\s*</div>',src,re.S)}
plan=[
 ("angka","zoom","Dari seribu dua ratus tiga puluh satu masyarakat yang dicatat antropolog, cuma seratus delapan puluh enam yang monogami."),
 ("pew","pan","Tapi hari ini, hanya sekitar dua persen penduduk dunia yang tinggal di rumah tangga poligami."),
 ("himba48","travel","Di suku Himba, Namibia, empat puluh delapan persen anak bukan anak biologis suami ibunya. Dan para suami umumnya tahu."),
 ("amazon","travel","Di Amazon, puluhan masyarakat percaya seorang anak bisa punya lebih dari satu ayah biologis."),
 ("indonesia","travel","Indonesia menganut asas monogami. Jadi, setia itu kodrat atau budaya? Jawab di komentar."),
 ("CTA","iris","Perjalanan lengkap ke empat budaya ini ada di video Kamasastra."),
]
cta=('<div class="scene" data-id="CTA" data-text="">\n      <svg viewBox="0 0 800 450">\n        <rect width="800" height="450" fill="#2f201c"/>'
     f'<text x="400" y="80" text-anchor="middle" {M} font-size="22" fill="{GOLD}" letter-spacing="6">KAMASASTRA</text>'
     '<rect x="250" y="110" width="300" height="170" rx="14" fill="#3a2723" stroke="#d9a441" stroke-width="4"/><g class="press"><polygon points="380,160 380,230 440,195" fill="#d9a441"/></g>'
     f'<text x="400" y="330" text-anchor="middle" {F} font-size="34" fill="{CREAM}">Tonton versi lengkap</text>'
     + lontar(620, 300, 1.3, "point", "slideR", "d1", flip=True) + '\n      </svg>\n    </div>')
extra={"angka":lontar(105,392,.95,"lup","peek","d3"),"himba48":lontar(405,392,.8,"none","peek","d3")}
out=[]
for sid,tr,txt in plan:
    b=cta if sid=="CTA" else blocks[sid]
    b=re.sub(r'data-text="[^"]*"','data-text="'+html.escape(txt,quote=True)+'"',b,count=1)
    b=re.sub(r' data-tr="\w+"','',b).replace('<div class="scene"',f'<div class="scene" data-tr="{tr}"',1)
    if sid=="indonesia": b=b.replace('translate(740 392) scale(1.1)','translate(600 398) scale(0.8)')
    if sid in extra: b=b.replace('\n      </svg>',extra[sid]+'\n      </svg>',1)
    out.append(b)
open('scenes-short.html','w').write("\n".join(out))
