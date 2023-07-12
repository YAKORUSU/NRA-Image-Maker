from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
import make_image

app = FastAPI()

@app.get("/")
async def get():
    return {"Result": "Server_ok"}

#Postリクエストが来たら、"make_image"という関数を呼び出し引数としてJsonを渡す
@app.post("/make_image")
#postされたJsonを受け取る
async def post(json: dict):
    #Jsonを文字列に変換
    json_str = str(json)
    #make_image.pyのmake_image関数を呼び出し、画像を生成
    return FileResponse(make_image.make_image(json_str))  
    
