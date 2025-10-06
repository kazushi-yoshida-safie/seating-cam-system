import os
from dotenv import load_dotenv
from dataclasses import dataclass
# 環境変数からSlackトークンを取得
load_dotenv()
USER_TOKEN = os.getenv("SLACK_USER_OAUTH_TOKEN")
BOT_TOKEN = os.getenv("SLACK_BOT_OAUTH_TOKEN")

# APIのエンドポイントを叩く際のヘッダーを定義
USER_AUTH_HEADER = {"Authorization": f"Bearer {USER_TOKEN}"}
BOT_AUTH_HEADER = {"Authorization": f"Bearer {BOT_TOKEN}"}

# Slack APIのURL (変更なし)
SLACK_API_URL_LOOKUP = "https://slack.com/api/users.lookupByEmail"
SLACK_API_URL_PROFILE_SET = "https://slack.com/api/users.profile.set"


# =============CLASS=============
@dataclass
class DatabaseConfig:
    """データベース接続設定"""
    dbname: str = os.environ.get("POSTGRES_DB", "seating-db")
    user: str = os.environ.get("POSTGRES_USER", "test")
    password: str = os.environ.get("POSTGRES_PASSWORD", "test")
    host: str = "db"
    port: str = "5432"
    
    def to_dict(self):
        """psycopg2用の辞書形式に変換"""
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port
        }
db_config = DatabaseConfig()