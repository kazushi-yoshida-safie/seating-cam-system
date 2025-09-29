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
        self.user_repo = UserRepository() #インスタンス初期化
        self.comparator = FaceComparator()

    def run(self, data:RaspiData):
        print("アプリケーションを実行します...")
        # print(data.encord)
        # 3. インスタンスのメソッドを呼び出す
        user_encodings = self.user_repo.get_all_user_face_encodings()        
        if user_encodings:
            print(f"{len(user_encodings)} 件のデータを取得しました。")
            for i, (user_id, face_encoding) in enumerate(user_encodings[:5]):
                    print(face_encoding)
                    result = self.comparator.calculate_distance(data.encord, face_encoding)
                    print(f"結果は{result}")
        else:
            print("データが見つかりませんでした。")
        
        print("アプリケーションを終了します。")

# ================== 実行部分 ==================
# if __name__ == "__main__":
#     # Applicationクラスをインスタンス化
#     app = FindUser()
#     # runメソッドを実行
# #     app.run()
