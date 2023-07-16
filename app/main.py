from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse
from typing import Optional, Dict
import make_image
import json
import urllib.parse

app = FastAPI()


@app.get("/")
async def get():
    return {"Result": "Server_ok"}

#Postリクエストが来たら、"make_image"という関数を呼び出し引数としてJsonを渡す
@app.post("/make_image")
#postされたJsonを受け取る
async def post(request: Request):
    json_data = await request.json()
    #jsonを文字列に変換
    json_str = json.dumps(json_data)
    #make_image.pyのmake_image関数を呼び出し、画像を生成
    return FileResponse(make_image.make_image(json_str))  

#Clientの画像取得がPOSTに対応していなかったときのためにGETでも画像を生成できるようにする
@app.get("/make_image3/{id}/{issue}/{deta}/{place}/{race_number}/{money}/{vote_type}/{horse_number1}/{horse_number2}/{horse_number3}")
async def get(id: int, issue: int, deta: str, place: str, race_number: int, money: int, vote_type: int, horse_number1: int, horse_number2: int, horse_number3: int):
    json_data = {
        "id": id, #追加
        "issue_date": issue,
        "date": urllib.parse.unquote(f"{deta}"),
        "place": urllib.parse.unquote(f"{place}"),
        "race_number": race_number,
        "money": money,
        "vote_type": vote_type,
        "buy": {
            "horse_number1": horse_number1,
            "horse_number2": horse_number2,
            "horse_number3": horse_number3
        }
    }
    print(json_data)
    json_str = json.dumps(json_data)
    return FileResponse(make_image.make_image(json_str))
