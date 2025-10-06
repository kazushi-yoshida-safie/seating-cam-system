from interfaces.data_access.user_repository import UserRepository
from domain.type import  User
from application.comparator import FaceComparator
from interfaces.data_access.recording_logs import SeatingRecorder
from interfaces.slack.slack import Slack
import numpy as np
import asyncio
from domain.type import RaspiData

class FindUser:
    """
    アプリケーションのセットアップと実行を担当するクラス
    """
    def __init__(self):
        self.user_repo = UserRepository()
        self.comparator = FaceComparator()
        self.recorder = SeatingRecorder()
        self.slack = Slack()

    def run(self, data:RaspiData):
        print("アプリケーションを実行します...")
        user_encodings = self.user_repo.get_all_user_face_encodings()        
        if not user_encodings:
             print("not found user_encordings")
             return
        #userの特定
        best_match_user = self.identify_user(data,user_encodings)
        if best_match_user == None:
             print("顔識別に失敗しました。")
             self.recorder.recording_logs(None,data.device_id,False)
             return

        # ログの追加
        self.recorder.recording_logs(best_match_user,data.device_id,True)
        #seatsとdevicesテーブルの更新
        self.recorder.recording_devices_and_seats_table(data.device_id)
        #Slackの送信
        asyncio.run(self.slack.update_slack_status(best_match_user))
        print("API STATE ALL SUCCESS!!")
    
    def identify_user(self,data:RaspiData,user_encodings):
         best_match_user = None
         min_distance = float('inf')
        # 3. インスタンスのメソッドを呼び出す
         print(f"{len(user_encodings)} 件のデータを取得しました。")
            # user特定ロジック
         for user_id, face_encoding in user_encodings:
                result_distance = self.comparator.calculate_distance(data.encord, face_encoding)
                if result_distance < min_distance:
                    min_distance = result_distance
                    best_match_user = user_id
        # TODO ここに距離が高すぎる場合は一致ユーザーがいないという処理にする
        
         return best_match_user
         

