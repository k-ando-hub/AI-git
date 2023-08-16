#!/usr/bin/env python3

# ライブラリのインポート
import boto3
import cv2

# 画像のパス
image_path = "./images/004.jpg"

# AWSを使った画像認識
rekognition = boto3.client(service_name="rekognition")
# 画像を読み込んで物体を探す
with open(image_path, "rb") as f:
    detect_text_data = rekognition.detect_labels(
        Image={"Bytes": f.read()},
    )["Labels"]

# 表示用に再度画像を読み込む
image = cv2.imread(image_path)
for d in detect_text_data:
    for b in d["Instances"]:
        x = int(b["BoundingBox"]["Left"] * image.shape[1])
        y = int(b["BoundingBox"]["Top"] * image.shape[0])
        w = int(b["BoundingBox"]["Width"] * image.shape[1])
        h = int(b["BoundingBox"]["Height"] * image.shape[0])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 241, 255), 3)
        image = cv2.putText(image, d["Name"], (x + 10, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 241, 255), thickness=5)
    print("------------------------------------------")
    print("ラベル: {} - {:.1f}％".format(d["Name"], d["Confidence"]))
print("------------------------------------------")

# 画像をリサイズして表示
image = cv2.resize(image, (int(image.shape[1] / 2), int(image.shape[0] / 2)))
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
