# NRA-Image-Maker
## Motivation
VR内競馬場にて馬券の発行を行う際にVR内で画像を処理させると重くなってしまうため、サーバー内で何とかできないかという話がありました。
Pythonを使用して画像の編集をすることができることがわかり実践してみることにしました。

## OverView

POSTされたJsonを元に馬券の画像を作成しリターンを行います。

- 購入内容を乗せたJsonを受け取るエンドポイント(POST)
- 画像をリアルタイムでレンダリングするイメージレンダラー

## Infrastructure

### APIエンドポイント
エンドポイントはテスト用と実運用の２つを作成する。
```Shell
#通信テスト時
http://{$hostname}:8000/
#馬券生成時
http://{$hostname}:8000/make_image3/{id}/{issue}/{deta}/{place}/{race_number}/{money}/{vote_type}/{horse_number1}/{horse_number2}/{horse_number3}/

#レスポンス
http://{$hostname}:8030/{uid}.png
```
//TODO

### サーバ情報

- ConoHaVPS (vCPU:1,Mem:512MB)

#### webサーバ

- nginx
  - 8000にてListen

#### ASGIサーバ

- gunicorn
- uvicorn

##### プロセス管理

- systemdにてgunicornをデーモン化
- gunicornではuvicornをマルチプロセス化して起動

#### ファイアウォール

- ufwにて制御

## Application

### 技術仕様

- 言語：Pytnon3系
- フレームワーク：FastAPI

### 馬券生成フロー
1. クライアントよりJsonがPOSTされる
2. POSTされたデータを`string`にして呼び出した`make_image`モジュールの`make_image`関数に引き渡す。
3. `String`を`Json`に戻し内容を馬券に記載するフォーマットに書き換える
4. 写真を呼び出し貼り付けを行い`.png`でTmpに保存する
5. `FileResponse`でクライアントに返す。

## About
//TODO
