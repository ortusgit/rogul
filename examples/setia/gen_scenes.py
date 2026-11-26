import html, sys
sys.path.insert(0,'../kit')
from kit import lontar
BG1, BG2 = "#2f201c", "#3a2723"
CREAM, GOLD, BRICK, TEAL, SKY, MUTED, DARK = "#f4ecd8", "#d9a441", "#b5523b", "#3aa6a0", "#8ecae6", "#b9a99a", "#1f1513"
F = 'font-family="Fraunces,serif" font-weight="800"'
M = 'font-family="Space Mono,monospace"'
N = 'font-family="Nunito,sans-serif" font-weight="800"'

def person(x, y, color, s=1.0, anim="bob", cls="", face=True, skirt=False, head=CREAM):
    body = (f'<path d="M-34 36h68l12 104h-92z" fill="{color}"/>' if skirt
            else f'<rect x="-32" y="36" width="64" height="104" rx="26" fill="{color}"/>')
    f = ('<g class="eyes"><circle cx="-10" cy="-2" r="4" fill="#1f1513"/><circle cx="10" cy="-2" r="4" fill="#1f1513"/></g>'
         '<path d="M-8 14q8 6 16 0" stroke="#1f1513" stroke-width="3" fill="none"/>') if face else ""
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="{anim} {cls}">'
            f'<circle r="32" fill="{head}"/>{body}{f}</g></g>')

def child(x, y, color=GOLD, anim="bob", cls="b2"):
    return (f'<g transform="translate({x} {y})"><g class="{anim} {cls}"><circle r="20" fill="{CREAM}"/>'
            f'<rect x="-20" y="24" width="40" height="60" rx="16" fill="{color}"/>'
            f'<g class="eyes"><circle cx="-6" cy="-2" r="3" fill="#1f1513"/><circle cx="6" cy="-2" r="3" fill="#1f1513"/></g></g></g>')

def heart(x, y, s=1, color=BRICK, cls="beat"):
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="{cls}">'
            f'<path d="M0-8c-10-20-40-8-30 14l30 28 30-28c10-22-20-34-30-14z" fill="{color}"/></g></g>')

def card(x, y, journal, ref, rot=-2, d="d3"):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><g class="fadeIn {d}"><rect width="210" height="54" rx="3" fill="{CREAM}"/>'
            f'<rect width="210" height="6" fill="{BRICK}"/><text x="10" y="26" font-family="Fraunces,serif" font-style="italic" font-weight="600" font-size="13" fill="{DARK}">{journal}</text>'
            f'<text x="10" y="44" {M} font-size="10" fill="#5a423b">{ref}</text></g></g>')

