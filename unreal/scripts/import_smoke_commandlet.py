"""Repeat the corrected UV/scale import in a non-Slate commandlet context."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('import_smoke.py')),init_globals={'ISEC_COMMANDLET':True})
