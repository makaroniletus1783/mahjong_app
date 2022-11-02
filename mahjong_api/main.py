from importlib.resources import path
from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要

app = FastAPI()


# リクエストbodyを定義
class Image(BaseModel):
    image_url: str


# シンプルなJSON Bodyの受け取り
@app.post("/mahjong/predict")
# 上で定義したUserモデルのリクエストbodyをuserで受け取る
# image = {"path": "contents/inu.jpg"}
def create_image(image: Image):
    # レスポンスbody
    return {"res": "ok", "画像": image.image_url}
