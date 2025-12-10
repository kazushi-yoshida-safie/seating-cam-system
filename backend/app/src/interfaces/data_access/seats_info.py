from domain.config import db_config
import psycopg2
from psycopg2.extras import RealDictCursor
from domain.type import Psycopg2Error
class SeatsInfo:
    def __init__(self):
        self.db_params = db_config.to_dict()
    
    def res_seats_info(self,department_id:int):
        sql="""SELECT seat_id,is_active,seating_user,created_at FROM seats WHERE department_id = %s;"""
        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(sql,(department_id, ))
                    res = cursor.fetchall()
                    if not res:
                        print(f"404: Department ID {department_id} not found.")
                        raise ValueError(f"Department ID {department_id} not found")
                print("SUCCSESS : ",res)
                return res
        except psycopg2.Error as e:
            print(f"database-error : {e}")
            if conn:
                conn.rollback()
            raise Psycopg2Error("department not found")
        finally:
            if conn is not None:
                conn.close()


