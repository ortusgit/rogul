import json,glob,subprocess,sys,os
name,prefix,out=sys.argv[1:4]; delta=float(sys.argv[4]) if len(sys.argv)>4 else 0
d=json.load(open(f'rec/{name}.json'))
webm=glob.glob(f'rec/{name}/*.webm')[0]
vdur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',webm]))
origin=d['click_wall']-d['nav']/1000+delta
starts={}
for x in d['log']:
    if x['e']=='playing' and x['i'] not in starts: starts[x['i']]=origin+x['t']/1000
files=sorted(glob.glob(f'audio/{prefix}-*.mp3'))
assert len(starts)==len(files),(len(starts),len(files))
endw=origin+d['end']/1000
print('video',vdur,'expected end',endw,'first start',starts[0])
cut0=max(0,starts[0]-0.6)  # potong awal: mulai 0,6 dtk sebelum suara pertama
inputs=['-ss',f'{cut0:.3f}','-i',webm]
filt=[]
for k,f in enumerate(files):
    inputs+=['-i',f]
    dk=(json.load(open(os.environ['DELTAS']))[k]-delta) if os.environ.get('DELTAS') else 0
    ms=int(round((starts[k]+dk-cut0)*1000))
    filt.append(f'[{k+1}:a]adelay={ms}|{ms}[a{k}]')
filt.append(''.join(f'[a{k}]' for k in range(len(files)))+f'amix=inputs={len(files)}:normalize=0[aout]')
cmd=['ffmpeg','-y','-loglevel','error',*inputs,'-filter_complex',';'.join(filt),'-map','0:v','-map','[aout]',*(['-vf',os.environ['CROP']] if os.environ.get('CROP') else []),
     '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ac','2','-shortest','-movflags','+faststart',out]
subprocess.run(cmd,check=True)
print(out, subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height','-of','csv=p=0',out]).decode())
