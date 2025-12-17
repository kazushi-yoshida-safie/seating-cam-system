import os
from domain.config import db_config
import pytz
import datetime
import psycopg2
class SeatingRecorder:
    def __init__(self):
        self.db_params = db_config.to_dict()
    
    def recording_logs(self, user_id, device_id, is_seated):
        sql = """
            INSERT INTO recognition_logs (device_id, user_id, event_type, created_at)
            VALUES (%s, %s, %s, %s);
        """
        
        jst = pytz.timezone('Asia/Tokyo')
        created_at = datetime.datetime.now(jst)
        
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            
            with conn.cursor() as cursor:
                cursor.execute(sql, (device_id, user_id, is_seated, created_at))
            
            conn.commit()
            print(f"SUCCESS!: user_id={user_id}, device_id={device_id}, is_seated={is_seated}")

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"database-error: {e}")
        
        finally:
            if conn is not None:
                conn.close()

    def recording_devices_and_seats_table(self,user,device_id):
     conn = psycopg2.connect(**self.db_params)
     try:
        # withステートメントでカーソルを管理し、自動的に閉じる
        with conn.cursor() as cursor:
            
            sql_update_device = """
                UPDATE devices 
                SET is_active = TRUE 
                WHERE device_id = %s
                RETURNING seat_id;
            """
            cursor.execute(sql_update_device, (device_id,))
            
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f"指定されたデバイスIDが見つかりません: {device_id}")
            
            seat_id = result[0] # 取得したseat_id
            print(f"デバイス(id={device_id})をアクティブ化しました。関連シートID: {seat_id}")

            sql_update_seat = """
                UPDATE seats
                SET is_active = TRUE,seating_user = %s
                WHERE seat_id = %s;
            """
            cursor.execute(sql_update_seat, (user,seat_id))
            print(f"シート(id={seat_id})をアクティブ化しました。")

        conn.commit()
        print("✅ トランザクションが正常にコミットされました。")

     except (Exception, psycopg2.Error) as e:
        print(f"error : {e}")
        conn.rollback()
     finally:
         if conn is not None:
             print("conn closed")
             conn.close()


