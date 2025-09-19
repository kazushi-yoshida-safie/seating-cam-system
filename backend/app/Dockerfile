# 1. ベースとなるPythonイメージを選択
FROM python:3.11-slim

# 2. コンテナ内での作業ディレクトリを設定
WORKDIR /src

# 3. 依存ライブラリのインストール (コードより先にインストールしてキャッシュを活用)
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 4. プロジェクトのソースコードをコンテナにコピー
COPY ./main.py /app/main.py
COPY ./src /app/src

# 5. コンテナがリッスンするポートを指定
EXPOSE 8000

# 6. コンテナ起動時に実行するコマンド
# uvicornを0.0.0.0でホストすることで、コンテナ外からのアクセスを許可
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]