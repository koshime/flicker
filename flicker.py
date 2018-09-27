import cv2
import sys
import numpy as np
import os
# import file_manager as fima
import matplotlib.pyplot as plt
import time

#フリッカ検出プログラム
def img_flicker(img_dst, num):
    # -------------------------------------------
    # img_dst : 2値化画像
    # num : 例えば80のときは、縦or横において[100-80=20]%以上の太さの黒線をフリッカとして認める。
    # -------------------------------------------
    height = img_dst.shape[0]
    width = img_dst.shape[1]
    thresh = float((100-num)/100)
    # -----------------------------------------------


    # フリッカの検出を行う
    # 2値化画像＝フリッカがあるところ（画素値0）と、ないところ（画素値255）のみの画像なので、→
    # ->fli_xをフリッカでない部分の長さとすると、その部分の画素値の合計は255*fli_xとなる。つまり、これでフリッカの長さがわかる

    # 横方向にフリッカーがあるとして検出
    fli_w = (np.sum(img_dst, axis=1))/255
    fli_w[fli_w <= width * thresh] = 0
    fli_w[fli_w > width * thresh] = 255
    count_w = len(np.where(fli_w==0)[0])  # 上の作業で追加した文字列の数　＝　フリッカの数

    #縦方向にフリッカーがあるとして検出
    fli_h = (np.sum(img_dst, axis=0))/255
    fli_h[fli_h <= height * thresh] = 0
    fli_h[fli_h > height * thresh] = 255
    count_h = len(np.where(fli_h==0)[0])

    # 縦横判定
    if count_h <= count_w:
        for w in range(0, width, 1):
            img_dst[:, w] = fli_w
        img_fli = fli_w
    elif count_h > count_w:
        for h in range(0, height, 1):
            img_dst[h] = fli_h
        img_fli = fli_h
    print("フリッカー検出が終わりました。")









    '''
    # 太さと本数を数える
    # ここでやってることは、代わりにInformationのモジュールでやることにした。
    state = 1
    count_fli = 0 #フリッカの本数
    thickness = [] #フリッカのそれぞれの長さを格納
    thick_avr = 0 #フリッカの長さの平均
    max_count = 0
    thick = 0 # フリッカの一番多い太さ
    for i in img_fli:
        if state == 1:  # 初期状態
            if i == 0:
                count_fli += 1
                thickness.append(1)
                state = 2
            elif i == 255:
                state = 3
        elif state == 2:  # 前にフリッカーがあったとき
            if i == 0:
                thickness[count_fli - 1] += 1
            elif i == 255:
                state = 3
        elif state == 3:  # 前にフリッカーがなかったとき
            if i == 0:
                count_fli +=1
                thickness.append(1)
                state = 2
            elif i == 255:
                state = 3
    '''

    #フリッカの一番多い太さを探す
    # if len(thickness) > 0:
    #     thick_avr = sum(thickness) // len(thickness)
    # st = set(thickness) #リストの中で重複してるのもをなくす
    # for num in st:
    #     c = thickness.count(num)
    #     if c > max_count:
    #         max_count = c
    #         thick = num
    return img_dst  # thickness, count_fli,

def average(list):
    return sum(sum(list))/len(list)

if __name__ == "__main__":
    #ファイルの読み込み
    file = "./" + input("ファイル名を入力してください : ")
    #start = time.time() #時間計測
    file_name = fima.name(file)
    img = fima.image_load(file)
    height = img.shape[0]
    width = img.shape[1]
    path = "./" + file_name
    if not os.path.exists(path):
        os.mkdir(path)

    #グレースケールに変換
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # #画像保存
    # result_file_name = "Q:\\flicker\\python\\data\\photo\\"+file_name+"\\"+file_name+"_gray.jpg"
    # fima.image_save(img_gray, result_file_name)

    # #ヒストグラム作成
    # hist = cv2.calcHist([img],[0],None,[256],[0,256])
    # #保存
    # result_file_name = path+"\\"+file_name+"_hist.jpg"
    # plt.plot(hist)
    # plt.savefig(result_file_name)

    #２値化
    thresh = int(average(img_gray)/2) # しきい値
    max_pixel = 255 # 画素の最大値
    ret, img_dst = cv2.threshold(img_gray, thresh, max_pixel, cv2.THRESH_BINARY)
    print("2値化が終わりました。")

    #フリッカ検出
    thick, img_fli = img_flicker(img_dst)

    #画像の保存
    result_file_name = "./"+file_name+"/"+file_name+"_test.jpg"
    fima.image_save(img_fli, result_file_name)

    #elapsed_time = time.time() - start #時間計測
    #print(str(elapsed_time)+"[sec]")
