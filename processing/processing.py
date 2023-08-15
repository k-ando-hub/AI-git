#!/usr/bin/env python3

# 必要なライブラリをインポート
from flask import Flask, render_template, Response
from datetime import datetime, timezone, timedelta
import cv2
import os
import boto3


# Flaskを使用する準備
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# AWSの準備
rekognition_client = boto3.client(service_name="rekognition")

# カメラの準備
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# フィルタ画像を読み込む
happy_image = cv2.imread("effects/happy.png", cv2.IMREAD_UNCHANGED)
donyori_image = cv2.imread("effects/donyori.png", cv2.IMREAD_UNCHANGED)

# 画像データを置く場所を作成
if not os.path.isdir("static/datas"):
    os.makedirs("static/datas")


# トップページにアクセスしたときに実行される関数
@app.route("/")
def main():
    return render_template("index.html")


# カメラ映像をストリーミングする関数
def camera_stream():
    while True:
        success, image = camera.read()
        b_image = cv2.imencode(".JPG", image)[1].tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + b_image + b"\r\n")
    camera.release()

@app.route("/stream")
def video_stream_function():
    return Response(camera_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")

# 2枚の画像を合成して加工する関数
def kakou_image(s_image, e_image):
    g_image = s_image * (1 - e_image[:, :, 3:] / 255) + e_image[:, :, :3] * (e_image[:, :, 3:] / 255)
    return g_image.astype("uint8")


# 撮影＆分析ボタンが押されたときに実行される関数
@app.route("/kakou", methods=["GET"])
def kakou_function():
    # OpenCVでカメラ映像の撮影
    success, image = camera.read()

    # AWSで表情認識
    detect_faces_response = rekognition_client.detect_faces(
        Image={"Bytes": cv2.imencode(".PNG", image)[1].tobytes()}, 
        Attributes=["ALL"]
    )["FaceDetails"]

    # 1個以上、認識できていたら処理を実行
    if len(detect_faces_response) > 0:
        # 表情データのみ取り出す
        emotion = detect_faces_response[0]["Emotions"][0]["Type"]
        print("emotion={}".format(emotion))
        
        # HAPPY: 幸せ | SAD: 悲しい | ANGRY: 怒り | CONFUSED: 困惑 | DISGUSTED: うんざり | SURPRISED: 驚き | CALM: 穏やか | FEAR: 不安

        # 表情に応じてエフェクトをつける
        if emotion == "HAPPY":
            # 画像を合成する
            image = kakou_image(image, happy_image)
        
        if emotion == "SAD" or emotion == "DISGUSTED" or emotion == "FEAR":
            # 画像を合成する
            image = kakou_image(image, donyori_image)
    
    else:
        # 顔が検出されなかったら、表情は無しにする
        emotion = "無し"

    # ファイル名のためにタイムスタンプを作成
    timestamp = datetime.now(timezone(timedelta(hours=9), "JST")).strftime("%Y%m%d_%H%M%S")
    # ファイル名（ファイルパス）を決める
    image_path = "static/datas/{}.jpg".format(timestamp)

    # 画像を保存
    cv2.imwrite(image_path, image)

    # 画像のパスを送り返す
    return image_path


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
