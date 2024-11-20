import os

from dotenv import load_dotenv

# 現在のスクリプトのディレクトリから.envをロード
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

RADIKO_AREA_ID = os.getenv('RADIKO_AREA_ID', 'JP13')  # デフォルト値として東京エリア（JP13）を指定