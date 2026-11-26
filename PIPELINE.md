# Runbook produksi harian Kamasastra

Channel YouTube **Kamasastra** (@kamasastra, UC_3tCCl9uWB8O5Ed1YnOtow): edukasi seks, relasi, budaya dan sains, berbahasa Indonesia.
Tagline: "Tabu dibahas, bukan dibuka." Narator/maskot: **Si Lontar** (daun lontar).
Kesepakatan (26 Nov 2026): **1 Short setiap hari** (±40–55 detik, 9:16) dan **video panjang Selasa, Kamis, Sabtu** (±5 menit, boleh 6–7 menit untuk topik besar, 16:9).

## 0. Persiapan sesi
```bash
git clone --depth 1 https://github.com/ortusgit/rogul /home/claude/rogul
ln -sfn /home/claude/rogul /home/claude/kamasastra      # skrip lama memakai path ini
cd /home/claude/rogul && mkdir -p rec
```
Baca `CALENDAR.md` (topik hari ini) dan `claude/panduan-produksi-kamasastra.md` di project "Konten Youtube".

## 1. Riset & naskah
- Cari web dulu untuk setiap angka/klaim; utamakan jurnal, lembaga resmi. Tulis "studi lanjutan", "diklaim", dsb. bila perlu.
- Video panjang: 22–28 adegan, narasi 100–220 karakter per adegan; ada adegan kartu sumber, subscribe (tanpa ikon mata), catatan jujur, daftar pustaka, pertanyaan komentar, penutup + teaser.
- Short: 5–6 adegan, total < 55 detik, adegan terakhir CTA.
- Tahun ditulis dengan kata di prompt TTS ("dua ribu dua puluh").
- Nada judul/caption provokatif tapi akurat; tidak vulgar; tanpa foto orang sungguhan.

## 2. Adegan (folder topik, mis. `topik-06/`)
- Salin pola dari `examples/setia/gen_scenes.py` (video) dan `examples/short5/gen.py` (Short). Helper di `kit/kit.py`.
- Area grafis **800×380** (subtitle punya pita sendiri di bawah). Untuk Short isi penting di x 75–725.
- Si Lontar cameo di ±1/3 adegan: `lontar(x, y, skala, pose, masuk, delay)`; pose none|wave|lup|point|sign.
- Transisi per adegan lewat `tr=` (pan|zoom|rise|iris|travel).
- Cek visual: `python3 ../kit/anim_page.py test.html "t" --noaudio` (+ `--short --src=...` untuk Short) lalu screenshot.

## 3. Suara (ElevenLabs)
- `creative_generate_speech`: voice_id `zjmMdjff4JG35O3EQJBV` (Mona), model `eleven_multilingual_v2`, `generations_count` 1. **Jangan pernah mengulang panggilan** (tiap panggilan = kredit).
- Ambil URL lewat `creative_get_generations`, unduh dengan curl ke `audio/adegan-NN.mp3` / `audio/short-NN.mp3`.
- Kebutuhan kredit: video ±4.800, Short ±600. Cek `account_get_usage` dulu; kalau tidak cukup, buat lebih pendek dan kabari pemilik.

## 4. Render (satu render pada satu waktu)
```bash
# video
python3 ../kit/anim_page.py page.html "Judul" ; ln -sfn ../rec rec
cd .. && python3 render.py topik/page.html 1920 1090 "#x{}" NAMA
# Short
python3 ../kit/anim_page.py short.html "Judul" --short --src=scenes-short.html '--head=<div id="top"><div class="brand">KAMASASTRA</div><h1>Judul Short</h1></div>'
cd .. && python3 render.py topik/short.html 1080 1930 "#x{}" NAMA
# kalibrasi per adegan -> deltas.json, lalu mux + SFX
python3 -c "import subprocess,json;ds=[float(subprocess.check_output(['python3','calib_mk.py','NAMA',str(i)]).decode()) for i in range(1,N)];json.dump([ds[0]]+ds,open('topik/deltas.json','w'));print(sum(ds)/len(ds))"
cd topik && DELTAS=deltas.json CROP=crop=1920:1080:0:10 python3 ../mux.py NAMA adegan vo.mp4 RATA2   # Short: CROP=crop=1080:1920:0:10, prefix short
cd .. && python3 mix_sfx.py NAMA RATA2 topik/page.html topik/vo.mp4 topik/FINAL.mp4 topik/cues.json
```
Target −14 s/d −15 LUFS. Cek beberapa frame sebelum lanjut.

## 5. Thumbnail (video panjang saja)
`python3 kit/thumb.py thumb.jpg "ANGKA/KATA" "baris atas" "label bawah" "#b5523b" "?"`

## 6. Upload (vidIQ, gratis, maks 3 upload YouTube/hari)
1. Taruh file di branch **media** (orphan, di-force-push; hanya berisi file hari itu):
   ```bash
   cd /tmp && rm -rf m && git clone --depth 1 -b media https://github.com/ortusgit/rogul m || (mkdir m && cd m && git init -q && git checkout -q --orphan media)
   # salin MP4/JPG ke /tmp/m/, lalu:
   cd /tmp/m && git checkout -q --orphan tmp && git add -A && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "media $(date +%F)" && git branch -D media 2>/dev/null; git branch -m media && git push -f origin media
   ```
   URL: `https://raw.githubusercontent.com/ortusgit/rogul/media/<file>`
2. `vidiq_video_upload {url}` → uploadId; thumbnail: `vidiq_upload_image` → imageId.
3. `vidiq_social_post_draft_create`: platformAccountId `UC_3tCCl9uWB8O5Ed1YnOtow`, privacyStatus `public`, categoryId 27, title, text (deskripsi), tags, thumbnailImageId (video), publishAt.
4. **Tunjukkan semua draf ke pemilik dan tunggu "ya"** sebelum `vidiq_social_post_publish`. Jangan publish tanpa persetujuan di sesi itu.
5. Cek `vidiq_social_post_status`, bagikan link. Ingatkan: "Dibuat untuk anak-anak = Tidak", "konten sintetis = Tidak" (default upload di Studio).

## Jadwal tayang (WIB)
- Video **17.00** (Sel, Kam, Sab) · Short **20.00** (setiap hari). Sesuaikan bila data vidIQ menunjukkan jam lain lebih baik.

## Anggaran kualitas (sisa kredit ElevenLabs)
Kebutuhan dasar ±18.600 kredit/minggu (3 video × 4.800 + 7 Short × 600); paket Creator 121.752/bulan. Sisanya dipakai untuk kualitas, **selalu sisakan cadangan ≥ 10.000** dan hitung dulu kebutuhan sampai tanggal reset:
1. **Musik latar khusus per video panjang** (±900 kredit, model musik ElevenLabs; instrumental, tenang, sesuai suasana topik) → simpan juga ke `sfx/norm/` bila bagus untuk dipakai ulang. Short boleh memakai `musik-loop.mp3`.
2. **Efek suara baru** yang pas dengan adegan (±17 kredit/efek, maks ±10 per video) → normalisasi lalu simpan di `sfx/norm/` dan commit agar bisa dipakai ulang.
3. **Narasi lebih kaya**: video boleh 6–7 menit untuk topik besar; Short sampai 55 detik dengan 6–7 adegan.
4. Jangan membuat ulang suara yang sudah ada; jangan memakai foto/AI realistis (kartun saja, agar label konten sintetis tetap "Tidak").

## 7. Setelah selesai
- Centang topik di `CALENDAR.md`, isi link YouTube, commit & push ke `main`.
- Simpan naskah ke project "Konten Youtube": `claude/naskah-voice-over-<topik>.md`.
