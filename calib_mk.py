import subprocess,numpy as np,json,glob,sys
name=sys.argv[1]; idx=int(sys.argv[2]) if len(sys.argv)>2 else 1
d=json.load(open(f'rec/{name}.json'))
go=[x['t'] for x in d['log'] if x['e']=='go' and x['i']==idx][0]
pred=d['click_wall']-d['nav']/1000+go/1000
webm=glob.glob(f'rec/{name}/*.webm')[0]; s=pred-1.5
out=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(s),'-i',webm,'-t','3','-vf','crop=200:6:0:2','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
fr=np.frombuffer(out,np.uint8).reshape(-1,6,200); m=[f.mean() for f in fr]; fps=len(m)/3
want=(idx%2==1)
z=[k for k,v in enumerate(m) if (v>128)==want and k>0 and (m[k-1]>128)!=want]
print(round(s+z[0]/fps-pred,2))
