from datetime import datetime, timedelta

import ffmpeg
import requests
from bs4 import BeautifulSoup

from .auth_handler import RadikoAuthHandler
from .utils import Logger

logger = Logger.getLogger(__name__)

class RadikoPlayer(object):
    def __init__(self, area_id: str):
        '''
        コンストラクタ
        
        Parameters
        ----------
        area_id : str
            RadikoのエリアID
        '''
        self._area_id = area_id
        self._headers = self._make_headers(area_id)
    
    def record(self, station_id: str, start_time: datetime, duration_minutes: int, output_path: str):
        '''
        Radikoのストリームを録音して保存する

        Parameters
        ----------
        station_id : str
            放送局ID
        start_time : datetime
            録音開始時間
        duration_minutes : int
            録音時間（分）
        output_path : str
            保存先のファイルパス
        '''
        ft = self._format_datetime(start_time)
        end_time = start_time + timedelta(minutes=duration_minutes)
        to = self._format_datetime(end_time)
        
        stream_url = f"https://radiko.jp/v2/api/ts/playlist.m3u8?station_id={station_id}&l=15&ft={ft}&to={to}"
        headers = f"X-RADIKO-AUTHTOKEN: {self._headers['X-Radiko-AuthToken']}"
        
        # ffmpegコマンドを実行して録音
        logger.info(f'Recording {output_path}...')
        (
            ffmpeg
            .input(filename=stream_url, headers=headers)
            .output(filename=output_path, acodec='copy')
            .run(overwrite_output=True)
        )
        logger.info(f'Successfully recorded {output_path}')
    
    def get_station_list(self) -> list[dict]:
        '''
        放送局リストを取得する
        
        Returns
        -------
        station_list : list[dict]
            放送局リスト
        '''
        url = f'https://radiko.jp/v3/station/list/{self._area_id}.xml'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        
        station_list = []
        for s in soup.find_all('station'):
            station_list.append(
                {
                    'id': s.find('id').text,
                    'name': s.find('name').text,
                    'ascii_name': s.find('ascii_name').text,
                    'ruby': s.find('ruby').text
                }
            )
        return station_list
    
    def _make_headers(self, area_id: str) -> dict:
        '''
        ヘッダーの作成
        
        Parameters
        ----------
        area_id : str
            RadikoのエリアID
        
        Returns
        -------
        headers : dict
            ヘッダー
        '''
        headers = RadikoAuthHandler(area_id=area_id).get_auththenticated_headers()
        headers['Connection'] = 'keep-alive'
        logger.debug(f'headers: {headers}')
        return headers
    
    def _format_datetime(self, dt: datetime) -> str:
        '''
        日時をフォーマットする
        
        Parameters
        ----------
        dt : datetime
            日時
        
        Returns
        -------
        formatted_dt : str
            フォーマットされた日時
        '''
        return dt.strftime('%Y%m%d%H%M%S')