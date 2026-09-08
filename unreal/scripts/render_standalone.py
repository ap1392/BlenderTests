"""Run saved MRQ presets sequentially without a second editor world in memory."""
import argparse
import json
import struct
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENGINE = Path('/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor')
PROJECT = ROOT / 'unreal/ISEC_Cinematic/ISEC_Cinematic.uproject'


def valid_frame(path):
    if not path.exists():
        return False
    with path.open('rb') as f:
        header = f.read(24)
    return len(header) == 24 and header[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', header[16:24]) == (3840, 2160)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['Review', 'Final'], default='Review')
    parser.add_argument('--shots', nargs='+', type=int, default=list(range(1, 7)))
    args = parser.parse_args()
    if any(s not in range(1, 7) for s in args.shots):
        parser.error('Shot numbers must be 1–6')
    manifest = json.loads((ROOT / 'unreal/validation/render_presets.json').read_text())
    if not manifest['complete']:
        raise RuntimeError('Saved MRQ presets are incomplete')
    directory = ROOT / 'renders/cinematic/unreal' / ('frames' if args.mode == 'Final' else 'review_shots')
    directory.mkdir(parents=True, exist_ok=True)
    report_path = directory / 'render_status.json'
    report = {'complete': False, 'mode': args.mode, 'errors': [], 'shots': [], 'started': time.time()}
    report_path.write_text(json.dumps(report, indent=2))
    for shot in args.shots:
        preset = next(p for p in manifest['presets'] if p['mode'] == args.mode and p['shot'] == shot)
        logfile = ROOT / f'unreal/validation/standalone_{args.mode.lower()}_{shot:02d}.log'
        # The user's default Python can be Intel; force the universal engine's
        # native Apple Silicon slice rather than inheriting Rosetta execution.
        command = ['/usr/bin/arch', '-arm64', str(ENGINE), str(PROJECT), '/Game/ISEC/Maps/ISEC_Presentation', '-game',
                   '-LevelSequence=/Game/ISEC/Cinematics/ISEC_72s.ISEC_72s',
                   '-MoviePipelineConfig=' + preset['asset'],
                   '-windowed', '-ResX=640', '-ResY=360', '-RenderOffscreen',
                   '-nop4', '-nosplash', '-nosound', '-unattended', '-stdout', '-FullStdOutLogOutput',
                   '-ExecCmds=r.Shadow.MaxResolution 512,r.Shadow.MaxCSMResolution 2048,r.Lumen.HardwareRayTracing 0']
        started = time.time()
        print(f'Starting {args.mode} shot {shot}; MRQ output remains 3840×2160', flush=True)
        with logfile.open('w') as log:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
            report['active_shot'] = shot
            report['process_id'] = process.pid
            report_path.write_text(json.dumps(report, indent=2))
            code = process.wait()
        missing = [i for i in range(preset['start'], preset['end_exclusive'])
                   if not valid_frame(directory / f'ISEC_{i:04d}.png')]
        entry = {'shot': shot, 'exit_code': code, 'elapsed_seconds': time.time()-started,
                 'missing_or_invalid_frames': missing, 'log': str(logfile)}
        report['shots'].append(entry)
        if code or missing:
            report['errors'].append(entry)
            report_path.write_text(json.dumps(report, indent=2))
            raise RuntimeError(f'Shot {shot} did not finish cleanly; inspect {logfile}')
        print(f'Completed shot {shot} in {entry["elapsed_seconds"]:.1f}s', flush=True)
        report_path.write_text(json.dumps(report, indent=2))
    required = range(1728) if args.mode == 'Final' else [s*288+143 for s in range(6)]
    report['complete'] = all(valid_frame(directory / f'ISEC_{i:04d}.png') for i in required)
    report['frames_written'] = len(list(directory.glob('ISEC_*.png')))
    report['elapsed_seconds'] = time.time()-report['started']
    report.pop('active_shot', None)
    report.pop('process_id', None)
    report_path.write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
