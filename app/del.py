#ファイルの作成からの日数が７日を超えたら削除する
import os
import shutil
import glob
import time

def delete_file():
    #ファイルの作成からの日数が７日を超えたら削除する
    now = time.time()
    for f in glob.glob('/home/yakorusu/app/temp/*'):
        if os.stat(f).st_mtime < now - 1 * 86400:
            if os.path.isfile(f):
                os.remove(f)
                print(f)
            elif os.path.isdir(f):
                shutil.rmtree(f)
                print(f)

#常に動かしておく
while True:
    delete_file()
    time.sleep(1)
