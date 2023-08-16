# ライブラリのインポート
import cv2

def detext_color(image_path, target_color):
    
    # 画像の読み込み
    img = cv2.imread(image_path)

    # 画像をBGRからHSVに変換
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 特定の色の範囲を定義
    if target_color.lower() == "green":
        lower_color = (50, 100, 100)
        upper_color = (70, 255, 255)
    elif target_color.lower() == "yellow":
        lower_color = (20, 100, 100)
        upper_color = (30, 255, 255)
    elif target_color.lower() == "red":
        lower_color = (0, 100, 100)
        upper_color = (10, 255, 255)
    
    # 特定の色の範囲内にあるピクセルをマスク
    mask = cv2.inRange(hsv_img, lower_color, upper_color)

    # マスクされた画像を表示するかどうか判定
    if cv2.countNonZero(mask) > 0:
        if target_color.lower() == "green":
            print("OK: システムは正常に稼働しています。")
    if cv2.countNonZero(mask) > 0:
        if target_color.lower() == "yellow":
            print("Warning: システムの異常を警告します。")
    if cv2.countNonZero(mask) > 0:
        if target_color.lower() == "red":
            print("Danger: システムが危険な状態です。")

# 画像ファイルと対象の色を指定して関数を呼び出す
detext_color("001.jpg", "green")
detext_color("002.jpg", "green")
detext_color("003.jpg", "yellow")
detext_color("004.jpg", "red")
