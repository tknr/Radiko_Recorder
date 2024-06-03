import os
import time

import ffmpeg
import requests
from datetime import datetime, timedelta

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
        self._headers = self._make_headers(area_id)
    
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
    
    def record(self, station: str, output_path: str, record_time: int):
        '''
        放送を録音する
        
        Parameters
        ----------
        station : str
            放送局名
        output_path : str
            出力ファイルのパス
        record_time : int
            録音時間（秒）
        '''
        end_time = datetime.now() + timedelta(seconds=record_time)
        chunk_files = []

        # 録音を開始する
        while datetime.now() < end_time:
            remaining_time = (end_time - datetime.now()).total_seconds()
            chunk_time = min(remaining_time, 5)  # 5秒ごとに録音
            output_chunk = f"{output_path}.{int(time.time())}.aac"
            chunk_files.append(output_chunk)
            
            # ストリームを取得して録音
            stream_url = self._get_stream_url(station)
            (
                ffmpeg
                .input(filename=stream_url, f='aac', acodec='aac')
                .output(filename=output_chunk, t=chunk_time)
                .run(overwrite_output=True)
            )
            
            time.sleep(chunk_time)  # 追加の遅延を防ぐために録音時間だけ待機
            logger.info(f'Recorded {station} for {chunk_time} seconds to {output_chunk}')

        # チャンクファイルのリストを作成
        with open('filelist.txt', 'w') as f:
            for chunk in chunk_files:
                f.write(f"file '{chunk}'\n")
        
        # チャンクファイルを結合
        (
            ffmpeg
            .input(filename='filelist.txt', format='concat', safe=0)
            .output(filename=output_path, c='copy')
            .run(overwrite_output=True)
        )
        
        # 一時ファイルの削除
        for chunk in chunk_files:
            os.remove(chunk)
        
        logger.info(f'Recorded {station} for {record_time} seconds to {output_path}')
    
    def get_program_table(self, station: str) -> str:
        '''
        番組表を取得する
        
        Parameters
        ----------
        station : str
            放送局名
        
        Returns
        -------
        program_table : str
            番組表
        '''
        response = requests.get(
            url=f'http://radiko.jp/v3/program/station/weekly/{station}.xml',
            headers=self._headers
        )
        return response.text
    
    def _get_m3u8_url(self, station: str) -> str:
        '''
        m3u8ファイルのURLを取得する
        
        Parameters
        ----------
        station : str
            放送局名
        
        Returns
        -------
        m3u8_url : str
            m3u8ファイルのURL
        '''
        response = requests.get(
            url=f'http://c-radiko.smartstream.ne.jp/{station}/_definst_/simul-stream.stream/playlist.m3u8',
            headers=self._headers
        )
        m3u8_url = response.content.splitlines()[-1]
        return m3u8_url
    
    def _get_stream_url(self, station: str) -> str:
        '''
        ストリームのURLを取得する
        
        Parameters
        ----------
        station : str
            放送局名
        
        Returns
        -------
        stream_url : str
            ストリームのURL
        '''
        m3u8_url = self._get_m3u8_url(station)
        response = requests.get(m3u8_url)
        stream_url = response.content.splitlines()[-1]
        return stream_url