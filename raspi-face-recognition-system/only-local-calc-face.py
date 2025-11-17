import time
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
import face_recognition
from pathlib import Path
import requests  # HTTPリクエストのために追加
import json      # JSONデータ作成のために追加

# --- 設定項目 ---
IMAGE_WIDTH: int = 1280
IMAGE_HEIGHT: int = 720
IMAGE_FORMAT: str = "RGB888"
# OUTPUT_DIR: Path = Path("encording") # ファイル保存が不要なためコメントアウト

DETECTION_MODEL: str = "cnn"

# --- API設定 (追加) ---
API_URL: str = "http://localhost:8000/receive-encording"
DEVICE_ID: int = 1001 # curlの例にあったdevice_id

# --- 関数 (変更) ---
def find_and_send_features(image_array):
    """
    画像から顔の特徴量を検出し、APIサーバーにPOSTリクエストで送信する。
    """
    try:
        print("画像データから顔を検出しています...")
        # ここはhogだと精度が悪い(けどcnnは遅い)
        face_locations = face_recognition.face_locations(image_array, model=DETECTION_MODEL)

        if not face_locations:
            print("-> 顔が検出されませんでした。")
            return False

        print(f"-> {len(face_locations)} 件の顔を検出しました。")
        if len(face_locations) > 1:
            print("複数の顔が検出されました。単一の顔のみ処理します。")
            # 複数の顔が検出されても、最初の1人だけ処理を続行する（仕様に応じて変更してください）
            # もし複数の顔でエラーにする場合は return False にしてください。
            # return False 

        face_encoding = face_recognition.face_encodings(image_array, face_locations)
        single_face_encoding = face_encoding[0] # 最初の顔の特徴量を取得

        # --- ここからファイル保存の代わりにAPI送信処理 ---
        print("特徴量をサーバーに送信準備しています...")

        # curlの例に合わせて、Numpy配列をカンマ区切りの文字列に変換
        encoding_str = ','.join(map(str, single_face_encoding))

        # 送信するJSONデータを作成 (キーはcurlの例に合わせて 'encord' としています)
        payload = {
            "device_id": DEVICE_ID,
            "encord": encoding_str
        }

        headers = {
            "Content-Type": "application/json"
        }

        # サーバーにPOSTリクエストを送信
        try:
            response = requests.post(API_URL, data=json.dumps(payload), headers=headers, timeout=10)
            
            # サーバーからの応答をチェック
            if response.status_code == 200:
                print("特徴量の送信に成功しました。")
                print(f"サーバー応答: {response.text}") # 応答内容を表示
                return True
            else:
                print(f"サーバーへの送信に失敗しました。ステータスコード: {response.status_code}")
                print(f"エラー内容: {response.text}")
                return False

        except requests.exceptions.RequestException as req_e:
            print(f"リクエスト中にエラーが発生しました (接続拒否など): {req_e}")
            return False
        # --- API送信処理ここまで ---

    except Exception as e:
        print(f"顔検出またはエンコード処理中にエラーが発生しました: {e}")
        return False

# --- メイン処理 (変更) ---
if __name__ == "__main__":
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (IMAGE_WIDTH, IMAGE_HEIGHT), "format": IMAGE_FORMAT})
    picam2.configure(camera_config)

    print("カメラを起動します...")
    picam2.start()
    time.sleep(2)

    print("スナップショットを撮影します...")

    image = picam2.capture_array("main")
    print("撮影が完了しました。")

    picam2.stop()
    print("カメラ終了しました。")

    # ファイルパスの代わりに、変更した関数を呼び出す
    success = find_and_send_features(image)

    if success:
        print("\n処理が正常に完了しました (特徴量送信済み)。")
    else:
        print("\n顔が検出されなかったか、サーバーへの送信に失敗しました。")