import sys, re, html; sys.path.insert(0,'../kit')
from kit import *
CREAM, GOLD, BRICK, TEAL, SKY, MUTED, DARK, BG2 = "#f4ecd8", "#d9a441", "#b5523b", "#3aa6a0", "#8ecae6", "#b9a99a", "#1f1513", "#3a2723"
S=[]
def add(*a,**k): S.append(scene(len(S)+1,*a,**k))
def house(x,y,lit=False,s=1):
    g=' class="glow"' if lit else ''
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-60 0v-70l60-44 60 44v70z" fill="#a0704a"/><rect{g} x="-14" y="-40" width="28" height="40" fill="{GOLD}"/></g>'
night=('<rect width="800" height="380" fill="#1b2340"/>'
  f'<g class="blink"><circle cx="140" cy="60" r="3" fill="{CREAM}"/><circle cx="300" cy="40" r="2" fill="{CREAM}"/><circle cx="470" cy="70" r="3" fill="{CREAM}"/></g>'
  f'<circle cx="620" cy="70" r="30" fill="{CREAM}"/><path d="M0 250l140-100 120 70 150-110 170 110 220-50v130H0z" fill="#2c3a5a"/>'
  f'<rect y="290" width="800" height="90" fill="#2d5f6e"/><path d="M90 320h110M300 345h160M540 325h110" stroke="{SKY}" stroke-width="3" opacity=".6"/>')
walker=f'<g transform="translate(300 250)"><g class="runX"><g transform="scale(.42)"><circle r="32" fill="{CREAM}"/><rect x="-32" y="36" width="64" height="104" rx="26" fill="{TEAL}"/></g></g></g>'
# 1 hook
add("hook","Hook","Bayangkan punya suami yang hanya datang malam hari, lalu pulang ke rumah ibunya sebelum fajar. Bagi suku Mosuo, itu biasa.",
  night+house(170,290,True)+house(630,290)+walker
  +T(170,318,0,"rumah kekasih",15,CREAM,M)+T(630,318,0,"rumah ibunya",15,CREAM,M)
  +T(400,130,0,"pulang sebelum fajar",30,GOLD,cls="fadeIn d2"),year="Mosuo · Tiongkok",tr="zoom")
# 2 peta
add("peta","Danau Lugu","Mereka tinggal di sekitar Danau Lugu, di perbatasan Yunnan dan Sichuan, Tiongkok. Jumlahnya sekitar empat puluh ribu orang.",
  f'<rect width="800" height="380" fill="#2a3b2e"/><path d="M90 40h620v300H90z" fill="#3f5a3f" stroke="{CREAM}" stroke-width="3" stroke-dasharray="2 0"/>'
  +f'<path class="strike" d="M400 40 L400 340" stroke="{BRICK}" stroke-width="5" stroke-dasharray="14 10"/>'
  +f'<g transform="translate(400 190)"><g class="zoomIn"><path d="M-110-20c20-60 90-70 140-40s90 30 80 80-70 80-130 60-110-40-90-100z" fill="{SKY}" stroke="{CREAM}" stroke-width="4"/>'
  +f'<text y="8" text-anchor="middle" {F} font-size="26" fill="{DARK}">Danau Lugu</text></g></g>'
  +T(230,80,0,"YUNNAN",20,CREAM,M,cls="fadeIn d1")+T(570,80,0,"SICHUAN",20,CREAM,M,cls="fadeIn d1")
  +f'<g transform="translate(400 320)"><g class="pop d3"><rect x="-120" y="-30" width="240" height="52" rx="14" fill="{GOLD}"/><text y="6" text-anchor="middle" {N} font-size="24" fill="{DARK}">± 40.000 orang</text></g></g>'
  +lontar(150,372,.9,"lup","peek","d3"),tr="travel")
