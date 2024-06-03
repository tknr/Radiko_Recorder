import time
import base64

import requests
from requests.exceptions import Timeout

from .utils import Logger

logger = Logger.getLogger(__name__)

class RadikoAuthHandler(object):
    '''
    Radiko APIの認可クラス
    '''
    _AUTH1_URL = 'https://radiko.jp/v2/api/auth1'
    _AUTH2_URL = 'https://radiko.jp/v2/api/auth2'
    
    # Radikoの認可キー (固定値)
    # 参照: http://radiko.jp/apps/js/playerCommon.js
    _RADIKO_AUTH_KEY = b'bcd151073c03b352e1ef2fd66c32209da9ca0afa'
    
    def __init__(self, area_id: str='JP13') -> None:
        '''
        コンストラクタ
        
        Parameters
        ----------
        area_id : str
            RadikoのエリアID
        
        Attributes
        ----------
        _headers : dict
            認可済みのヘッダ
        '''
        # ヘッダの初期化
        self._headers = {
            'User-Agent': 'python3.7',
            'Accept': '*/*',
            'X-Radiko-App': 'pc_html5',
            'X-Radiko-App-Version': '0.0.1',
            'X-Radiko-User': 'dummy_user',
            'X-Radiko-Device': 'pc',
            'X-Radiko-AuthToken': '',
            'X-Radiko-Partialkey': '',
            'X-Radiko-AreaId': area_id
        }
        
        # 認可処理
        self._auth()

    def get_auththenticated_headers(self) -> dict:
        '''
        認可済みのヘッダを取得する
        
        Returns
        -------
        dict
            認可済みのヘッダ
        '''
        return self._headers

    def _auth(self):
        '''
        RadikoAPIで認可を行う
        '''
        # 認可リクエストを送信
        res = self._call_auth_api(RadikoAuthHandler._AUTH1_URL)
        
        # 認可用トークンと部分鍵を取得
        self._headers['X-Radiko-AuthToken'] = self._get_auth_token(res)
        self._headers['X-Radiko-Partialkey'] = self._get_partial_key(res)
        
        # auth1から得たトークンを使ってauth2を実行
        res = self._call_auth_api(RadikoAuthHandler._AUTH2_URL)
        
        # ログ出力
        logger.debug(f'authenticated headers:{self._headers}')
        logger.debug(f'res.headers:{res.headers}')
        for cookie in res.cookies:
            logger.debug(f'res.cookie:{cookie}')
        logger.debug(f'res.content:{res.content}')

    def _call_auth_api(self, api_url: str) -> requests.Response:
        '''
        RadikoAPIに認可リクエストを送信する
        
        Parameters
        ----------
        api_url : str
            認可リクエストを送信するAPIのURL
        
        Returns
        -------
        requests.Response
            認可リクエストのレスポンス
        '''
        try:
            # 認可リクエストを送信
            res = requests.get(url=api_url, headers=self._headers, timeout=5.0)
            time.sleep(1)
        except Timeout as e:
            logger.warning(f'failed in {api_url}.')
            logger.warning('API Timeout')
            logger.warning(e)
            raise Exception(f'failed in {api_url}.')
        if res.status_code != 200:
            logger.warning(f'failed in {api_url}.')
            logger.warning(f'status_code:{res.status_code}')
            logger.warning(f'content:{res.content}')
            raise Exception(f'failed in {api_url}.')
        logger.debug(f'auth in {api_url} is success.')
        return res

    def _get_auth_token(self, response: requests.Response) -> str:
        '''
        HTTPレスポンスから認可用トークンを取得する
        
        Parameters
        ----------
        response : requests.Response
            認可リクエストのレスポンス
        
        Returns
        -------
        str
            認可用トークン
        '''
        return response.headers['X-Radiko-AUTHTOKEN']

    def _get_partial_key(self, response: requests.Response) -> str:
        '''
        HTTPレスポンスから認可用の部分鍵を取得する
        
        Parameters
        ----------
        response : requests.Response
            認可リクエストのレスポンス
        
        Returns
        -------
        str
            認可用の部分鍵
        '''
        length = int(response.headers['X-Radiko-KeyLength'])
        offset = int(response.headers['X-Radiko-KeyOffset'])
        partial_key = base64.b64encode(RadikoAuthHandler._RADIKO_AUTH_KEY[offset: offset + length])
        return partial_key