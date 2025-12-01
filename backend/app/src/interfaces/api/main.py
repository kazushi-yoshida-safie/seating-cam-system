from fastapi import FastAPI
import uvicorn
from application.find_user import FindUser
from interfaces.data_access.seats_info import SeatsInfo

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
def receice_seats_info(department_id: int):
    app = SeatsInfo()
    app.res_seats_info(department_id)
    return {"department_id": department_id}
# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "APIサーバーは正常に稼働しています"}

# サーバーを起動
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)