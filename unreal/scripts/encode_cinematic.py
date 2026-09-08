"""Encode only a complete, dimension-verified 72-second MRQ PNG sequence."""
import json
import shutil
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "renders/cinematic/unreal/frames"
OUTPUT = ROOT / "renders/cinematic/ISEC_72s_4K.mp4"
EXPECTED = 1728


def main():
    status = json.loads((FRAMES / "render_status.json").read_text())
    if not status.get("complete") or status.get("errors"):
        raise RuntimeError("MRQ has not completed successfully")
    files = sorted(FRAMES.glob("ISEC_*.png"))
    if len(files) != EXPECTED:
        raise RuntimeError(f"Expected {EXPECTED} frames, found {len(files)}")
    indices = [int(p.stem.replace("ISEC_", "", 1)) for p in files]
    if indices != list(range(EXPECTED)):
        raise RuntimeError("Missing or nonconsecutive frame numbers")
    for path in files:
        with path.open("rb") as f:
            header = f.read(24)
        if header[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", header[16:24]) != (3840, 2160):
            raise RuntimeError(f"Invalid 4K PNG: {path}")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe are required")
    temporary = OUTPUT.with_name(OUTPUT.stem + ".encoding.mp4")
    subprocess.run([
        ffmpeg, "-y", "-framerate", "24", "-start_number", str(indices[0]),
        "-i", str(FRAMES / "ISEC_%04d.png"), "-frames:v", str(EXPECTED),
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
        "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-movflags", "+faststart", "-an", str(temporary)
    ], check=True)
    data = json.loads(subprocess.check_output([
        ffprobe, "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames,duration",
        "-of", "json", str(temporary)
    ]))
    stream = data["streams"][0]
    if (stream["width"], stream["height"], stream["r_frame_rate"], int(stream["nb_read_frames"])) != (3840, 2160, "24/1", EXPECTED):
        raise RuntimeError(f"Encoded movie failed verification: {stream}")
    if abs(float(stream["duration"]) - 72) > .001:
        raise RuntimeError("Encoded movie duration differs from 72 seconds")
    subprocess.run([
        ffmpeg, "-v", "error", "-xerror", "-i", str(temporary),
        "-map", "0:v:0", "-f", "null", "-"
    ], check=True)
    temporary.replace(OUTPUT)
    data.update({"movie": str(OUTPUT), "frame_directory": str(FRAMES), "technical_validation": "passed", "visual_review": "pending"})
    OUTPUT.with_suffix(".validation.json").write_text(json.dumps(data, indent=2))
    print(OUTPUT)


if __name__ == "__main__":
    main()
