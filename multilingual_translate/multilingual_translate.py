#!/usr/bin/env python3

# 必要なライブラリをインポート
from flask import Flask, render_template, request
import boto3

# Flaskを使用する準備
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/translate", methods=["GET"])
def translate_function():
    """メッセージを貰って任意の処理を実行する関数"""
    # Webアプリ側から送られてきたテキストを取得する
    input_text = request.args.get("input_text")
    source_lang = request.args.get("source_lang")
    target_lang = request.args.get("target_lang")

    print("input_text={}".format(input_text))

    # AWSを使った翻訳の準備
    translate = boto3.client(service_name="translate")
    # テキストを翻訳
    translate_text = translate.translate_text(
        Text=input_text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )["TranslatedText"]

    print("translate_text={}".format(translate_text))

    # Webアプリに翻訳したテキストを送り返す
    return translate_text
    

@app.route("/")
def main():
    """トップページにアクセスしたときに実行される関数"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
