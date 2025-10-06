from interfaces.data_access.user_repository import UserRepository
import numpy as np
from domain.type import  User
from application.comparator import FaceComparator
# UserRepositoryクラスが定義されているファイルをインポートする必要があります
# from infrastructure.persistence.user_repository import UserRepository 
from domain.type import RaspiData
class FindUser:
    """
    アプリケーションのセットアップと実行を担当するクラス
    """
    def __init__(self):
        self.user_repo = UserRepository()
        self.comparator = FaceComparator()

    def run(self, data:RaspiData):
        print("アプリケーションを実行します...")
        user_encodings = self.user_repo.get_all_user_face_encodings()        
        if not user_encodings:
             print("not found user_encordings")
             return
        #userの特定
        best_match_user = self.identity_user(user_encodings)
        
        print(f"特定したユーザーは{best_match_user}")
        print("アプリケーションを終了します。")
    
    def identify_user(self,data:RaspiData,user_encodings):
         best_match_user = None
         min_distance = float('inf')
        # 3. インスタンスのメソッドを呼び出す
         if user_encodings:
            print(f"{len(user_encodings)} 件のデータを取得しました。")
            # user特定ロジック
            for user_id, face_encoding in user_encodings:
                    result_distance = self.comparator.calculate_distance(data.encord, face_encoding)
                    if result_distance < min_distance:
                         min_distance = result_distance
                         best_match_user = user_id
            # TODO ここに距離が高すぎる場合は一致ユーザーがいないという処理にする
         else:
            print("データが見つかりませんでした。")
        
         return best_match_user
         

