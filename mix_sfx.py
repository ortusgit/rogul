"""Tambah efek suara + musik latar ke MP4 Kamasastra yang sudah bersuara.
Pemakaian: python3 mix_sfx.py rec_name delta page.html in.mp4 out.mp4
Waktu adegan diambil dari log render (rec/<name>.json), sama seperti mux.py.
"""
import json, re, subprocess, sys

name, delta, page, src, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
import os
SFX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx', 'norm') + '/'
GAIN = {'whoosh': -15, 'pop': -15, 'stamp': -11, 'click': -13, 'heartbeat': -12, 'alarm': -17,
        'phone': -13, 'ding': -15, 'paper': -12}
# isyarat per adegan: (detik setelah adegan mulai, efek)
CUES = {
    'judul': [(0.3, 'ding')],
    'monyet': [(0.15, 'paper'), (0.8, 'heartbeat'), (2.0, 'paper')],
    'dimas': [(0.15, 'paper'), (0.8, 'phone'), (3.2, 'heartbeat')],
    'peta': [(0.4, 'pop'), (1.2, 'pop'), (2.0, 'pop')],
    'definisi': [(1.2, 'pop')],
    'othello': [(0.15, 'paper')],
    'buss': [(0.15, 'paper'), (2.0, 'paper')],
    'hasil': [(0.1, 'pop'), (1.3, 'pop')],
    'jantung': [(0.3, 'heartbeat')],
    'evolusi': [(1.2, 'pop')],
    'subscribe': [(1.1, 'click'), (1.3, 'ding')],
    'bantahan': [(1.9, 'stamp'), (2.2, 'paper')],
    'kuis': [(0.4, 'pop'), (1.2, 'pop')],
    'takahashi': [(0.15, 'paper'), (2.0, 'paper')],
    'otakbeda': [(0.5, 'ding')],
    'titi': [(0.15, 'paper'), (0.8, 'heartbeat'), (2.0, 'paper')],
    'hormon': [(0.1, 'pop'), (1.3, 'pop')],
    'alarm': [(0.15, 'paper'), (0.6, 'alarm')],
    'kemungkinan': [(0.15, 'paper'), (0.6, 'phone')],
    'sehat': [(0.4, 'ding'), (1.2, 'click'), (2.0, 'click'), (2.8, 'click')],
    'bahaya': [(0.1, 'pop')],
    'dimas2': [(0.15, 'paper'), (1.0, 'ding')],
    'jawaban': [(1.3, 'stamp')],
    'catatan': [(0.2, 'paper')],
    'pustaka': [(0.4, 'paper'), (1.2, 'paper'), (2.0, 'paper'), (2.8, 'paper'), (3.6, 'paper')],
    'komentar': [(0.4, 'pop'), (1.2, 'pop')],
    'penutup': [(0.3, 'ding')],
    'CTA': [(0.3, 'ding')],
}

if len(sys.argv) > 6:
    CUES.update({k: [tuple(x) for x in v] for k, v in json.load(open(sys.argv[6])).items()})
d = json.load(open(f'rec/{name}.json'))
origin = d['click_wall'] - d['nav'] / 1000 + delta
starts = {}
for x in d['log']:
    if x['e'] == 'playing' and x['i'] not in starts:
        starts[x['i']] = origin + x['t'] / 1000
cut0 = max(0, starts[0] - 0.6)
ids = re.findall(r'class="scene[^"]*"[^>]*?data-id="([^"]+)"', open(page).read())
assert len(ids) == len(starts), (len(ids), len(starts))
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]))

events = []
for i, sid in enumerate(ids):
    t0 = starts[i] - cut0 - 0.05          # adegan aktif sesaat sebelum suara mulai
    if i > 0:
        events.append((t0 - 0.35, 'whoosh'))
    for off, s in CUES.get(sid, []):
        events.append((t0 + off, s))
events = [(t, s) for t, s in events if 0 <= t < dur - 0.5]

inputs = ['-i', src, '-i', SFX + 'musik-loop.mp3']
filt = ['[0:a]aformat=channel_layouts=stereo,aresample=44100,asplit=2[voice][sc]',
        f'[1:a]atrim=0:{dur:.2f},volume=-21dB,afade=t=in:d=2,afade=t=out:st={dur-3:.2f}:d=3[mus]',
        '[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=400[duck]']
labels = []
for k, (t, s) in enumerate(events):
    inputs += ['-i', SFX + s + '.wav']
    ms = int(t * 1000)
    filt.append(f'[{k+2}:a]volume={GAIN[s]}dB,adelay={ms}|{ms}[e{k}]')
    labels.append(f'[e{k}]')
filt.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0[sfx]')
filt.append('[voice][sfx][duck]amix=inputs=3:normalize=0,volume=8dB,alimiter=limit=0.89:level=disabled[aout]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(filt),
                '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-t', f'{dur:.3f}', '-movflags', '+faststart', out], check=True)
print(out, len(events), 'efek suara')
