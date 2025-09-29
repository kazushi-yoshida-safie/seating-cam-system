from pydantic import BaseModel
from dataclasses import dataclass
class RaspiData(BaseModel):
    device_id: str
    encord: str

@dataclass
class User:
    """ユーザー情報を保持するデータクラス"""
    user_id: str
    name: str
    face_encoding_str: str # DBから取得した文字列形式の特徴量
