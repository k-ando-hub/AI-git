#!/usr/bin/env python3

# 必要なライブラリをインポート
import cv2
import subprocess
import boto3
import wave


class SpeechCamera(object):
    def __init__(self):
        self.image = None
        self.enable_process = False
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def run(self):
        print("=================================================")
        print("[s]キーを押すと画像認識・翻訳・音声合成スタート")
        print("=================================================")
        while True:
            success, image = self.cap.read()
            if success:
                cv2.imshow("Camera", image)
                key = cv2.waitKey(1)
                if key == ord("s"):
                    self.process(image)

    def process(self, image):
        # -------------------------------
        # カメラ画像を保存する
        # -------------------------------
        image_filename = "camera.png"
        cv2.imwrite(image_filename, image)

        # -------------------------------
        # 画像認識して表示用の画像を作成
        # -------------------------------
        detect_data = self.detectLabels(image_filename)
        for d in detect_data:
            for b in d["Instances"]:
                x = int(b["BoundingBox"]["Left"] * image.shape[1])
                y = int(b["BoundingBox"]["Top"] * image.shape[0])
                w = int(b["BoundingBox"]["Width"] * image.shape[1])
                h = int(b["BoundingBox"]["Height"] * image.shape[0])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 241, 255), 2)
                text_size = cv2.getTextSize(d["Name"], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                image = cv2.rectangle(image, (x, y - text_size[0][1] - 10), (x + text_size[0][0], y), (0, 241, 255), -1)
                image = cv2.putText(image, d["Name"], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)

        # -------------------------------
        # 画像認識の結果を翻訳する
        # -------------------------------
        trans_text = ""
        for i in range(len(detect_data)):
            trans_text += detect_data[i]["Name"] + "\n"
        transrate_data = self.transrate(trans_text)
        sp_transrate_data = transrate_data.split("\n")[:-1]

        for i in range(len(detect_data)):
            original_name = detect_data[i]["Name"]
            trans_name = sp_transrate_data[i]
            confidence = detect_data[i]["Confidence"]
            print(trans_name + "({})({:.2f}%)".format(original_name, confidence))
            if i == 4:
                break
        print("=================================================")

        # -------------------------------
        # 翻訳結果の文章化
        # -------------------------------
        text = ""
        for i in range(len(sp_transrate_data)):
            text += sp_transrate_data[i]
            if i == 2:
                break
            else:
                text += ","
        text += "が見つかりました。"

        # -------------------------------
        # 翻訳結果を音声合成する
        # -------------------------------
        speech_data = self.synthesizeSpeech(text)
        speech_filename = "speech.wav"
        wave_data = wave.open(speech_filename, 'wb')
        wave_data.setnchannels(1)
        wave_data.setsampwidth(2)
        wave_data.setframerate(16000)
        wave_data.writeframes(speech_data.read())
        wave_data.close()

        cv2.imshow("Result", image)
        key = cv2.waitKey(100)

        # 保存したWAVデータを再生
        subprocess.check_call('aplay -D plughw:Headphones {}'.format("speech.wav"), shell=True)

        print("=================================================")
        print("[s]キーを押すと画像認識・翻訳・音声合成スタート")
        print("=================================================")

    def detectLabels(self, path):
        # AWSで画像認識
        rekognition = boto3.client("rekognition")
        with open(path, 'rb') as f:
            return rekognition.detect_labels(
                Image={'Bytes': f.read()},
            )["Labels"]
        return []

    def transrate(self, text):
        # AWSで翻訳
        translate = boto3.client(service_name="translate")
        return translate.translate_text(
            Text=text,
            SourceLanguageCode="en",
            TargetLanguageCode="ja"
        )["TranslatedText"]

    def synthesizeSpeech(self, text):
        # AWSで音声合成
        polly = boto3.client(service_name="polly")
        return polly.synthesize_speech(
            Text=text,
            OutputFormat='pcm',
            VoiceId='Mizuki'
        )['AudioStream']


if __name__ == '__main__':
    SpeechCamera().run()
