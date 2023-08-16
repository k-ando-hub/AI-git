#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

# ライブラリのインポート
import boto3

def detect_text(image_path, target_text):

    # Amazon Rekognitionに接続
    client=boto3.client('rekognition')
   
   # 画像をバイトデータとして読み込み、画像内のテキストを検出
    with open(image_path, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    
    # 検出されたテキストを取得
    text_instances = [text['DetectedText'] for text in response['TextDetections']]

    # 指定した文字列が含まれているか確認
    if target_text in text_instances:
        return f'{target_text}'
    elif target_text in text_instances:
        return f'{target_text}'
    elif target_text in text_instances:
        return f'{target_text}'
    else:
        return f"画像内に'{target_text}'は見つかりませんでした。"

# 画像ファイルのパスと特定の文字列を指定
image_path = "001.jpg"
target_text = "OK"

# テキストを検出して結果を出力
result = detect_text(image_path, target_text)
print(result)