import psycopg2
import os

def get_all_user_face_encodings():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "seating-db"),
            user=os.environ.get("POSTGRES_USER", "test"),
            password=os.environ.get("POSTGRES_PASSWORD", "test"),
            host="localhost",
            port="5432"
        )
        with conn.cursor() as cur:
            sql = "SELECT user_id, face_encoding FROM users;"
            cur.execute(sql)   
            rows = cur.fetchall()
            
            print("データの取得に成功しました。")
            return rows

    except psycopg2.Error as e:
        print(f"データベースエラー: {e}")
        return None
        
    finally:
        if conn is not None:
            conn.close()
            print("データベース接続をクローズしました。")


# ==================test case==================
# if __name__ == "__main__":
#     user_encodings = get_all_user_face_encodings()
#     print(len(user_encodings))
#     if user_encodings:
#         print(f"{len(user_encodings)} 件のデータを取得しました。")
#         # 最初の5件だけ表示してみる
#         for i, (user_id, face_encoding) in enumerate(user_encodings[:5]):
#             # face_encodingはバイナリデータの可能性があるため、長さだけ表示
#             print(f"  {i+1}. User ID: {user_id}, Encoding Length: {len(face_encoding)}")