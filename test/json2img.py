from PIL import Image, ImageDraw, ImageFont
import json
import tempfile
import qrcode
import os

vote_type_str = {
    1: "単勝",
    2: "複勝",
    3: "枠連",
    4: "馬連",
    5: "ワイド",
    6: "馬単",
    7: "三連複",
    8: "三連単",
}

# フォントの定義
place_font = ImageFont.truetype("./new_tamanegi.ttf", 40)  #フォントのパスとサイズを指定
number_font = ImageFont.truetype("path/to/font.ttf", 60) #馬番号のフォント
day_font = ImageFont.truetype("path/to/font.ttf", 40) #開催日のフォント
vote_font = ImageFont.truetype("path/to/font.ttf", 40) #投票形式のフォント
money_font = ImageFont.truetype("path/to/font.ttf", 40) #金額のフォント



def make_image(json_str:str)->str:
    #json_strを辞書型に変換
    json_dict = json.loads(json_str)
    

    #json_dictから必要な情報を取得
    #開催日
    date = json_dict["date"]

    #開催場所
    place = json_dict["place"]

    #レース番号
    race_number = int(json_dict["race_number"])

    #金額
    money = int(json_dict["money"])
    #7桁で指定しているため、金額が7桁に満たない場合は星で埋める
    if len(money) >= 7:
        money_str = money
    else:
        stars = '☆' * (7 - len(money))
        money_str = stars + money

    #枚数(1組10円のため金額から除法で計算)
    number = money / 10


    #投票形式
    vote_type = int(json_dict["vote_type"])
    vote = vote_type_str[vote_type]

    # 画像の生成
    image = "~\Image\{vote}.png".format(vote=vote)
    draw = ImageDraw.Draw(image)

    #開催日の描画
    day_text = date
    day_text_color = (0, 0, 0)
    day_text_x = 20
    day_text_y = 20
    draw.text((day_text_x, day_text_y), day_text, font=day_font, fill=day_text_color)

    


    #馬番号
    if vote == "単勝" or vote == "複勝":
        horse_number1 = json_dict["buy"]["horse_number1"]

        # 馬番号の描画


    elif vote == "枠連" or vote == "馬連" or vote == "ワイド" or vote == "馬単":
        horse_number1 = json_dict["buy"]["horse_number1"]
        horse_number2 = json_dict["buy"]["horse_number2"]

    elif vote == "三連複" or vote == "三連単":
        horse_number1 = json_dict["buy"]["horse_number1"]
        horse_number2 = json_dict["buy"]["horse_number2"]
        horse_number3 = json_dict["buy"]["horse_number3"]
    

    # テキストの描画
    text = "馬券"
    font_size = 40
    font = ImageFont.truetype("path/to/font.ttf", font_size)  # フォントのパスを指定
    text_color = (0, 0, 0)
    text_x = (width - draw.textsize(text, font=font)[0]) // 2  # 中央に配置するための計算
    text_y = (height - draw.textsize(text, font=font)[1]) // 2
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # 枠線の描画
    border_color = (0, 0, 0)
    border_width = 5
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline=border_color, width=border_width)

    # 番号の描画
    number_text = "123"
    number_font_size = 60
    number_font = ImageFont.truetype("path/to/font.ttf", number_font_size)  # フォントのパスを指定
    number_text_color = (0, 0, 0)
    number_text_x = 20
    number_text_y = (height - draw.textsize(number_text, font=number_font)[1]) // 2
    draw.text((number_text_x, number_text_y), number_text, font=number_font, fill=number_text_color)

    # 画像の一時保存
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as image:
        temp_filename = image.name
        image.save(draw)

    # im
    return temp_filename
