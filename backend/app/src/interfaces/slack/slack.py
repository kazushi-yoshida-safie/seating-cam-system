import  domain.config as config
from interfaces.data_access.user_repository import UserRepository
import httpx
import asyncio
class Slack:
    def __init__(self):
        self.user_repo = UserRepository()

    async def update_slack_status(self,user):
        print("start update slack status")
        if not config.USER_TOKEN or not config.BOT_TOKEN:
            print("Token is not set")
            return 
        email = self.user_repo.get_user_email(user)
        if not email:
            raise ValueError(f"not found{user} email")
        user_id = None
        async with httpx.AsyncClient() as client:
            try:
                response_lookup = await client.get(
                    config.SLACK_API_URL_LOOKUP,
                    headers=config.BOT_AUTH_HEADER,
                    params={"email": email}
                )
                response_lookup.raise_for_status()
                data_lookup = response_lookup.json()

                if not data_lookup.get("ok"):
                    raise RuntimeError(f"Slack APIエラー (lookup): {data_lookup.get('error', '不明なエラー')}")
                
                user_id = data_lookup["user"]["id"]

            except httpx.RequestError as e:
                raise RuntimeError(f"Slack APIへの接続に失敗しました: {e}")
            except KeyError:
                raise ValueError("指定されたメールアドレスを持つSlackユーザーが見つかりません。")

            try:
                status_text = "吉田和司API test"
                status_emoji = ":speech_balloon:"

                profile_data = {
                    "profile": {
                        "status_text": status_text,
                        "status_emoji": status_emoji
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
                    raise RuntimeError(f"Slack APIエラー (profile.set): {data_profile.get('error', '不明なエラー')}")

            except httpx.RequestError as e:
                raise RuntimeError(f"Slack APIへの接続に失敗しました: {e}")
        
        print(f"✅ {user} ({user_id}) のステータスを '{status_text}' に更新しました。")
        # return user_id
