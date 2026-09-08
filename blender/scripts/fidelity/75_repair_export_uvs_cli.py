import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('73_export_batches_cli.py')),init_globals={'ISEC_UV_REPAIR_ONLY':True})
