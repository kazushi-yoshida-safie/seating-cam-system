#ここが良くない。内側の円が外側について知ってしまっている。
#アプリケーション層がインターフェース層のことを知ってはいけない。(importもダメ)
#次回修正事項
from interfaces.data_access.user_repository import UserRepository
import os
# UserRepositoryクラスが定義されているファイルをインポートする必要があります
# from infrastructure.persistence.user_repository import UserRepository 
from domain.type import RaspiData
class FindUser:
    """
    アプリケーションのセットアップと実行を担当するクラス
    """
    def __init__(self):
        self.user_repo = UserRepository() #インスタンス初期化

    def run(self, data:RaspiData):
        print("アプリケーションを実行します...")
        print(data.encord)
        # 3. インスタンスのメソッドを呼び出す
        user_encodings = self.user_repo.get_all_user_face_encodings()
        
        if user_encodings:
            print(f"{len(user_encodings)} 件のデータを取得しました。")
            for i, (user_id, face_encoding) in enumerate(user_encodings[:5]):
                if face_encoding == data.encord:
                    print(f"一致ユーザーは{user_id}です")
        else:
            print("データが見つかりませんでした。")
        
        print("アプリケーションを終了します。")

# ================== 実行部分 ==================
# if __name__ == "__main__":
#     # Applicationクラスをインスタンス化
#     app = FindUser()
#     # runメソッドを実行
#     app.run()