# 3 tidak serumah
add("serumah","Tidak serumah","Tradisi ini disebut pernikahan berjalan. Pasangan tidak tinggal serumah. Masing-masing tetap tinggal bersama keluarga ibunya.",
  f'<rect width="800" height="380" fill="#2f201c"/>'
  +T(400,70,0,"pernikahan berjalan",38,CREAM,cls="zoomIn")+T(400,104,0,"tisese · zǒu hūn",18,GOLD,M,cls="fadeIn d1")
  +house(220,320,s=1.1)+house(580,320,s=1.1)
  +person(170,200,BRICK,.55,"bob",skirt=True)+person(270,200,TEAL,.55,"bob","b2",skirt=True)
  +person(530,200,BRICK,.55,"bob","b3",skirt=True)+person(630,200,SKY,.55,"bob")
  +T(220,350,0,"keluarga ibu (dia)",15,CREAM,M)+T(580,350,0,"keluarga ibu (dia)",15,CREAM,M)
  +f'<g transform="translate(400 240)"><g class="pop d2"><circle r="36" fill="{BRICK}"/><path d="M-16-16l32 32M16-16l-32 32" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/></g></g>'
  +T(400,300,0,"tidak serumah",18,GOLD,M,cls="fadeIn d3"),tr="pan")
# 4 paman
add("paman","Peran paman","Anak dibesarkan keluarga ibu. Paman dari pihak ibu ikut mendidik dan menanggung, peran yang di banyak tempat dipegang ayah.",
  f'<rect width="800" height="380" fill="#3a2723"/><path d="M130 350v-170l170-100 170 100v170z" fill="#a0704a"/>'
  +person(215,230,BRICK,.62,"bob",skirt=True)+child(300,280,SKY)+person(385,230,TEAL,.62,"bob","b3")
  +T(215,372,0,"ibu",15,CREAM,M)+T(300,372,0,"anak",15,CREAM,M)+T(385,372,0,"paman",15,GOLD,M)
  +f'<g transform="translate(585 150)"><g class="pop d2"><rect x="-115" y="-40" width="230" height="80" rx="16" fill="{TEAL}"/><text y="-6" text-anchor="middle" {N} font-size="21" fill="{DARK}">mendidik</text><text y="22" text-anchor="middle" {N} font-size="21" fill="{DARK}">&amp; menanggung</text></g></g>'
  +lontar(600,330,1.0,"point","slideR","d3",flip=True),tr="rise")
# 5 bukan bebas
add("bukanbebas","Bukan bebas","Tapi ini bukan cinta bebas tanpa aturan. Banyak pasangan Mosuo bertahan lama, dan pariwisata kini ikut mengubah tradisinya.",
  f'<rect width="800" height="380" fill="#2f201c"/>'
  +f'<g transform="translate(400 80)"><g class="zoomIn"><text text-anchor="middle" {F} font-size="44" fill="{CREAM}">"cinta bebas"</text></g></g>'
  +f'<path class="strike" d="M200 68 L600 68" stroke="{BRICK}" stroke-width="10" stroke-linecap="round"/>'
  +person(250,190,TEAL,.7,"sway")+person(340,190,GOLD,.7,"sway",skirt=True)+heart(295,150,.8)
  +T(295,350,0,"pasangan jangka panjang",17,CREAM,M,cls="fadeIn d2")
  +f'<g transform="translate(560 230)"><g class="pop d3"><rect x="-55" y="-34" width="110" height="72" rx="10" fill="{CREAM}"/><circle cy="2" r="22" fill="{BG2}"/><circle cy="2" r="11" fill="{SKY}"/><rect x="22" y="-44" width="26" height="12" rx="3" fill="{CREAM}"/></g></g>'
  +T(560,330,0,"pariwisata",17,GOLD,M,cls="fadeIn d3"),tr="pan")
# 6 CTA
add("CTA","CTA","Jadi, setia itu kodrat atau budaya? Jawabannya ada di video lengkap Kamasastra. Tonton sekarang.",
  T(400,55,0,"VIDEO LENGKAP",20,GOLD,M)
  +'<rect x="250" y="80" width="300" height="170" rx="14" fill="#3a2723" stroke="#d9a441" stroke-width="4"/><g class="press"><polygon points="380,130 380,200 440,165" fill="#d9a441"/></g>'
  +T(400,300,0,"Setia: kodrat atau budaya?",30,CREAM)+lontar(668,372,1.0,"point","slideR","d1",flip=True),tr="iris")
open('scenes-short.html','w').write("\n".join(S))
tot=0
for m in re.findall(r'data-text="([^"]*)"',"\n".join(S)):
    t=html.unescape(m); tot+=len(t); print(len(t), t)
print("total",tot)
