import os
from pathlib import Path

from dotenv import load_dotenv

# 環境変数へ反映
load_dotenv()

RADIKO_AREA_ID = os.getenv('RADIKO_AREA_ID')

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)