def T(x, y, s, txt, size=20, fill=CREAM, font=F, anchor="middle", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<text{c} x="{x}" y="{y}" text-anchor="{anchor}" {font} font-size="{size}" fill="{fill}">{txt}</text>'

def scene(num, sid, title, text, body, year=None, bg=BG1):
    y = f'\n      <div class="year">{year}</div>' if year else ""
    return (f'    <!-- {num:02d} {title} -->\n    <div class="scene" data-id="{sid}" data-text="{html.escape(text, quote=True)}">{y}\n'
            f'      <svg viewBox="0 0 800 450">\n        <rect width="800" height="450" fill="{bg}"/>\n        {body}\n      </svg>\n    </div>\n')

S = []
TR=['zoom', 'pan', 'iris', 'rise', 'pan', 'zoom', 'pan', 'pan', 'zoom', 'pan', 'zoom', 'rise', 'rise', 'travel', 'zoom', 'pan', 'travel', 'pan', 'travel', 'zoom', 'travel', 'pan', 'pan', 'iris', 'rise', 'rise', 'pan', 'iris']
def add(*a, **k):
    sc = scene(len(S) + 1, *a, **k)
    S.append(sc.replace(' data-text=', f' data-tr="{TR[len(S)]}" data-text=', 1))

ring = lambda x, y, c, cls: f'<g transform="translate({x} {y})"><g class="wiggle {cls}"><circle r="34" fill="none" stroke="{c}" stroke-width="12"/><path d="M-10-40l10-14 10 14z" fill="{SKY}"/></g></g>'

# 01
add("judul", "Judul",
    "Halo, aku Si Lontar lagi. Kemarin kita bongkar kenapa orang selingkuh. Hari ini pertanyaannya lebih berani: apakah setia itu kodrat manusia, atau aturan buatan budaya?",
    T(400, 96, 0, "KAMASASTRA", 20, GOLD, M).replace('font-size="20"', 'font-size="20" letter-spacing="6"')
    + T(400, 184, 0, "Setia itu", 50, CREAM, F, cls="fadeIn d1")
    + f'<g transform="translate(400 268)"><g class="zoomIn"><text text-anchor="middle" {F} font-size="86" fill="{BRICK}">BUDAYA?</text></g></g>'
    + T(400, 332, 0, "…atau kodrat manusia?", 30, GOLD, 'font-family="Fraunces,serif" font-weight="600"', cls="fadeIn d3")
    + ring(140, 150, GOLD, "") + ring(178, 170, CREAM, "w2") + ring(640, 330, GOLD, "w2") + ring(676, 350, CREAM, "") + lontar(120, 392, 1.3, "wave", "pop", "d3"))

# 02
card3 = lambda x, d, icon, lab: (f'<g transform="translate({x} 220)"><g class="pop {d}"><rect x="-110" y="-130" width="220" height="250" rx="20" fill="{BG2}" stroke="{GOLD}" stroke-width="3"/>'
                                 f'{icon}<text y="100" text-anchor="middle" {N} font-size="20" fill="{CREAM}">{lab}</text></g></g>')
ic1 = person(0, -60, TEAL, .55, "bob") + person(-60, -40, BRICK, .45, "bob", "b2", skirt=True) + person(60, -40, GOLD, .45, "bob", "b3", skirt=True)
ic2 = person(-55, -60, TEAL, .5, "bob") + person(55, -60, SKY, .5, "bob", "b3") + child(0, -10, GOLD)
ic3 = (f'<path d="M-70 40v-60l40-34 40 34v60z" fill="{CREAM}"/><rect x="-42" y="6" width="22" height="34" fill="{BG2}"/>'
       f'<circle cx="60" cy="-80" r="18" fill="{GOLD}"/><g class="runX"><g transform="translate(20 -10) scale(.4)"><circle r="32" fill="{CREAM}"/><rect x="-32" y="36" width="64" height="104" rx="26" fill="{TEAL}"/></g></g>')
add("tiga", "Tiga dunia",
    "Bayangkan ini. Di satu tempat, punya dua istri itu sah. Di tempat lain, seorang anak boleh punya dua ayah. Di tempat lain lagi, suami tidak tinggal serumah. Semuanya nyata.",
    card3(160, "d1", ic1, "2 istri, sah") + card3(400, "d2", ic2, "anak, 2 ayah") + card3(640, "d3", ic3, "suami tak serumah"), bg=BG2)

# 03
bubble = lambda x, y, w, txt, fill, tc, d: (f'<g transform="translate({x} {y})"><g class="pop {d}"><rect x="{-w/2}" y="-34" width="{w}" height="62" rx="18" fill="{fill}"/>'
                                            f'<text y="6" text-anchor="middle" {N} font-size="19" fill="{tc}">{txt}</text></g></g>')
add("debat", "Dimas vs Sari",
    "Dimas, dalam kisah rekaan kita, berdebat dengan Sari. Kata Dimas, manusia aslinya tidak monogami. Kata Sari, itu cuma alasan. Siapa yang benar? Kita cek datanya.",
    '<rect y="360" width="800" height="90" fill="#2f201c"/>'
    + person(250, 230, TEAL, 1, "sway") + person(550, 230, GOLD, 1, "sway", skirt=True)
    + bubble(250, 110, 330, "“Manusia aslinya tak monogami!”", CREAM, DARK, "d1")
    + bubble(560, 150, 230, "“Itu cuma alasan.”", BRICK, CREAM, "d2")
    + f'<g transform="translate(400 290)"><g class="pop d3"><circle r="30" fill="{GOLD}"/><text y="12" text-anchor="middle" {F} font-size="34" fill="{DARK}">?</text></g></g>'
    + T(250, 388, 0, "Dimas", 16, CREAM, M) + T(550, 388, 0, "Sari", 16, CREAM, M) + lontar(700, 392, 1.1, "lup", "peek", "d3"), year="Ilustrasi", bg="#22182a")

# 04
pin = lambda x, y, lab, d, c=BRICK: (f'<g transform="translate({x} {y})"><g class="pop {d}"><path d="M0 0c-14-18-20-26-20-36a20 20 0 0 1 40 0c0 10-6 18-20 36z" fill="{c}"/><circle cy="-36" r="7" fill="{CREAM}"/>'
                                      f'<text y="24" text-anchor="middle" {M} font-size="14" fill="{CREAM}">{lab}</text></g></g>')
land = '#5a423b'
add("peta", "Rute",
    "Hari ini kita keliling empat tempat: Afrika Barat, Namibia, hutan Amazon, dan sebuah danau di pegunungan Tiongkok. Setelah itu, kita pulang ke Indonesia.",
    f'<g class="driftX"><path d="M90 120q60-50 140-20t40 120q-30 90-80 120-40-40-60-110-50-40-40-110z" fill="{land}"/>'
    f'<path d="M330 110q60-40 120-10 30 50 10 100 20 70-30 130-40-10-60-80-60-30-60-80 0-40 20-60z" fill="{land}"/>'
    f'<path d="M480 90q120-40 220 10 20 60-30 100-60 10-100 40-40-30-60-70-30-40-30-80z" fill="{land}"/>'
    f'<path d="M600 300q40-10 90 10-10 20-60 20-30-10-30-30z" fill="{land}"/></g>'
    + pin(370, 205, "Afrika Barat", "d1") + pin(420, 320, "Namibia", "d2") + pin(190, 270, "Amazon", "d3")
    + pin(600, 150, "Tiongkok", "d4") + pin(645, 300, "Indonesia", "d5", TEAL)
    + T(400, 60, 0, "4 budaya + 1 rumah", 28, GOLD))

# 05
add("atlas", "Ethnographic Atlas",
    "Antropolog George Murdock menyusun Ethnographic Atlas, katalog aturan keluarga dari seribu dua ratus tiga puluh satu masyarakat di seluruh dunia.",
    f'<g transform="translate(250 230)"><g class="sway"><rect x="-120" y="-130" width="240" height="250" rx="10" fill="{BRICK}"/>'
    f'<rect x="-104" y="-114" width="208" height="218" rx="6" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    f'<text y="-50" text-anchor="middle" {F} font-size="21" fill="{CREAM}">ETHNOGRAPHIC</text><text y="-16" text-anchor="middle" {F} font-size="26" fill="{CREAM}">ATLAS</text>'
    f'<circle cy="50" r="34" fill="none" stroke="{GOLD}" stroke-width="4"/><path d="M-34 50h68M0 16v68M-24 30q24 20 48 0M-24 70q24-20 48 0" stroke="{GOLD}" stroke-width="3" fill="none"/></g></g>'
    + T(570, 200, 0, "1.231", 96, CREAM, F, cls="fadeIn d1") + T(570, 248, 0, "masyarakat dicatat", 20, GOLD, M, cls="fadeIn d2")
    + card(470, 300, "Ethnographic Atlas", "Murdock · 1967 · Univ. Pittsburgh", 2) + lontar(405, 392, 1.0, "point", "peek", "d2"), year="1967", bg=BG2)

# 06
bars = [(186, "monogami", TEAL, ""), (453, "poligini sesekali", GOLD, "d1"), (588, "poligini sering", BRICK, "d2"), (4, "poliandri", SKY, "d3")]
b = f'<line x1="120" y1="330" x2="680" y2="330" stroke="{MUTED}" stroke-width="3"/>'
for k, (v, lab, c, d) in enumerate(bars):
    h = max(4, v / 588 * 210); x = 140 + k * 140
    b += f'<rect class="growUp {d}" x="{x}" y="{330-h:.0f}" width="100" height="{h:.0f}" rx="6" fill="{c}"/>'
    b += T(x + 50, 320 - h, 0, str(v), 34, CREAM, F, cls=f"fadeIn {d}") + "".join(T(x + 50, 354 + 17*i, 0, w, 14, CREAM, M) for i, w in enumerate(lab.split(" ")))
add("angka", "Angka atlas",
    "Hasilnya mengejutkan. Hanya seratus delapan puluh enam yang monogami. Lebih dari seribu masyarakat membolehkan laki-laki beristri lebih dari satu, entah sesekali atau sering.",
    b + T(400, 62, 0, "aturan pernikahan · 1.231 masyarakat", 18, GOLD, M))

# 07
vil = lambda x: f'<g transform="translate({x} 0)"><path d="M-30 0v-40l30-26 30 26v40z" fill="{CREAM}"/><rect x="-8" y="-24" width="16" height="24" fill="{BG2}"/></g>'
add("bukanorang", "Masyarakat vs orang",
    "Tapi tunggu. Itu hitungan masyarakat, bukan hitungan orang. Di masyarakat yang membolehkan poligami pun, kebanyakan pernikahan tetap satu suami, satu istri.",
    f'<g transform="translate(0 200)"><g class="slideL">{vil(130)}{vil(210)}{vil(290)}</g></g>' + T(210, 250, 0, "1 masyarakat", 18, GOLD, M)
    + f'<g class="pop d3"><text x="400" y="190" text-anchor="middle" {F} font-size="56" fill="{CREAM}">≠</text></g>'
    + person(540, 140, TEAL, .6, "bob") + person(600, 150, GOLD, .55, "bob", "b2", skirt=True) + person(680, 140, TEAL, .6, "bob", "b3")
    + T(610, 250, 0, "orang", 18, GOLD, M)
    + f'<g transform="translate(400 340)"><g class="zoomIn z2"><rect x="-260" y="-36" width="520" height="66" rx="16" fill="{BRICK}"/>'
    f'<text y="10" text-anchor="middle" {F} font-size="26" fill="{CREAM}">kebanyakan tetap 1 suami + 1 istri</text></g></g>', bg=BG2)

# 08
g = ""
for r in range(10):
    for c in range(10):
        n = r * 10 + c
        col = BRICK if n in (44, 55) else "#5a423b"
        g += f'<circle cx="{150+c*24}" cy="{110+r*24}" r="9" fill="{col}"/>'
add("pew", "Pew 2 persen",
    "Survei Pew Research Center tahun 2019 di seratus tiga puluh negara dan wilayah menemukan, hanya sekitar dua persen penduduk dunia yang tinggal di rumah tangga poligami.",
    f'<g class="fadeIn">{g}</g><g transform="translate(258 218)"><g class="beat"><circle r="40" fill="none" stroke="{GOLD}" stroke-width="4"/></g></g>'
    + T(560, 220, 0, "±2%", 110, CREAM, F, cls="fadeIn d1") + T(560, 262, 0, "penduduk dunia", 20, GOLD, M, cls="fadeIn d2")
    + card(460, 330, "Pew Research Center", "2019 · 130 negara &amp; wilayah", -2) + lontar(410, 392, 1.0, "lup", "peek", "d2"), year="2019")

# 09
hb = ""
for k, (lab, v, d) in enumerate([("Burkina Faso", 36, ""), ("Mali", 34, "d1"), ("Nigeria", 28, "d2")]):
    y = 150 + k * 85
    hb += T(250, y + 22, 0, lab, 20, CREAM, M, anchor="end") + f'<rect x="270" y="{y}" width="400" height="34" rx="10" fill="#4a332d"/>'
    hb += f'<rect class="fill {d}" x="270" y="{y}" width="{v/40*400:.0f}" height="34" rx="10" fill="{BRICK}"/>' + T(270 + v / 40 * 400 + 14, y + 26, 0, f"{v}%", 26, GOLD, F, anchor="start", cls=f"fadeIn {d}")
add("sabuk", "Sabuk poligami",
    "Angkanya melonjak di Afrika Barat dan Tengah. Di Burkina Faso tiga puluh enam persen, di Mali tiga puluh empat persen, dan di Nigeria dua puluh delapan persen.",
    T(400, 80, 0, "tinggal di rumah tangga poligami", 18, GOLD, M) + hb + T(400, 384, 0, "Pew Research Center (2019)", 15, MUTED, M), bg=BG2)

# 10
bolt = lambda x, y: f'<g transform="translate({x} {y})"><g class="blink"><path d="M0-30l-14 30h12l-6 30 22-36h-12l8-24z" fill="{GOLD}"/></g></g>'
add("jankowiak", "Konflik antar istri",
    "Apakah berbagi suami membuat semua bahagia? Antropolog William Jankowiak dan timnya mempelajari catatan enam puluh sembilan masyarakat poligami. Konflik antar istri hampir selalu muncul.",
    '<rect y="360" width="800" height="90" fill="#2f201c"/>' + person(400, 210, TEAL, .9, "bob")
    + person(220, 230, BRICK, .9, "shake", skirt=True) + person(580, 230, GOLD, .9, "shake", skirt=True)
    + bolt(300, 170) + bolt(500, 170)
    + T(400, 80, 0, "69 masyarakat poligami", 30, GOLD)
    + card(580, 96, "Ethnology", "Jankowiak dkk. · 2005 · 44:81", -2), year="2005", bg="#22182a")

# 11
add("cemburu", "89 persen",
    "Pemicu yang paling sering disebut adalah berebut perhatian dan kasih sayang suami, dilaporkan di delapan puluh sembilan persen masyarakat itu. Ternyata cemburu ikut pindah rumah.",
    f'<g transform="translate(250 220)"><circle r="110" fill="{BG2}"/><circle class="ring89" r="90" fill="none" stroke="{BRICK}" stroke-width="30" transform="rotate(-90)"/>'
    f'<text y="16" text-anchor="middle" {F} font-size="50" fill="{CREAM}">89%</text></g>'
    + T(570, 170, 0, "berebut perhatian", 30, CREAM, cls="fadeIn d1") + T(570, 210, 0, "&amp; kasih sayang suami", 30, CREAM, cls="fadeIn d1")
    + f'<g transform="translate(570 300)"><g class="zoomIn z2"><rect x="-170" y="-34" width="340" height="60" rx="16" fill="{GOLD}"/>'
    f'<text y="6" text-anchor="middle" {N} font-size="22" fill="{DARK}">cemburu ikut pindah rumah</text></g></g>')

# 12 subscribe
add("subscribe", "Subscribe",
    "Kalau kamu mulai ragu soal apa yang disebut alami, subscribe Kamasastra. Kita bongkar hal yang biasanya cuma dibisikkan, pakai data, tanpa menghakimi.",
    f'<g class="press"><rect x="250" y="170" width="300" height="90" rx="45" fill="{BRICK}"/><text x="400" y="228" text-anchor="middle" {N} font-size="34" fill="{CREAM}">SUBSCRIBE</text></g>'
    f'<g transform="translate(600 150)"><g class="wiggle"><path d="M-20 10a20 20 0 0 1 40 0v14l8 10h-56l8-10z" fill="{GOLD}"/><circle cy="40" r="6" fill="{GOLD}"/></g></g>'
    f'<g transform="translate(520 300)"><g class="click"><path d="M0 0l0 50 12-12 12 24 10-5-12-24 18 0z" fill="{CREAM}"/></g></g>'
    + lontar(205, 330, 1.5, "point", "slideL", "d1"))

# 13 poliandri
add("poliandri", "Poliandri",
    "Kebalikannya, satu istri dengan beberapa suami, disebut poliandri. Atlas tadi cuma mencatat empat masyarakat. Tapi riset tahun 2012 menemukan lima puluh tiga masyarakat lain yang membolehkannya.",
    person(230, 200, GOLD, .85, "bob", skirt=True) + person(110, 230, TEAL, .6, "bob", "b2") + person(350, 230, SKY, .6, "bob", "b3")
    + f'<g transform="translate(520 170)"><g class="pop d1"><text text-anchor="middle" {F} font-size="64" fill="{MUTED}">4</text></g></g>'
    + f'<path class="strike" d="M480 150 L560 150" stroke="{BRICK}" stroke-width="8" stroke-linecap="round"/>'
    + f'<g transform="translate(640 200)"><g class="zoomIn z2"><circle r="70" fill="{BRICK}"/><text y="22" text-anchor="middle" {F} font-size="64" fill="{CREAM}">53</text></g></g>'
    + T(520, 210, 0, "Atlas", 16, MUTED, M) + T(640, 300, 0, "di luar Himalaya", 16, GOLD, M)
    + card(40, 66, "Human Nature", "Starkweather &amp; Hames · 2012", 2), year="2012", bg=BG2)

# 14 himba intro
hut = lambda x, s: f'<g transform="translate({x} 330) scale({s})"><path d="M-50 0a50 46 0 0 1 100 0z" fill="#a0704a"/><rect x="-12" y="-26" width="24" height="26" rx="10" fill="#3a2723"/></g>'
cow = lambda x, cls: f'<g transform="translate({x} 345)"><g class="bob {cls}"><ellipse rx="34" ry="18" fill="#6e4d36"/><circle cx="34" cy="-10" r="12" fill="#6e4d36"/><path d="M28-20q-6-14 6-14M40-20q6-14 18-12" stroke="{CREAM}" stroke-width="3" fill="none"/></g></g>'
add("himba", "Himba",
    "Sekarang ke Namibia. Tahun 2020, antropolog Brooke Scelza dan timnya meneliti DNA ayah dan anak di komunitas Himba, dengan cara yang dirancang bersama warga.",
    '<rect width="800" height="300" fill="#d9a441" opacity=".25"/><circle cx="710" cy="90" r="40" fill="#d9a441"/><rect y="320" width="800" height="130" fill="#6e4d36" opacity=".6"/>'
    + hut(140, 1) + hut(250, .8) + cow(380, "") + cow(470, "b2")
    + f'<g transform="translate(580 240)"><g class="helix"><path d="M-20-80c40 27-40 53 0 80s-40 53 0 80M20-80c-40 27 40 53 0 80s40 53 0 80" stroke="{BRICK}" stroke-width="7" fill="none"/></g></g>'
    + T(400, 80, 0, "DNA ayah &amp; anak", 34, CREAM) + lontar(720, 360, 1.2, "wave", "pop", "d2"), year="2020 · Namibia", bg="#3a2723")

# 15 48%
add("himba48", "48 persen",
    "Hasilnya: empat puluh delapan persen anak ternyata bukan anak biologis suami ibunya. Studi genetik terbaik di masyarakat lain biasanya hanya menemukan satu sampai tiga persen.",
    f'<g transform="translate(240 215)"><circle r="120" fill="{BG2}"/><path class="pieHalf" d="M0 0 L0 -120 A120 120 0 0 1 -15 119 Z" fill="{BRICK}"/>'
    f'<text x="56" y="14" text-anchor="middle" {F} font-size="40" fill="{CREAM}">48%</text></g>'
    + T(570, 120, 0, "Himba", 22, CREAM, M) + f'<rect x="440" y="134" width="260" height="34" rx="10" fill="#4a332d"/><rect class="fill" x="440" y="134" width="250" height="34" rx="10" fill="{BRICK}"/>'
    + T(570, 220, 0, "masyarakat lain", 22, CREAM, M) + f'<rect x="440" y="234" width="260" height="34" rx="10" fill="#4a332d"/><rect class="fill d2" x="440" y="234" width="16" height="34" rx="6" fill="{TEAL}"/>'
    + T(476, 260, 0, "1–3%", 24, GOLD, F, anchor="start", cls="fadeIn d2")
    + card(470, 330, "Science Advances", "Scelza dkk. · 2020 · 6:eaay6195", -2))

# 16 ayah sosial
add("ayahsosial", "Ayah sosial",
    "Yang lebih mengejutkan, suami dan istri Himba umumnya tahu. Bagi mereka, anak yang lahir dari istrimu adalah anakmu, siapa pun ayah biologisnya.",
    '<rect y="360" width="800" height="90" fill="#2f201c"/>' + person(300, 190, TEAL, 1.05, "sway") + child(380, 270, GOLD)
    + heart(345, 150, 1)
    + f'<g transform="translate(590 210)"><g class="stampIn"><rect x="-150" y="-46" width="300" height="92" rx="10" fill="none" stroke="{BRICK}" stroke-width="8"/>'
    f'<text y="-6" text-anchor="middle" {M} font-weight="700" font-size="30" fill="{BRICK}">AYAH</text><text y="30" text-anchor="middle" {M} font-weight="700" font-size="30" fill="{BRICK}">SOSIAL</text></g></g>'
    + T(400, 70, 0, "“anak istrimu = anakmu”", 30, GOLD, cls="fadeIn d1"), bg=BG2)

# 17 amazon
tree = lambda x, s, cls: f'<g transform="translate({x} 360) scale({s})"><g class="sway {cls}"><rect x="-8" y="-120" width="16" height="120" fill="#6e4d36"/><circle cy="-140" r="50" fill="#2c8580"/><circle cx="-34" cy="-110" r="34" fill="{TEAL}"/><circle cx="34" cy="-110" r="34" fill="{TEAL}"/></g></g>'
add("amazon", "Amazon",
    "Di hutan Amazon, enam puluh satu masyarakat tercatat percaya seorang anak bisa punya lebih dari satu ayah biologis. Ilmuwan menyebutnya partible paternity, ayah yang bisa dibagi.",
    '<rect width="800" height="450" fill="#1d3a33"/><rect y="350" width="800" height="100" fill="#2f201c"/>'
    + tree(90, 1, "") + tree(720, 1.1, "b2")
    + person(300, 200, TEAL, .9, "bob") + person(500, 200, SKY, .9, "bob", "b3") + child(400, 270, GOLD)
    + heart(400, 160, .8)
    + T(400, 70, 0, "partible paternity", 34, GOLD) + T(400, 104, 0, "61 masyarakat Amazon", 18, CREAM, M, cls="fadeIn d2") + lontar(615, 392, 1.0, "lup", "peek", "d3"), year="Amazon")

# 18 bari
fish = lambda d: f'<g class="flyIn {d}"><path d="M0 0q20-16 40 0q-20 16-40 0zM40 0l14-10v20z" fill="{SKY}"/></g>'
add("bari", "Bari",
    "Pada suku Bari di Venezuela, Stephen Beckerman menemukan anak yang punya ayah kedua lebih sering bertahan hidup. Sang ayah kedua wajib mengirim ikan dan hasil buruan.",
    '<rect y="360" width="800" height="90" fill="#2f201c"/>' + person(180, 200, TEAL, .9, "bob") + child(330, 270, GOLD) + person(560, 200, SKY, .9, "bob", "b3")
    + f'<g transform="translate(430 230)">{fish("d1")}</g><g transform="translate(450 280)">{fish("d2")}</g>'
    + T(180, 384, 0, "ayah", 16, CREAM, M) + T(560, 384, 0, "ayah kedua", 16, CREAM, M)
    + T(400, 80, 0, "lebih sering bertahan hidup", 30, GOLD)
    + card(560, 110, "Current Anthropology", "Beckerman dkk. · 1998 · 39:164", 2), year="1998 · Venezuela", bg="#22182a")

# 19 mosuo
add("mosuo", "Pernikahan berjalan",
    "Di tepi Danau Lugu, Tiongkok, suku Mosuo mengenal pernikahan berjalan. Laki-laki mengunjungi kekasihnya pada malam hari, lalu pulang ke rumah ibunya sebelum fajar.",
    '<rect width="800" height="450" fill="#1b2340"/>'
    + f'<g class="blink"><circle cx="120" cy="70" r="3" fill="{CREAM}"/><circle cx="300" cy="50" r="2" fill="{CREAM}"/><circle cx="470" cy="80" r="3" fill="{CREAM}"/></g>'
    + f'<circle cx="650" cy="80" r="34" fill="{CREAM}"/><path d="M0 260l140-110 120 80 150-120 170 120 220-60v140H0z" fill="#2c3a5a"/>'
    + f'<rect y="300" width="800" height="150" fill="#2d5f6e"/><path d="M60 330h120M300 360h160M560 340h120" stroke="{SKY}" stroke-width="3" opacity=".6"/>'
    + f'<g transform="translate(160 300)"><path d="M-60 0v-70l60-44 60 44v70z" fill="#a0704a"/><rect x="-14" y="-40" width="28" height="40" fill="{GOLD}" class="glow"/></g>'
    + f'<g transform="translate(640 300)"><path d="M-60 0v-70l60-44 60 44v70z" fill="#a0704a"/><rect x="-14" y="-40" width="28" height="40" fill="{GOLD}"/></g>'
    + f'<g transform="translate(300 250)"><g class="runX"><g transform="scale(.42)"><circle r="32" fill="{CREAM}"/><rect x="-32" y="36" width="64" height="104" rx="26" fill="{TEAL}"/></g></g></g>'
    + T(160, 330, 0, "rumah kekasih", 15, CREAM, M) + T(640, 330, 0, "rumah ibunya", 15, CREAM, M), year="Danau Lugu · Tiongkok")

# 20 mosuo keluarga
add("mosuo2", "Rumah keluarga ibu",
    "Anak dibesarkan keluarga ibu, dan paman ikut berperan seperti ayah. Tapi ini bukan bebas tanpa aturan. Kebanyakan tetap berpasangan satu, dan tradisinya kini ikut berubah karena pariwisata.",
    f'<path d="M110 360v-180l180-110 180 110v180z" fill="#a0704a"/>'
    + person(165, 230, BRICK, .62, "bob", skirt=True) + person(255, 230, GOLD, .62, "bob", "b2", skirt=True) + child(320, 278, SKY) + person(410, 230, TEAL, .62, "bob", "b3")
    + T(165, 382, 0, "nenek", 14, CREAM, M) + T(285, 382, 0, "ibu &amp; anak", 14, CREAM, M) + T(410, 382, 0, "paman", 14, CREAM, M)
    + f'<g transform="translate(620 170)"><g class="pop d2"><rect x="-120" y="-40" width="240" height="80" rx="16" fill="{TEAL}"/><text y="10" text-anchor="middle" {N} font-size="22" fill="{DARK}">umumnya 1 pasangan</text></g></g>'
    + f'<g transform="translate(620 290)"><g class="pop d3"><rect x="-50" y="-30" width="100" height="64" rx="10" fill="{CREAM}"/><circle cy="2" r="20" fill="{BG2}"/><circle cy="2" r="10" fill="{SKY}"/><rect x="20" y="-40" width="24" height="12" rx="3" fill="{CREAM}"/></g></g>'
    + T(620, 360, 0, "berubah karena pariwisata", 16, GOLD, M, cls="fadeIn d3"), bg=BG2)

# 21 indonesia
add("indonesia", "UU Perkawinan",
    "Lalu kita? Undang-Undang Perkawinan tahun 1974 menganut asas monogami: satu suami, satu istri. Poligami hanya lewat izin pengadilan, dengan syarat ketat, termasuk persetujuan istri.",
    f'<g transform="translate(230 225)"><g class="sway"><rect x="-120" y="-150" width="240" height="290" rx="8" fill="{CREAM}"/><rect x="-120" y="-150" width="240" height="44" rx="8" fill="{BRICK}"/>'
    f'<text y="-120" text-anchor="middle" {M} font-size="18" fill="{CREAM}">UU No. 1/1974</text><text y="-70" text-anchor="middle" {F} font-size="26" fill="{DARK}">Perkawinan</text>'
    f'<path d="M-90-30h180M-90 0h180M-90 30h140M-90 60h170" stroke="{MUTED}" stroke-width="5"/></g></g>'
    + f'<g transform="translate(230 285)"><g class="stampIn"><rect x="-110" y="-30" width="220" height="60" rx="8" fill="none" stroke="{TEAL}" stroke-width="7"/><text y="10" text-anchor="middle" {M} font-weight="700" font-size="22" fill="{TEAL}">ASAS MONOGAMI</text></g></g>'
    + "".join(f'<g transform="translate(470 {y})"><g class="pop {d}"><circle r="20" fill="{GOLD}"/><path d="M-9 0l6 7 12-14" stroke="{DARK}" stroke-width="4" fill="none"/></g></g>'
              + T(504, y + 8, 0, t, 20, CREAM, N, anchor="start", cls=f"fadeIn {d}") for y, t, d in [(150, "izin pengadilan", "d2"), (220, "syarat ketat", "d3"), (290, "persetujuan istri", "d4")]) + lontar(740, 392, 1.1, "none", "peek", "d4"),
    year="1974 · Indonesia")

# 22 kodrat
add("kodrat", "Kodrat?",
    "Jadi, apa kodrat manusia? Banyak antropolog menyebut kita monogami dengan kecenderungan poligini ringan. Kita mampu berpasangan erat, tapi budayalah yang menulis aturannya.",
    f'<path d="M180 300a220 220 0 0 1 440 0" fill="none" stroke="#4a332d" stroke-width="40"/>'
    f'<path d="M180 300a220 220 0 0 1 110-190" fill="none" stroke="{TEAL}" stroke-width="40"/><path d="M510 110a220 220 0 0 1 110 190" fill="none" stroke="{BRICK}" stroke-width="40"/>'
    f'<g class="needle"><path d="M400 300L396 120h8z" fill="{CREAM}"/></g><circle cx="400" cy="300" r="16" fill="{GOLD}"/>'
    + T(180, 345, 0, "monogami", 18, TEAL, M) + T(620, 345, 0, "banyak pasangan", 18, BRICK, M)
    + f'<g transform="translate(400 384)"><g class="zoomIn z2"><text text-anchor="middle" {F} font-size="30" fill="{GOLD}">“monogami, sedikit poligini”</text></g></g>' + lontar(75, 392, 1.0, "point", "peek", "d3"), bg=BG2)

# 23 pola
pts = [(200, 330), (270, 300), (340, 310), (410, 250), (480, 230), (550, 180), (620, 160)]
dots = "".join(f'<circle class="pop d{min(5,k//2+1)}" cx="{x}" cy="{y}" r="10" fill="{GOLD}"/>' for k, (x, y) in enumerate(pts))
add("pola", "Pola cemburu",
    "Satu pola lagi. Studi Scelza di sebelas populasi menemukan, makin besar peran ayah mengasuh anak, makin keras reaksi cemburu pada perselingkuhan. Aturan setia ikut mengikuti siapa yang menanggung anak.",
    f'<path d="M160 360H660M160 360V110" stroke="{MUTED}" stroke-width="3"/>'
    f'<path class="ecg" d="M190 340L640 150" stroke="{BRICK}" stroke-width="6" fill="none"/>' + dots
    + T(410, 386, 0, "peran ayah mengasuh →", 16, CREAM, M) + f'<text x="140" y="240" text-anchor="middle" {M} font-size="16" fill="{CREAM}" transform="rotate(-90 140 240)">reaksi cemburu →</text>'
    + T(400, 70, 0, "11 populasi · 1.048 orang", 22, GOLD, M)
    + card(180, 100, "Nature Human Behaviour", "Scelza dkk. · 2020 · 4:20", 2), year="2020")

# 24 dimas sari 2
add("kesepakatan", "Kesepakatan",
    "Jadi Dimas dan Sari sama-sama separuh benar. Manusia memang lentur. Justru karena itu, setia bukan takdir, melainkan kesepakatan yang dipilih dan dijaga berdua.",
    '<circle cx="660" cy="90" r="40" fill="#d9a441" opacity=".85"/><rect y="360" width="800" height="90" fill="#2f201c"/>'
    + person(250, 230, TEAL, 1, "bob") + person(550, 230, GOLD, 1, "bob", "b2", skirt=True) + heart(400, 210, 1.3)
    + f'<g transform="translate(400 110)"><g class="zoomIn z2"><rect x="-200" y="-40" width="400" height="70" rx="18" fill="{CREAM}"/><text y="8" text-anchor="middle" {F} font-size="30" fill="{DARK}">setia = kesepakatan</text></g></g>',
    year="Ilustrasi", bg="#22182a")

# 25 catatan
add("catatan", "Catatan",
    "Catatan jujur: data atlas berasal dari catatan etnografi lama, dan tiap budaya terus berubah. Membandingkan budaya bukan untuk menilai mana yang lebih baik, tapi untuk memahami.",
    f'<rect x="170" y="90" width="380" height="290" rx="10" fill="{CREAM}"/>'
    + T(200, 160, 0, "• catatan etnografi lama", 19, DARK, M, anchor="start", cls="fadeIn d1")
    + T(200, 220, 0, "• budaya terus berubah", 19, DARK, M, anchor="start", cls="fadeIn d2")
    + T(200, 280, 0, "• bukan untuk menilai", 19, DARK, M, anchor="start", cls="fadeIn d3")
    + T(200, 340, 0, "tujuannya: memahami", 19, BRICK, M, anchor="start", cls="fadeIn d4")
    + lontar(650, 370, 2.0, "lup", "peek", "d1"),
    year="Catatan", bg=BG2)

# 26 pustaka
refs = [
    ("Murdock (1967); Gray (1998)", "Ethnographic Atlas · codebook", "World Cultures, 10(1), 86–136"),
    ("Pew Research Center (2019)", "Religion and Living Arrangements Around the World", "pewresearch.org · 130 negara"),
    ("Jankowiak, Sudakov &amp; Wilreker (2005)", "Co-wife conflict and co-operation", "Ethnology, 44(1), 81–98"),
    ("Starkweather &amp; Hames (2012)", "A survey of non-classical polyandry", "Human Nature, 23(2), 149–172"),
    ("Scelza dkk. (2020)", "High rate of extrapair paternity in a human population", "Science Advances, 6(8) · doi:10.1126/sciadv.aay6195"),
    ("Scelza dkk. (2020)", "Patterns of paternal investment predict … jealous response", "Nature Human Behaviour, 4, 20–26"),
    ("Beckerman dkk. (1998); Walker dkk. (2015)", "Barí partible paternity · co-fathers (Suruí)", "Current Anthropology 39:164 · PeerJ 3:e899"),
    ("UU No. 1 Tahun 1974 · Shih (2010)", "Tentang Perkawinan · Quest for Harmony (Mosuo)", "Pasal 3–5 · Stanford University Press"),
]
pk = T(400, 40, 0, "DAFTAR PUSTAKA", 20, GOLD, M).replace('font-size="20"', 'font-size="20" letter-spacing="6"')
for k, (a, t, j) in enumerate(refs):
    x = 38 + (k % 2) * 372; y = 54 + (k // 2) * 76; d = f"d{min(8, k+1)}"
    pk += (f'<g transform="translate({x} {y})"><g class="fadeIn {d}"><rect width="352" height="70" rx="4" fill="{CREAM}"/><rect width="6" height="70" fill="{BRICK}"/>'
           f'<text x="18" y="22" {N} font-size="12.5" fill="{DARK}">{a}</text>'
           f'<text x="18" y="42" font-family="Fraunces,serif" font-style="italic" font-weight="600" font-size="12.5" fill="{DARK}">{t}</text>'
           f'<text x="18" y="58" {M} font-size="10" fill="#5a423b">{j}</text></g></g>')
pk += T(400, 370, 0, "Cek sendiri · tautan lengkap di deskripsi ↓", 15, GOLD, M, cls="fadeIn d8")
add("pustaka", "Daftar pustaka",
    "Semua sumber video ini ada di layar dan di deskripsi. Jangan langsung percaya, termasuk pada daun lontar tua sepertiku. Cek sendiri.", pk)

# 27 komentar
add("komentar", "Komentar",
    "Pertanyaan untukmu: menurutmu setia itu bawaan manusia, atau kesepakatan budaya? Jawab jujur di kolom komentar.",
    T(400, 100, 0, "Setia itu…", 40, CREAM)
    + f'<g class="pop d1"><rect x="150" y="150" width="220" height="110" rx="20" fill="{TEAL}"/><text x="260" y="218" text-anchor="middle" {F} font-size="36" fill="{DARK}">KODRAT</text></g>'
    + f'<g class="pop d2"><rect x="430" y="150" width="220" height="110" rx="20" fill="{BRICK}"/><text x="540" y="218" text-anchor="middle" {F} font-size="36" fill="{CREAM}">BUDAYA</text></g>'
    + f'<g transform="translate(400 330)"><g class="wiggle"><text text-anchor="middle" {M} font-size="22" fill="{GOLD}">jawab di komentar 👇</text></g></g>' + lontar(710, 395, 1.2, "sign", "peek", "d3", sign="?"))

# 28 penutup
add("penutup", "Penutup",
    "Kalau setia itu kesepakatan, apa yang membuat sebuah pernikahan bertahan puluhan tahun? Kita bongkar di video berikutnya. Sampai jumpa, dari Si Lontar!",
    T(400, 96, 0, "BERIKUTNYA", 20, GOLD, M).replace('font-size="20"', 'font-size="20" letter-spacing="6"')
    + T(400, 186, 0, "Rahasia pernikahan", 46, CREAM, cls="fadeIn d1")
    + f'<g transform="translate(400 272)"><g class="zoomIn z2"><text text-anchor="middle" {F} font-size="72" fill="{BRICK}">AWET?</text></g></g>'
    + ring(170, 350, GOLD, "") + ring(206, 370, CREAM, "w2") + ring(600, 350, GOLD, "w2") + ring(636, 370, CREAM, "") + lontar(400, 396, 1.0, "wave", "pop", "d3"))

open("/home/claude/kamasastra/setia/scenes.html", "w").write("\n".join(S))
for s in S:
    import re
    t = html.unescape(re.search(r'data-text="([^"]*)"', s).group(1)); print(len(t), re.search(r'data-id="([^"]*)"', s).group(1))
