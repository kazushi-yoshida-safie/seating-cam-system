from domain.config import db_config
import psycopg2
class SeatsInfo:
    def __init__(self):
        self.db_params = db_config.to_dict()
    
    def res_seats_info(self,department_id:int):
        sql="""SELECT * FROM seats WHERE department_id = %s;"""
        try:
            with psycopg2.connect(**self.db_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql,(department_id, ))
                    res = cursor.fetchall()
                print("SUCCSESS : ",res)
        except psycopg2.Error as e:
            print(f"database-error : {e}")
            if conn:
                conn.rollback()
        finally:
            if conn is not None:
                conn.close()


