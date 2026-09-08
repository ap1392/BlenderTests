"""Validate and encode the active render when it finishes; visual review stays pending."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / 'renders/cinematic/unreal/frames/render_status.json'
REPORT = ROOT / 'renders/cinematic/postprocess_status.json'
PYTHON = Path('/Users/aditya2610/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')


def main():
    state = {'stage': 'waiting_for_render', 'audited_shots': [], 'visual_review': 'pending'}
    try:
        while True:
            REPORT.write_text(json.dumps(state, indent=2))
            try:
                render = json.loads(STATUS.read_text())
            except json.JSONDecodeError:
                time.sleep(2)
                continue
            if render.get('errors'):
                raise RuntimeError('Renderer reported a failure; see render_status.json')
            if render.get('complete'):
                break
            time.sleep(15)
        # Wait until Unreal has exited before using CPU/RAM for image audits.
        for shot in range(1, 7):
            state['stage'] = 'auditing_shot_' + str(shot)
            REPORT.write_text(json.dumps(state, indent=2))
            subprocess.run([str(PYTHON), str(ROOT / 'unreal/scripts/audit_movie_frames.py'), '--shot', str(shot)], check=True)
            state['audited_shots'].append(shot)
        state['stage'] = 'encoding_movie'
        REPORT.write_text(json.dumps(state, indent=2))
        subprocess.run([sys.executable, str(ROOT / 'unreal/scripts/encode_cinematic.py')], check=True)
        state['stage'] = 'encoded_awaiting_visual_review'
        state['movie'] = str(ROOT / 'renders/cinematic/ISEC_72s_4K.mp4')
    except Exception as exc:
        state['stage'] = 'failed'
        state['error'] = str(exc)
        raise
    finally:
        REPORT.write_text(json.dumps(state, indent=2))


if __name__ == '__main__':
    main()
