import requests,bs4
from rich import print,logging,pretty,inspect
from rich.console import Console
import re

baken_kind = {
    0: "Tansho",
    1: "Fukusho",
    2: "Wakuren",
    3: "Umaren",
    4: "Wide",
    5: "Umatan",
    6: "Fuku3",
    7: "Tan3",
}

def baken_payout(race_id:str, baken_id:int, horse_number1:int, horse_number2:int, horse_number3:int)->int:
    #中央レース情報を取得する
    url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.content, 'html.parser')
    result = soup.find_all(class_ = baken_kind[baken_id])
    result_result = result[0].find_all(class_ = "Result")
    result_result = result_result[0].text.split("\n")
    result_result = [i for i in result_result if i != ""]
    result_payout = result[0].find_all(class_ = "Payout")
    result_payout = result_payout[0].text.split("円")
    result_payout = [i for i in result_payout if i != ""]

    #枠連の場合は払い戻し結果がない場合があるので、払い戻し結果がない場合は0を返す
    if len(result_result) == 0:
        return 0
    
    #払い戻しを計算する
    #単勝
    if baken_id == 0:
        hit = str(horse_number1) in result_result
        if not hit:
            payout = 0
        else:
            payout =  int(result_payout[0].replace(",",""))
    #複勝
    elif baken_id == 1:
        index = result_result.index(str(horse_number1)) if str(horse_number1) in result_result else -1
        if index == -1:
            payout = 0
        else:
            payout =  int(result_payout[index].replace(",",""))
    #枠連
    elif baken_id == 2:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #馬連
    elif baken_id == 3:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #ワイド
    elif baken_id == 4:
        result_result = [result_result[i:i+2] for i in range(0, len(result_result), 2)]
        index = [i for i in result_result if str(horse_number1) in i and str(horse_number2) in i]
        if len(index) == 0:
            payout = 0
        else:
            payout = int(result_payout[result_result.index(index[0])].replace(",",""))
    #馬単
    elif baken_id == 5:
        hit = (str(horse_number1) == result_result[0]) and (str(horse_number2) == result_result[1])
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #三連複
    elif baken_id == 6:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result) and (str(horse_number3) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #三連単
    elif baken_id == 7:
        hit = (str(horse_number1) == result_result[0]) and (str(horse_number2) == result_result[1]) and (str(horse_number3) == result_result[2])
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    
    return payout

def baken_nar_payout(race_id:str, baken_id:int, horse_number1:int, horse_number2:int, horse_number3:int)->int:
    #中央レース情報を取得する
    url = f"https://nar.netkeiba.com/race/result.html?race_id={race_id}"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.content, 'html.parser')
    result = soup.find_all(class_ = baken_kind[baken_id])
    result_result = result[0].find_all(class_ = "Result")
    result_result = result_result[0].text.split("\n")
    result_result = [i for i in result_result if i != ""]
    result_payout = result[0].find_all(class_ = "Payout")
    result_payout = result_payout[0].text.split("円")
    result_payout = [i for i in result_payout if i != ""]

    #枠連の場合は払い戻し結果がない場合があるので、払い戻し結果がない場合は0を返す
    if len(result_result) == 0:
        return 0
    
    #払い戻しを計算する
    #単勝
    if baken_id == 0:
        hit = str(horse_number1) in result_result
        if not hit:
            payout = 0
        else:
            payout =  int(result_payout[0].replace(",",""))
    #複勝
    elif baken_id == 1:
        index = result_result.index(str(horse_number1)) if str(horse_number1) in result_result else -1
        if index == -1:
            payout = 0
        else:
            payout =  int(result_payout[index].replace(",",""))
    #枠連
    elif baken_id == 2:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #馬連
    elif baken_id == 3:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #ワイド
    elif baken_id == 4:
        result_result = [result_result[i:i+2] for i in range(0, len(result_result), 2)]
        index = [i for i in result_result if str(horse_number1) in i and str(horse_number2) in i]
        if len(index) == 0:
            payout = 0
        else:
            payout = int(result_payout[result_result.index(index[0])].replace(",",""))
    #馬単
    elif baken_id == 5:
        hit = (str(horse_number1) == result_result[0]) and (str(horse_number2) == result_result[1])
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #三連複
    elif baken_id == 6:
        hit = (str(horse_number1) in result_result) and (str(horse_number2) in result_result) and (str(horse_number3) in result_result)
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))
    #三連単
    elif baken_id == 7:
        hit = (str(horse_number1) == result_result[0]) and (str(horse_number2) == result_result[1]) and (str(horse_number3) == result_result[2])
        if not hit:
            payout = 0
        else:
            payout = int(result_payout[0].replace(",",""))

    return payout


if __name__ == "__main__":
    print(baken_payout("202304020211", 7, 3, 10, 2))
    print(baken_nar_payout("202335080611", 7, 4, 10, 6))