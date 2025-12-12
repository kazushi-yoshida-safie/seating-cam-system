from fastapi import FastAPI,HTTPException
import uvicorn
from application.find_user import FindUser
from interfaces.data_access.seats_info import SeatsInfo
from domain.type import Psycopg2Error

from domain.type import RaspiData
# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ラズパイから受け取るデータの型を定義


# POSTリクエストを受け取るエンドポイントを定義
@app.post("/receive-encording")
def receive_data_from_raspi(data: RaspiData):
    print(f"  deviceID: {data.device_id}")
    print(f"  message: {data.encord}")
    app=FindUser()
    app.run(data)
    
    return {"status": "success", "received_message": data.encord}

@app.get("/all-seats-info/{department_id}")
def receive_seats_info(department_id: int):
    try:
        app = SeatsInfo()
        res = app.res_seats_info(department_id)
        return {"status": "success", "data": res}
    except  ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Psycopg2Error as p:
        raise HTTPException(status_code=500, detail=str(p))
# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "APIサーバーは正常に稼働しています"}

# サーバーを起動
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)