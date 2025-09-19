
import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from backend.app.src.core import config
# .envファイルから環境変数を読み込む
load_dotenv()

# FastAPIアプリケーションを初期化
app = FastAPI(
    title="Slack Full Name Updater", # 説明を変更
    description="Update a Slack user's full name using their email address." # 説明を変更
)
# 【変更点1】リクエストボディの型を定義
class UpdateFullNameRequest(BaseModel):
    email: EmailStr
    new_full_name: str


# 【変更点2】エンドポイントと関数名を変更
@app.post("/update-full-name")
async def update_full_name(request: UpdateFullNameRequest):
    """
    指定されたメールアドレスのSlackユーザーの氏名を変更します。
    """
    if not config.USER_TOKEN or not config.BOT_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth tokens are not configured in the environment."
        )

    user_id = None
    
    async with httpx.AsyncClient() as client:
        # --- ステップ1: メールアドレスからユーザーIDを取得 ---
        try:
            response_lookup = await client.get(
                config.SLACK_API_URL_LOOKUP,
                headers=config.BOT_AUTH_HEADER,
                params={"email": request.email}
            )
            response_lookup.raise_for_status()
            data_lookup = response_lookup.json()

            if not data_lookup.get("ok"):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Slack API error (lookup): {data_lookup.get('error', 'Unknown error')}"
                )
            
            user_id = data_lookup["user"]["id"]

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Slack API: {e}"
            )
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with the provided email address."
            )

        # --- ステップ2: ユーザーIDを使って氏名を変更 ---
        try:
            # 【変更点3】Slackに送信するデータを 'real_name' に変更
            profile_data = {
                "profile": {
                    "real_name": request.new_full_name
                },
                "user": user_id
            }
            response_profile = await client.post(
                config.SLACK_API_URL_PROFILE_SET,
                headers=config.USER_AUTH_HEADER,
                json=profile_data
            )
            response_profile.raise_for_status()
            data_profile = response_profile.json()

            if not data_profile.get("ok"):
                 raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Slack API error (profile.set): {data_profile.get('error', 'Unknown error')}"
                )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not connect to Slack API: {e}"
            )
            
    return {"message": "Full name updated successfully", "user_id": user_id}