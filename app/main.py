from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import make_image
import json

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
@app.get("/make_image2/{text}")
#postされたテキストを受け取る
async def post(text: str):
    #make_image.pyのmake_image関数を呼び出し、画像を生成
    return FileResponse(make_image.make_image(text))  
    
