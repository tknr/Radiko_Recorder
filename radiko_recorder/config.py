import os

from dotenv import load_dotenv

# 環境変数へ反映
load_dotenv()

RADIKO_AREA_ID = os.getenv('RADIKO_AREA_ID')