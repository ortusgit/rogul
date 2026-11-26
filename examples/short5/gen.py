import sys; sys.path.insert(0,'../kit')
from kit import *
S=[]
def add(*a,**k): S.append(scene(len(S)+1,*a,**k))
# 1 hook
add("hook","Hook","Psikolog John Gottman meminta pasangan bertengkar selama lima belas menit, lalu melacak mereka bertahun-tahun.",
  '<rect y="300" width="800" height="80" fill="#2f201c"/>'+person(250,170,TEAL,.9,"shake")+person(470,170,GOLD,.9,"shake",skirt=True)
  +f'<g transform="translate(360 120)"><g class="blink"><path d="M0-26l-12 26h10l-5 24 18-30h-10l6-20z" fill="{GOLD}"/></g></g>'
  +f'<g transform="translate(640 150)"><g class="pop d1"><circle r="58" fill="{CREAM}"/><circle r="48" fill="none" stroke="{DARK}" stroke-width="4"/><g class="needle" style="transform-origin:0 0"><line y2="-38" stroke="{BRICK}" stroke-width="5" stroke-linecap="round"/></g><rect x="-8" y="-72" width="16" height="12" fill="{CREAM}"/></g></g>'
  +T(640,240,0,"15 menit",22,GOLD,M,cls="fadeIn d2"),year="1970-an",tr="zoom")
# 2
add("bukan","Bukan seberapa sering","Hasilnya mengejutkan. Yang menentukan awet atau tidaknya bukan seberapa sering mereka bertengkar.",
  f'<g transform="translate(400 130)"><g class="zoomIn"><text text-anchor="middle" {F} font-size="54" fill="{CREAM}">sering bertengkar</text></g></g>'
  +f'<path class="strike" d="M190 112 L610 112" stroke="{BRICK}" stroke-width="10" stroke-linecap="round"/>'
  +f'<g transform="translate(400 230)"><g class="pop d2"><text text-anchor="middle" {F} font-size="40" fill="{GOLD}">≠ pasti bercerai</text></g></g>'
  +lontar(160,350,1.2,"sign","peek","d2",sign="!"),tr="pan")
# 3 5:1
hearts="".join(heart(150+k*62,150,.9,cls=f"pop d{min(5,k+1)}") for k in range(5))
add("rasio","Rasio 5:1","Pasangan yang awet punya rasio ajaib: setidaknya lima interaksi positif untuk setiap satu yang negatif, bahkan saat bertengkar.",
  f'<rect x="120" y="230" width="560" height="10" rx="5" fill="{MUTED}"/><path d="M400 240 l-30 60h60z" fill="{MUTED}"/>'
  +hearts+f'<g transform="translate(600 150)"><g class="pop d5"><path d="M-40 10a22 22 0 0 1 20-30a28 28 0 0 1 50 6a18 18 0 0 1 8 34h-70a16 16 0 0 1-8-10z" fill="#5a423b"/></g></g>'
  +T(400,90,0,"5 : 1",70,CREAM,cls="zoomIn"),tr="zoom")
# 4 1:1 cliff
add("jurang","Jurang 1:1","Kalau rasionya turun ke satu banding satu atau kurang, hubungan itu sedang berdiri di tepi jurang.",
  f'<path d="M0 380 V250 H470 l40 130z" fill="#5a423b"/><path d="M470 250 l40 130" stroke="#3a2723" stroke-width="6"/>'
  +person(330,130,TEAL,.75,"sway")+person(420,130,GOLD,.75,"sway",skirt=True)
  +f'<g transform="translate(590 120)"><g class="stampIn"><rect x="-90" y="-44" width="180" height="88" rx="10" fill="none" stroke="{BRICK}" stroke-width="8"/><text y="18" text-anchor="middle" {F} font-size="50" fill="{BRICK}">1 : 1</text></g></g>'
  +lontar(120,250,1.1,"none","peek","d2"),bg="#22182a",tr="pan")
# 5 positif
ic=lambda x,d,body,lab: f'<g transform="translate({x} 160)"><g class="pop {d}"><circle r="62" fill="{BG2}" stroke="{GOLD}" stroke-width="4"/>{body}</g></g>'+T(x,262,0,lab,22,CREAM,N,cls=f"fadeIn {d}")
add("positif","Interaksi positif","Positif itu sederhana: mendengarkan, bercanda, memegang tangan. Jadi, berapa rasio kalian minggu ini?",
  ic(220,"d1",f'<path d="M-14-30a26 26 0 0 1 40 22c0 16-16 18-16 32a12 12 0 0 1-22 2" fill="none" stroke="{CREAM}" stroke-width="8" stroke-linecap="round"/>',"mendengarkan")
  +ic(400,"d2",f'<circle r="34" fill="{GOLD}"/><path d="M-18 4a18 18 0 0 0 36 0z" fill="{DARK}"/><path d="M-18-12l8 4M18-12l-8 4" stroke="{DARK}" stroke-width="4"/>',"bercanda")
  +ic(580,"d3",f'<path d="M-40 10h30l10-8 10 8h30" stroke="{CREAM}" stroke-width="16" stroke-linecap="round" fill="none"/>',"pegang tangan")
  +T(400,330,0,"berapa rasio kalian?",28,GOLD,cls="fadeIn d4")+lontar(700,370,1.0,"lup","peek","d4"),tr="rise")
# 6 CTA
add("CTA","CTA","Rahasia lengkap pernikahan yang awet, segera di Kamasastra. Subscribe supaya tidak ketinggalan.",
  T(400,60,0,"SEGERA DI KAMASASTRA",20,GOLD,M)
  +'<rect x="250" y="90" width="300" height="170" rx="14" fill="#3a2723" stroke="#d9a441" stroke-width="4"/><g class="press"><polygon points="380,140 380,210 440,175" fill="#d9a441"/></g>'
  +T(400,310,0,"Rahasia pernikahan AWET",34,CREAM)+lontar(640,300,1.3,"point","slideR","d1",flip=True),tr="iris")
open('scenes.html','w').write("\n".join(S))
import re,html
for m in re.findall(r'data-text="([^"]*)"',"\n".join(S)): print(len(html.unescape(m)), html.unescape(m))
