import time
from datetime import datetime
import numpy as np
from picamera2 import Picamera2
import face_recognition

def find_and_save_features(image_array, output_txt_path):
    try:
        print("画像データから顔を検出しています...")
        face_locations = face_recognition.face_locations(image_array, model="cnn") #ここはhogだと精度が悪い(けどcnnは遅い)

        if not face_locations:
            print("-> 顔が検出されませんでした。")
            return False

        print(f"-> {len(face_locations)} 件の顔を検出しました。")
        if len(face_locations) > 1:
            print("複数の顔が検出されました")
            return False

        face_encodings = face_recognition.face_encodings(image_array, face_locations)

        with open(output_txt_path, 'w') as f:
            print(f"特徴量をファイルに書き込んでいます: {output_txt_path}")

            for i, encoding in enumerate(face_encodings):
                encoding_str = ','.join(map(str, encoding))
                f.write(encoding_str + '\n')
                print(f"  - {i+1}番目の顔の特徴量を保存しました。")

        print("特徴量の保存が完了しました。")
        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1280, 720), "format": "RGB888"})
    picam2.configure(camera_config)

    print("カメラを起動します...")
    picam2.start()
    time.sleep(2)

    print("スナップショットを撮影します...")

    image = picam2.capture_array("main")
    print("撮影が完了しました。")

    picam2.stop()
    print("カメラ終了しました。")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    feature_file_path = f"features_{timestamp}.txt"

    success = find_and_save_features(image, feature_file_path)

    if success:
        print("\n処理が正常に完了しました。")
    else:
        print("\n顔が検出されなかったため、特徴量ファイルは作成されませんでした。")
