import time
from datetime import datetime
from picamera2 import Picamera2
import face_recognition

def extract_and_save_features(image_path, output_txt_path):
    """
    指定された画像から顔を検出し、その特徴量をテキストファイルに保存する関数。

    Args:
        image_path (str): 入力となる画像ファイルのパス。
        output_txt_path (str): 特徴量を保存するテキストファイルのパス。
    """
    try:
        # 1. 画像ファイルを読み込む
        print(f"画像を読み込んでいます: {image_path}")
        image = face_recognition.load_image_file(image_path)

        # 2. 画像内のすべての顔を検出する
        #    モデルは'hog' (CPU向け) または 'cnn' (GPU向け、より高精度)が選べます。
        #    ラズパイでは'hog'が現実的です。
        face_locations = face_recognition.face_locations(image, model="hog")
        print(f"-> {len(face_locations)} 件の顔を検出しました。")

        # 3. 顔が検出されなかった場合は、処理を終了する
        if not face_locations:
            print("画像内に顔が検出されませんでした。")
            return

        # 4. 検出した顔の特徴量（128次元のベクトル）を抽出する
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # 5. 抽出した特徴量をテキストファイルに書き込む
        with open(output_txt_path, 'w') as f:
            print(f"特徴量をファイルに書き込んでいます: {output_txt_path}")
            # 検出した顔の数だけループ
            for i, encoding in enumerate(face_encodings):
                # numpy配列をカンマ区切りの文字列に変換
                encoding_str = ','.join(map(str, encoding))
                f.write(encoding_str + '\n')
                print(f"  - {i+1}番目の顔の特徴量を保存しました。")
        
        print("特徴量の保存が完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

# --- メインの処理 ---
if __name__ == "__main__":
    # Picamera2のインスタンスを作成・設定
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)

    # カメラを起動
    print("カメラを起動します...")
    picam2.start()
    time.sleep(2) # 露出調整のための待ち時間

    # タイムスタンプ付きのファイルパスを生成
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_file_path = f"capture-image/snapshot_{timestamp}.jpg"
    feature_file_path = f"features_{timestamp}.txt"

    # 画像をキャプチャ・保存
    print(f"{image_file_path} として画像を保存します...")
    picam2.capture_file(image_file_path)
    print("保存が完了しました。")

    # カメラを停止
    picam2.stop()

    # --- ★ここからが追加した処理 ---
    # 撮影した画像から顔特徴量を抽出してファイルに保存する
    extract_and_save_features(image_file_path, feature_file_path)
