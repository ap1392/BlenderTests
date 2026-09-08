"""Persistent editor worker for this project's explicitly listed Python jobs.

Uses Unreal's game-thread ticker, no network listener or UI automation.
"""
import unreal,json,runpy,os,traceback,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];QUEUE=ROOT/'unreal/validation/editor_job.json';RESULT=ROOT/'unreal/validation/editor_job_result.json'
ALLOWED={'import_architecture.py','build_materials.py','build_cinematic_scene.py','render_cinematic.py'}
os.environ['ISEC_EDITOR_SESSION']='1'
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
last_id=None
(ROOT/'unreal/validation/editor_session_ready.json').write_text(json.dumps({'ready':True,'engine':unreal.SystemLibrary.get_engine_version()}))
def tick(delta):
 global last_id
 if not QUEUE.exists():return True
 job=json.loads(QUEUE.read_text())
 if job['id']==last_id:return True
 last_id=job['id'];status={'id':last_id,'script':job['script'],'complete':False,'started':time.time()};RESULT.write_text(json.dumps(status))
 try:
  if job['script']not in ALLOWED:raise RuntimeError('Job is not in the project allowlist')
  os.environ['ISEC_RENDER_FULL']='1'if job.get('full_movie')else'0'
  runpy.run_path(str(ROOT/'unreal/scripts'/job['script']),run_name='__main__')
  status['complete']=True
 except Exception:
  status['error']=traceback.format_exc();unreal.log_error(status['error'])
 status['finished']=time.time();RESULT.write_text(json.dumps(status,indent=2));return True
unreal.isec_job_ticker=unreal.register_ticker_callback(tick,delay=.5)
