from PIL import Image, ImageDraw, ImageFont
import json
import tempfile
import qrcode
import os
import pdb
import random

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
place_font = ImageFont.truetype("/home/yakorusu/app/font/new_tamanegi.ttf", 73)  #開催場所のフォント,HGSMinchoEフォントを使用
hose_number_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 60) #馬番号のフォント
day_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 45) #開催日のフォント,IPAexGothicフォントを使用
issue_date_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 40)  #発売日のフォント,HGSMinchoEフォントを使用
race_number_font = ImageFont.truetype("/home/yakorusu/app/font/Inter-Bold.ttf", 76) #レース番号のフォント,Inter Boldフォントを使用
horse_number_font = ImageFont.truetype("/home/yakorusu/app/font/Inter-Bold.ttf", 76) #馬番号のフォント
money_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 37) #金額のフォント,IPAexGothicフォントを使用
number_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 37) #枚数のフォント,IPAexGothicフォントを使用
random_number_font = ImageFont.truetype("/home/yakorusu/app/font/ipaexg.ttf", 33) #ランダムな数列のフォント,IPAexGothicフォントを使用


def make_image(json_str:str)->str:
    # 文字列(json_str)をJsonに変換
    json_dict = json.loads(json_str)

    # json_dictから必要な情報を取得
    # 発行日
    issue_date = json_dict["issue_date"]
    
    # 開催日
    date = json_dict["date"]

    # 開催場所
    place = json_dict["place"]

    # レース番号
    race_number = int(json_dict["race_number"])

    # 金額
    money = f'{json_dict["money"]}'
    # 7桁で指定しているため、金額が7桁に満たない場合は星で埋める
    if len(money) >= 7:
        money_str = money
    else:
        stars = '★' * (7 - len(money))
        money_str = stars + money

    # 馬番の横の金額
    if len(money) >= 6:
        money2_str = money
    else:
        stars = '☆' * (6 - len(money))
        money2_str = stars + money

    # 枚数(1組10円のため金額から除法で計算)
    number = f'{json_dict["money"] // 10}'
    print(number)
    # 6桁で指定しているため、金額が6桁に満たない場合は星で埋める
    if len(number) >= 6:
        number_str = number
    else:
        star = '★' * (6 - len(number))
        number_str = star + number


    # 投票形式
    vote_type = int(json_dict["vote_type"])
    vote = vote_type_str[vote_type]

    #40桁のランダムな数列を生成
    random_number = str(random.randrange(10**40))

    # 画像の呼び出し ~\img\{vote}.png"
    image_name = f"/home/yakorusu/app/img/{vote}.png"
    image = Image.open(image_name)
    draw = ImageDraw.Draw(image)

    #開催日の描画
    day_text = date
    day_text_color = (0, 0, 0)#黒
    day_text_x = 38.0
    day_text_y = 19.0
    draw.text((day_text_x, day_text_y), day_text, font=day_font, fill=day_text_color)

    #開催場所の描画
    place_text = place
    place_text_color = (0, 0, 0)#黒
    place_text_x = 32.0
    place_text_y = 74.0
    draw.text((place_text_x, place_text_y), place_text, font=place_font, fill=place_text_color)

    #レース番号の描画
    race_number_text = race_number
    race_number_text_color = (255, 255, 255)#白
    #レース番号が1桁の場合と2桁の場合で位置を変える
    if len(str(race_number)) == 1:
        race_number_text_x = 90.0
        race_number_text_y = 148.0
    else:
        race_number_text_x = 70.0
        race_number_text_y = 148.0
    draw.text((race_number_text_x, race_number_text_y), str(race_number_text), font=race_number_font, fill=race_number_text_color)

    #金額の描画
    money_text = money_str
    money_text_color = (0, 0, 0)#黒
    money_text_x = 850.0
    money_text_y = 595.0
    draw.text((money_text_x, money_text_y), money_text, font=money_font, fill=money_text_color)

    #金額２の描画
    money2_text = money2_str
    money2_text_color = (0, 0, 0)#黒
    money2_text_x = 880.0
    money2_text_y = 260.0
    draw.text((money2_text_x, money2_text_y), money2_text, font=money_font, fill=money2_text_color)

    #枚数の描画
    number_text = number_str
    number_text_color = (0, 0, 0)#黒
    number_text_x = 560.0
    number_text_y = 595.0
    draw.text((number_text_x, number_text_y), number_text, font=number_font, fill=number_text_color)

    #日付の描画
    #20230716を07月16日に変換
    issue_date_str = str(issue_date)
    issue_date_text = issue_date_str[4:6] + "月" + issue_date_str[6:8] + "日"
    issue_date_text_color = (0, 0, 0)#黒
    issue_date_text_x = 43.0
    issue_date_text_y = 625.0
    draw.text((issue_date_text_x, issue_date_text_y), issue_date_text, font=issue_date_font, fill=issue_date_text_color)

    #40文字のランダムな数字の描画
    random_number_text = random_number[0:12] + " " + random_number[13:25] + " " + random_number[26:33] + " " + random_number[34:39]
    random_number_text_color = (0, 0, 0)#黒
    random_number_text_x = 330.0
    random_number_text_y = 635.0
    draw.text((random_number_text_x, random_number_text_y), random_number_text, font=random_number_font, fill=random_number_text_color)

    #QRコードの描画を２つ行う
    #QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )
    qr.add_data(random_number)
    qr.make(fit=True)
    #背景は透明にする
    qr_img = qr.make_image(fill_color="black", back_color="White")
    #QRコードのサイズを変更
    qr_img = qr_img.resize((150, 150))
    #QRコードの描画
    image.paste(qr_img, (32, 265))

    #QRコードの生成
    qr2 = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )
    qr2.add_data(random_number_text)
    qr2.make(fit=True)
    #背景は透明にする
    qr2_img = qr2.make_image(fill_color="black", back_color="White")
    #QRコードのサイズを変更
    qr2_img = qr2_img.resize((150, 150))
    #QRコードの描画
    image.paste(qr2_img, (230, 265))

    #馬番号の描画
    horse_number1 = json_dict["buy"]["horse_number1"]
    horse_number2 = json_dict["buy"]["horse_number2"]
    horse_number3 = json_dict["buy"]["horse_number3"]

    #投票形式ごとで分岐)
    if vote == "単勝" or vote == "複勝":
        horse_number1_color = (0, 0, 0)#黒
        #馬番号が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number1)) == 1:
            horse_number1_x = 590.0
            horse_number1_y = 210.0
        else:
            horse_number1_x = 572.0
            horse_number1_y = 210.0
        draw.text((horse_number1_x, horse_number1_y), str(horse_number1), font=horse_number_font, fill=horse_number1_color) 
        
    elif vote == "枠連" or vote == "馬連" or vote == "ワイド" or vote == "馬単":
        #枠連の場合は白、それ以外は黒
        if vote == "枠連":
            horse_number1_color = (255, 255, 255)
            horse_number2_color = (255, 255, 255)
        else:
            horse_number1_color = (0, 0, 0)
            horse_number2_color = (0, 0, 0)
        #馬番号1が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number1)) == 1:
            horse_number1_x = 590.0
            horse_number1_y = 210.0
        else:
            horse_number1_x = 572.0
            horse_number1_y = 210.0
        draw.text((horse_number1_x, horse_number1_y), str(horse_number1), font=horse_number_font, fill=horse_number1_color)
        #馬番号2が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number2)) == 1:
            horse_number2_x = 768.0
            horse_number2_y = 210.0
        else:
            horse_number2_x = 748.0
            horse_number2_y = 210.0
        draw.text((horse_number2_x, horse_number2_y), str(horse_number2), font=horse_number_font, fill=horse_number2_color)

    elif vote == "三連複" or vote == "三連単":
        horse_number1_color = (0, 0, 0)
        horse_number2_color = (0, 0, 0)
        horse_number3_color = (0, 0, 0)
        #馬番号1が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number1)) == 1:
            horse_number1_x = 590.0
            horse_number1_y = 210.0
        else:
            horse_number1_x = 572.0
            horse_number1_y = 210.0
        draw.text((horse_number1_x, horse_number1_y), str(horse_number1), font=horse_number_font, fill=horse_number1_color)

        #馬番号2が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number2)) == 1:
            horse_number2_x = 685.0
            horse_number2_y = 210.0
        else:
            horse_number2_x = 666.0
            horse_number2_y = 210.0
        draw.text((horse_number2_x, horse_number2_y), str(horse_number2), font=horse_number_font, fill=horse_number2_color)

        #馬番号3が1桁の場合と2桁の場合で位置を変える
        if len(str(horse_number3)) == 1:
            horse_number3_x = 780.0
            horse_number3_y = 210.0
        else:
            horse_number3_x = 760.0
            horse_number3_y = 210.0
        draw.text((horse_number3_x, horse_number3_y), str(horse_number3), font=horse_number_font, fill=horse_number3_color)



    # 画像をtempフォルダに保存
    data_dir = "/home/yakorusu/app/temp"
    os.makedirs(data_dir, exist_ok=True)
    save_filename = f"{data_dir}/{issue_date}.png"
    image.save(save_filename)


    testprint = date + "," + place + "," + str(race_number) + "," + money_str + "," + number_str + "," + vote
    return save_filename


# test
data = {"issue_date": 20230713,"date" : "20xx年x回x日","place" : "東京","race_number" : 5,"money" : 100,"vote_type" : 7,"buy" : {"horse_number1" : 2,"horse_number2" : 10,"horse_number3" : 18}}
json_str = json.dumps(data)
race_result = make_image(json_str)
print(race_result)
# print(json_str)
