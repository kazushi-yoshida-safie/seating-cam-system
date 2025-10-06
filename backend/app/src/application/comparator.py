import numpy as np

class FaceComparator:
    """
    2つの顔特徴量ベクトル間の類似度を計算する責務を持つクラス。
    """

    def _parse_encoding_str(self, encoding_str: str) -> np.ndarray:
        """
        カンマ区切りの文字列をNumPyの数値配列（ベクトル）に変換する。
        """
        try:
            return np.array([float(num) for num in encoding_str.split(',')])
        except (ValueError, TypeError):
            # 不正な形式の文字列が来た場合に空の配列を返す
            return np.array([])

    def calculate_distance(self, encoding_from_pi_str: str, encoding_from_db_str: str) -> float:
        """
        2つの文字列形式の顔特徴量からユークリッド距離を計算する。

        Args:
            encoding_from_pi_str (str): ラズパイから送られてきた顔特徴量。
            encoding_from_db_str (str): データベースから取得した顔特徴量。

        Returns:
            float: 2つの特徴量ベクトル間のユークリッド距離。
                   距離が小さいほど似ていると判断できる。
                   不正な入力の場合は非常に大きな値を返す。
        
        ---
        特徴量精度は後でここをいじる
        """
        # 1. 両方の文字列を数値ベクトルに変換
        pi_vector = self._parse_encoding_str(encoding_from_pi_str)
        db_vector = self._parse_encoding_str(encoding_from_db_str)

        # 2. ベクトルが正常に変換できたか、次元数が同じかを確認
        if pi_vector.size == 0 or db_vector.size == 0 or pi_vector.shape != db_vector.shape:
            return float('inf') # 比較不能な場合は無限大（最大値）を返す

        # 3. 2つのベクトル間のユークリッド距離を計算して返す
        distance = np.linalg.norm(pi_vector - db_vector)
        return distance