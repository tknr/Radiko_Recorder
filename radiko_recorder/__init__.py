import time
import datetime as dt
from datetime import datetime

from scheduler import Scheduler

from .recorder import RadikoPlayer
from .config import (
    RADIKO_AREA_ID,
    OUTPUT_DIR
)

def check_schedule(schedule: Scheduler):
    '''
    スケジュールをチェックする関数
    
    Parameters
    ----------
    schedule : Scheduler
        スケジュール
    '''
    while True:
        schedule.exec_jobs()
        time.sleep(1)

def record_radio(station: str, output_path: str, record_time: int):
    '''
    ラジオを録音する関数
    
    Parameters
    ----------
    station : str
        放送局
    output_path : str
        出力先パス
    record_time : int
        録音時間（秒）
    '''
    player = RadikoPlayer(area_id=RADIKO_AREA_ID)
    player.record(station=station, output_path=output_path, record_time=record_time)

def main():
    '''
    メイン関数
    '''
    station = "FMGUNMA" # 群馬エフエム放送
    output_path = OUTPUT_DIR / f'{station}_{datetime.now().strftime("%Y%m%d%H%M%S")}.aac'
    record_time = 30
    
    # スケジュールを設定
    schedule = Scheduler(tzinfo=dt.timezone.utc)
    
    # 日本時間
    tz_japan = dt.timezone(dt.timedelta(hours=9), name='JST')
    
    # 指定した時間にラジオを録音する
    schedule.daily(
        timing=dt.time(hour=2, minute=53, tzinfo=tz_japan),
        handle=record_radio,
        args=(station, output_path, record_time),
    )
    
    # スケジュールをチェック
    check_schedule(schedule)

__all__ = ['main']