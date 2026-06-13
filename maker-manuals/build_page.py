from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
PUBLIEKSLAAG_ROOT = ROOT.parent
sys.path.insert(0, str(PUBLIEKSLAAG_ROOT))

from site_content import write_manuals_source_index


if __name__ == "__main__":
    write_manuals_source_index()
