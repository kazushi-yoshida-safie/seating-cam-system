import os

# 環境変数からSlackトークンを取得
USER_TOKEN = os.getenv("SLACK_USER_OAUTH_TOKEN")
BOT_TOKEN = os.getenv("SLACK_BOT_OAUTH_TOKEN")

# APIのエンドポイントを叩く際のヘッダーを定義
USER_AUTH_HEADER = {"Authorization": f"Bearer {USER_TOKEN}"}
BOT_AUTH_HEADER = {"Authorization": f"Bearer {BOT_TOKEN}"}

# Slack APIのURL (変更なし)
SLACK_API_URL_LOOKUP = "https://slack.com/api/users.lookupByEmail"
SLACK_API_URL_PROFILE_SET = "https://slack.com/api/users.profile.set"