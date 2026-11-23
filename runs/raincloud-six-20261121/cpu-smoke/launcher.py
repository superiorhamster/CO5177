import subprocess,json,time
from pathlib import Path
d=Path('runs/raincloud-six-20261121/cpu-smoke');base=['colab','--config','/tmp/raincloud-cpu.json'];name='raincloud-cpu-smoke'
state={'status':'starting','runtime':'CPU'};created=False
try:
 subprocess.run(base+['new','-s',name],check=True);created=True;time.sleep(8)
 with (d/'execution.log').open('w') as f:subprocess.run(base+['exec','-s',name,'--timeout','0','-f',str(d/'raincloud_smoke.ipynb')],stdout=f,stderr=subprocess.STDOUT,check=True)
 n=json.loads((d/'raincloud_smoke_output.ipynb').read_text());assert not [o for c in n['cells'] for o in c.get('outputs',[]) if o.get('output_type')=='error']
 assert 'RAINCLOUD_SMOKE_PASSED' in (d/'execution.log').read_text()
 subprocess.run(base+['download','-s',name,'/content/raincloud-smoke.zip',str(d/'artifacts.zip')],check=True)
 state['status']='passed'
except Exception as e:state.update(status='failed',error=str(e));raise
finally:
 if created:state['vm_released']=subprocess.run(base+['stop','-s',name]).returncode==0
 (d/'driver.json').write_text(json.dumps(state,indent=2))
