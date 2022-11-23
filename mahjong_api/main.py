import cv2
import requests
import os
from importlib.resources import path
from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要
import prediction as pi

app = FastAPI()


# リクエストbodyを定義
class Image(BaseModel):
    image_url: str
    is_richi: bool


# シンプルなJSON Bodyの受け取り
@app.post("/mahjong/predict")
# 上で定義したUserモデルのリクエストbodyをuserで受け取る
# image = {"image_url": "contents/inu.jpg"}
def create_image(image: Image):
    url = image.image_url
    is_richi = image.is_richi
    response = requests.get(url)
    im = response.content

    file_name = "test.jpg"
    with open(file_name, "wb") as f:
        f.write(im)

    # 以下で画像の推論
    file = './test.jpg'
    image = cv2.imread(file, cv2.IMREAD_COLOR)
    detections = pi.detect(image, pi.mahjong_labels)

    os.remove(file_name)

    # レスポンスbody
    return {"res": "ok", "画像": detections, "リーチ": is_richi}
