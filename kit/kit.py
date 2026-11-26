"""Kit grafis Kamasastra (dipakai gen_scenes.py tiap video).
ATURAN TATA LETAK: adegan digambar di viewBox 800x380. Area 380-450 tidak ada; 15% bawah layar = pita subtitle.
Grafis utama tetap di y 20-360. Si Lontar tampil sebagai CAMEO di dalam adegan (tidak ada narator di pojok).
"""
import html
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

def scene(num, sid, title, text, body, year=None, bg=BG1, tr='pan'):
    y = f'\n      <div class="year">{year}</div>' if year else ""
    return (f'    <!-- {num:02d} {title} -->\n    <div class="scene" data-id="{sid}" data-tr="{tr}" data-text="{html.escape(text, quote=True)}">{y}\n'
            f'      <svg viewBox="0 0 800 450">\n        <rect width="800" height="380" fill="{bg}"/>\n        {body}\n      </svg>\n    </div>\n')


# ---------- Si Lontar ----------
def lontar_svg(mouth_cls="lmouth"):
    """Si Lontar utuh (viewBox asli 74x92)."""
    return ('<line x1="30" y1="80" x2="28" y2="90" stroke="#d9b77a" stroke-width="4" stroke-linecap="round"/>'
            '<line x1="44" y1="80" x2="46" y2="90" stroke="#d9b77a" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M52 10c10-6 18 2 14 10" stroke="#b5523b" stroke-width="3" fill="none"/>'
            '<rect x="20" y="4" width="34" height="78" rx="12" fill="#d9b77a" stroke="#a8834a" stroke-width="2"/>'
            '<circle cx="37" cy="12" r="3" fill="#3a2723"/>'
            '<g stroke="#a8834a" stroke-width="1.5"><line x1="25" y1="64" x2="49" y2="64"/><line x1="25" y1="70" x2="49" y2="70"/><line x1="25" y1="76" x2="45" y2="76"/></g>'
            '<g class="eyes"><circle cx="30" cy="36" r="4.5" fill="#2f201c"/><circle cx="44" cy="36" r="4.5" fill="#2f201c"/>'
            '<circle cx="31.5" cy="34.5" r="1.5" fill="#fff"/><circle cx="45.5" cy="34.5" r="1.5" fill="#fff"/></g>'
            '<circle cx="25" cy="45" r="3.5" fill="#b5523b" opacity=".5"/><circle cx="49" cy="45" r="3.5" fill="#b5523b" opacity=".5"/>'
            f'<ellipse class="{mouth_cls}" cx="37" cy="54" rx="6" ry="4.5" fill="#b5523b"/>')

PROPS = {
    "none": "",
    "wave": '<g transform="translate(54 40)"><g class="wave"><path d="M0 0 l16 -18" stroke="#a8834a" stroke-width="4" stroke-linecap="round"/><circle cx="17" cy="-19" r="4" fill="#d9b77a"/></g></g>',
    "lup": '<g transform="translate(54 44)"><path d="M0 0 l10 -6" stroke="#a8834a" stroke-width="4" stroke-linecap="round"/><circle cx="20" cy="-14" r="11" fill="#8ecae6" fill-opacity=".35" stroke="#d9a441" stroke-width="4"/></g>',
    "point": '<g transform="translate(54 44)"><path d="M0 0 l22 -4" stroke="#a8834a" stroke-width="4" stroke-linecap="round"/><path d="M22-4l-6-5m6 5l-6 5" stroke="#a8834a" stroke-width="3" stroke-linecap="round"/></g>',
    "sign": '<g transform="translate(54 30)"><path d="M0 14 l8 -4" stroke="#a8834a" stroke-width="4" stroke-linecap="round"/><rect x="6" y="-30" width="56" height="34" rx="4" fill="#f4ecd8" stroke="#a8834a" stroke-width="2"/><text x="34" y="-7" text-anchor="middle" font-family="Fraunces,serif" font-weight="800" font-size="20" fill="#b5523b">{sign}</text></g>',
}

def lontar(x, y, s=1.0, pose="none", enter="peek", d="d1", flip=False, sign="?"):
    """Cameo Si Lontar. (x,y) = titik kaki. enter: peek|pop|slideL|slideR|none. pose: none|wave|lup|point|sign."""
    prop = PROPS[pose].replace("{sign}", sign)
    fx = "scale(-1 1)" if flip else ""
    cls = f"{enter} {d}" if enter != "none" else ""
    return (f'<g transform="translate({x} {y}) scale({s})"><g class="{cls}"><g transform="{fx}"><g transform="translate(-37 -92)"><g class="lbody">'
            f'{lontar_svg()}{prop}</g></g></g></g></g>')

def subscribe_scene(text):
    """Adegan ajakan subscribe (tanpa ikon mata), Si Lontar menekan tombol."""
    return ('subscribe', 'Subscribe', text,
            f'<g class="press"><rect x="250" y="140" width="300" height="90" rx="45" fill="{BRICK}"/><text x="400" y="198" text-anchor="middle" {N} font-size="34" fill="{CREAM}">SUBSCRIBE</text></g>'
            f'<g transform="translate(600 120)"><g class="wiggle"><path d="M-20 10a20 20 0 0 1 40 0v14l8 10h-56l8-10z" fill="{GOLD}"/><circle cy="40" r="6" fill="{GOLD}"/></g></g>'
            + lontar(210, 330, 1.5, "point", "slideL", "d1"))
