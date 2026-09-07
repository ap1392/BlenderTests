# BlenderTests

Local Blender workspace for editable 3D scenes and rendered previews.

Verified setup: Blender 5.2.1 LTS, native Apple Silicon installation in Applications.
The setup scene rendered successfully with Cycles on the Apple M3 Pro 18-core GPU.
The first render took about three minutes. Blender needs macOS graphics access;
running it inside Codex's restricted sandbox failed during Metal initialization,
while the approved run outside that sandbox completed successfully.
Blender was installed from the official download, with its SHA-256 checked against
Homebrew's published metadata. The Intel Homebrew installation was removed.

## Workflow

Describe the object or scene you want in this Codex task. Codex can write Blender
Python scripts, run them with Blender, inspect the rendered images, and iterate.
The resulting `.blend` files can be opened and edited normally in Blender.
This workflow uses Blender's bundled Python (`bpy`); no separate Python package,
API key, or Blender MCP add-on is required.

## Commands

Run these from this folder:

```sh
# Verify the installed version
./blender.sh --version

# Rebuild the setup verification scene and render
./blender.sh --background --python-exit-code 1 --python scripts/setup_check.py

# Open the editable scene on macOS
open -a Blender output/setup_check/setup_check.blend
```

`blender.sh` uses `/Applications/Blender.app/Contents/MacOS/Blender`.
Set `BLENDER_APP` if you move Blender to a different location.

## Files

- `scripts/setup_check.py`: reproducible studio scene with a cube, sphere, and ring.
- `output/setup_check/setup_check.blend`: editable scene, camera, lights, and materials.
- `output/setup_check/setup_check.png`: rendered preview.
- `output/setup_check/setup_report.json`: Blender version and rendering device used.

The setup check rebuilds its own output files. Keep future projects in separate
subfolders so rerunning it does not overwrite your work.

## References

- [OpenAI's Blender workflow](https://developers.openai.com/blog/architectural-visualization-with-astra)
- [Blender Python API](https://docs.blender.org/api/current/)
