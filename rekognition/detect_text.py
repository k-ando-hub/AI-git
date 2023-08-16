#!/usr/bin/env python3

# ライブラリのインポート
import boto3
import cv2

# 画像のパス
image_path = "./images/001.jpg"

# # AWSを使った画像認識
rekognition = boto3.client(service_name="rekognition")

# 画像を読み込んで、画像中からテキストを探す
with open(image_path, "rb") as f:
    detect_text_data = rekognition.detect_text(
        Image={"Bytes": f.read()},
    )["TextDetections"]

# 表示用に再度画像を読み込む
image = cv2.imread(image_path)
for d in detect_text_data:
    if d["Type"] == "WORD":
        print("------------------------------------------")
        print("検出された単語: {}".format(d["DetectedText"]))
        x = int(d["Geometry"]["BoundingBox"]["Left"] * image.shape[1])
        y = int(d["Geometry"]["BoundingBox"]["Top"] * image.shape[0])
        w = int(d["Geometry"]["BoundingBox"]["Width"] * image.shape[1])
        h = int(d["Geometry"]["BoundingBox"]["Height"] * image.shape[0])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 241, 255), 3)
        image = cv2.putText(image, d["DetectedText"], (x, y + h + 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 241, 255), thickness=5)
print("------------------------------------------")
# 画像をリサイズして表示
image = cv2.resize(image, (int(image.shape[1] / 2), int(image.shape[0] / 2)))
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
