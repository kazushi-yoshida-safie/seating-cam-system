import psycopg2
import os

class UserRepository:
    def __init__(self):
        db_connection_params = {
            "dbname": os.environ.get("POSTGRES_DB", "seating-db"),
            "user": os.environ.get("POSTGRES_USER", "test"),
            "password": os.environ.get("POSTGRES_PASSWORD", "test"),
            "host": "db",
            "port": "5432"
        }
        self.db_params = db_connection_params

    def get_all_user_face_encodings(self) -> list | None:
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            
            with conn.cursor() as cur:
                sql = "SELECT user_id, face_encoding FROM users;"
                cur.execute(sql)   
                rows = cur.fetchall()
                print("========SUCCESS========\n  get encording data!\n=======================")
                return rows

        except psycopg2.Error as e:
            print(f"database error: {e}")
            return None
            
        finally:
            if conn is not None:
                conn.close()
                print("closed database")

# ================== 使い方（実行例） ==================
# if __name__ == "__main__":
#     # 1. データベースの接続情報を辞書として準備
#     db_connection_params = {
#         "dbname": os.environ.get("POSTGRES_DB", "seating-db"),
#         "user": os.environ.get("POSTGRES_USER", "test"),
#         "password": os.environ.get("POSTGRES_PASSWORD", "test"),
#         "host": "localhost",
#         "port": "5432"
#     }
    
#     # 2. 接続情報を渡して、UserRepositoryクラスをインスタンス化
#     user_repo = UserRepository(db_params=db_connection_params)
    
#     # 3. インスタンスのメソッドを呼び出す
#     user_encodings = user_repo.get_all_user_face_encodings()
    
#     if user_encodings:
#         print(f"{len(user_encodings)} 件のデータを取得しました。")
#         for i, (user_id, face_encoding) in enumerate(user_encodings[:5]):
#             print(f"  {i+1}. User ID: {user_id}, Encoding Length: {len(face_encoding)}")