from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageStat
import json

root = Path(__file__).resolve().parents[3]
progress = json.loads((root / 'renders/fidelity/large/progress.json').read_text())
register = json.loads((root / 'references/fidelity/calibration/camera_register.json').read_text())
expected = {entry['camera'] for entry in register}
finished = {entry['camera'] for entry in progress['results']}
if not progress.get('complete') or expected != finished:
    raise SystemExit('Comparison generation waits for all twelve cameras in one completed revision.')
output = root / 'renders/fidelity/comparisons'
output.mkdir(exist_ok=True)
font_path = '/System/Library/Fonts/Helvetica.ttc'
heading = ImageFont.truetype(font_path, 23)
footer = ImageFont.truetype(font_path, 18)
small = ImageFont.truetype(font_path, 16)
contact = Image.new('RGB', (1800, 6 * 390), '#eeeeec')
draw = ImageDraw.Draw(contact)
for i, entry in enumerate(register):
    name = entry['camera']
    source = root / entry['reference']
    if name.startswith('REF08'):
        source = root / 'references/fidelity/atrium/isec_reflections_004-1.jpg'
    render = root / 'renders/fidelity/large' / f'{name}_validation.png'
    images = [Image.open(source).convert('RGB'), Image.open(render).convert('RGB')]
    recorded = next(result for result in progress['results'] if result['camera'] == name)
    if images[1].size != (recorded['width'], recorded['height']):
        raise ValueError('Render dimensions differ from the completed record: ' + name)
    if max(ImageStat.Stat(images[1]).stddev) < 2:
        raise ValueError('Render appears blank: ' + name)
    canvas = Image.new('RGB', (2200, 1000), '#eeeeec')
    d = ImageDraw.Draw(canvas)
    for j, (im, label) in enumerate(zip(images, ['REFERENCE PHOTOGRAPH', 'BLENDER RECONSTRUCTION — ' + progress['revision']])):
        factor = min(1070 / im.width, 915 / im.height)
        im = im.resize((int(im.width * factor), int(im.height * factor)), Image.Resampling.LANCZOS)
        canvas.paste(im, (j * 1100 + (1100 - im.width) // 2, 48 + (915 - im.height) // 2))
        d.text((j * 1100 + 20, 13), label, font=heading, fill='#222222')
    d.text((20, 973), name + ' | Camera registration remains approximate; see the five-issue discrepancy register.', font=footer, fill='#222222')
    canvas.save(output / f'{name}.jpg', quality=94)
    thumb = canvas.copy()
    thumb.thumbnail((895, 360))
    x, y = (i % 2) * 900, (i // 2) * 390
    contact.paste(thumb, (x, y + 25))
    draw.text((x + 10, y + 5), name, font=small, fill='#222222')
contact.save(output / 'contact.jpg', quality=94)
(output / 'revision.json').write_text(json.dumps({'revision': progress['revision'], 'cameras': sorted(finished), 'samples': progress['samples'], 'maximum_dimension': progress['maximum_dimension']}, indent=2))
print('Twelve consistent comparison boards refreshed: ' + progress['revision'])
