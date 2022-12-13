import cv2
import requests
import os
from importlib.resources import path
from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要
import prediction as pi
import calculation as cal
import json

app = FastAPI()


# リクエストbodyを定義
class Image(BaseModel):
    image_url: str
    minkan: List[str] = []
    annkan: List[str] = []
    chi: List[str] = []
    pon: List[str] = []
    chankan: List[str] = []
    nukidora: List[str] = []
    dora: List[str] = []
    ura_dora: List[str] = []
    win_tile: str
    is_tsumo: bool
    is_riichi: bool
    is_ippatsu: bool
    is_rinshan: bool
    is_cahnkan: bool
    is_haitei: bool
    is_houtei: bool
    is_daburu_riichi: bool
    is_nagashi_mangan: bool
    is_tenhou: bool
    is_renhou: bool
    is_chiihou: bool
    player_wind: str
    round_wind: str

# シンプルなJSON Bodyの受け取り


@app.post("/mahjong/predict")
# 上で定義したUserモデルのリクエストbodyをuserで受け取る
# image = {"image_url": "contents/inu.jpg"}
async def create_image(image: Image):
    # 必要な変数
    yaku = {}

    url = image.image_url
    yaku['minkan'] = image.minkan
    yaku['annkan'] = image.annkan
    yaku['chi'] = image.chi
    yaku['pon'] = image.pon
    yaku['chankan'] = image.chankan
    yaku['nukidora'] = image.nukidora
    yaku['dora'] = image.dora
    yaku['ura_dora'] = image.ura_dora
    yaku['win_tile'] = image.win_tile
    yaku['is_tsumo'] = image.is_tsumo
    yaku['is_riichi'] = image.is_riichi
    yaku['is_ippatsu'] = image.is_ippatsu
    yaku['is_rinshan'] = image.is_rinshan
    yaku['is_cahnkan'] = image.is_cahnkan
    yaku['is_haitei'] = image.is_haitei
    yaku['is_houtei'] = image.is_houtei
    yaku['is_daburu_riichi'] = image.is_daburu_riichi
    yaku['is_nagashi_mangan'] = image.is_nagashi_mangan
    yaku['is_tenhou'] = image.is_tenhou
    yaku['is_renhou'] = image.is_renhou
    yaku['is_chiihou'] = image.is_chiihou
    yaku['player_wind'] = image.player_wind
    yaku['round_wind'] = image.round_wind

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

    # 点数計算
    # テストデータ
    hai = ['m2', 'm2', 'm2', 'm2', 'm4', 'm4', 'm4', 'm5',
           'm5', 'm7', 'm7', 'm7', 'm7', 'm9', 'm9', 'm9', 'm9']
    yaku_test = {'minkan': ['m9'], 'annkan': ['m2', 'm7'], 'chi': [], 'pon': [], 'chankan': [], 'nukidora': [], 'dora': ['m1', 'm1', 'm6', 'm8'], 'ura_dora': [], 'win_tile': 'm5', 'is_tsumo': True, 'is_riichi': False, 'is_ippatsu': False,
                 'is_rinshan': True, 'is_cahnkan': False, 'is_haitei': False, 'is_houtei': False, 'is_daburu_riichi': False, 'is_nagashi_mangan': False, 'is_tenhou': False, 'is_renhou': False, 'is_chiihou': False, 'player_wind': '西', 'round_wind': '東'}

    math = cal.Calculation(hai, yaku_test)
    hand = math.print_hand_result()

    # レスポンスbody
    return {"res": "ok", "画像": detections, "han": hand['han'], "fu": hand['fu'], "parent": hand['parent'], "child": hand['child'], "yaku": hand['yaku']}
