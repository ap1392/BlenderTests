"""Decode every completed shot frame and prepare chronological visual review sheets.

Run with the bundled Python that provides Pillow and NumPy. Metrics flag frames
for inspection; they do not certify visual quality or replace visual review.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--shot', type=int, required=True, choices=range(1, 7))
    args = parser.parse_args()
    start = (args.shot-1)*288
    source = ROOT / 'renders/cinematic/unreal/frames'
    output = ROOT / f'renders/cinematic/review/shot_{args.shot:02d}'
    output.mkdir(parents=True, exist_ok=True)
    metrics = []
    previous = None
    for second in range(12):
        sheet = Image.new('RGB', (2880, 1220), '#191919')
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 12), f'ISEC shot {args.shot} | second {second+1}/12 | every frame, chronological left to right', fill='white')
        for within in range(24):
            index = start + second*24 + within
            path = source / f'ISEC_{index:04d}.png'
            with Image.open(path) as image:
                if image.size != (3840, 2160):
                    raise RuntimeError(f'Invalid dimensions: {path}')
                image.load()
                rgb = image.convert('RGB')
                thumbnail = rgb.resize((480, 270), Image.Resampling.LANCZOS)
                pixels = np.asarray(rgb.resize((320, 180), Image.Resampling.BOX), dtype=np.float32)/255
            luma = pixels @ np.array([.2126, .7152, .0722], dtype=np.float32)
            row = {'frame': index, 'seconds': index/24, 'mean_luma': float(luma.mean()),
                   'near_white_fraction': float((luma>.98).mean()), 'near_black_fraction': float((luma<.01).mean())}
            if previous is not None:
                row['mean_absolute_frame_difference'] = float(np.abs(luma-previous).mean())
                row['mean_exposure_change'] = float(abs(luma.mean()-previous.mean()))
                row['inspection_flag'] = row['mean_exposure_change']>.07 or row['mean_absolute_frame_difference']>.12
            previous = luma
            metrics.append(row)
            x = (within%6)*480
            y = 44+(within//6)*294
            sheet.paste(thumbnail, (x, y))
            draw.text((x+6, y+273), f'{index:04d} | {index/24:.3f}s', fill='white')
        sheet.save(output / f'second_{second+1:02d}.jpg', quality=93, subsampling=0)
    report = {'shot': args.shot, 'decoded_frames': len(metrics), 'dimensions': [3840, 2160],
              'visual_review': 'pending', 'flagged_frames': [r['frame'] for r in metrics if r.get('inspection_flag')],
              'frames': metrics}
    (output / 'frame_audit.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k!='frames'}, indent=2))


if __name__ == '__main__':
    main()
