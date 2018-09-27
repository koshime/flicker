# 1フレームごとにフリッカ検出を行う
import cv2
import sys
import numpy as np
import os
import flicker as fler
import xlrd #excelの読み込み
import xlwt #excelへの書き込み
import shutil


# ---------------------------------------------------------------------
# 引数の説明です
# width : 幅
# height : 高さ
# num : フレーム数
# img_name : イメージそのものの名前（差分画像名の作成）
# dir_name : イメージが保存されてるディレクトリ名（差分画像を保存するためのフォルダパス作成にのみ使用）
# dir_path_gray : 差分画像を作成するための元画像のフォルダパス
# 　　　　　　　　'./' + dir_name + "_gray" + '/'
# ---------------------------------------------------------------------

def deguchi(height, width, num, dir_path_gray, img_name, dir_name):

    # 直前のフレームを定義
    preframe = np.zeros((int(height), int(width)), np.uint8)
    thresh = -5  # しきい値
    thresh_fler = 80  # 「flicker」を起動する際に入力する引数の部分

    # -----------------------------------------------------------------------
    # 検出後の画像を保存するためのフォルダを作成
    dir_path_diff = "./" + dir_name + "_diff" + "/"

    # イメージを保存するディレクトリがすでにあったらディレクトリツリーを削除
    if os.path.exists(dir_path_diff):
        shutil.rmtree(dir_path_diff)
    # 存在しないなら作成
    if not os.path.exists(dir_path_diff):
        os.makedirs(dir_path_diff)
    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------
    # エクセルに書き込むための作業？
    # book = xlwt.Workbook()
    # Sheet_1 = book.add_sheet('NewSheet_1')
    # Sheet_1.write(0, 0, "画像番号")
    # Sheet_1.write(0, 1, "フリッカの太さ")
    # -----------------------------------------------------------------------
    # 差分検出を行うところ
    i = 0
    while i < num:
        if num > 0:
            # 画像へアクセスする準備（パスの作成）
            img_path_gray = dir_path_gray + img_name + '_gray_%s.png' % str(i).zfill(4)
            # 画像の読み込み（グレースケールで）
            frame = cv2.imread(img_path_gray, 0)
            # 画像の絶対値を求める。（比較相手は直前のフレーム）
            img_diff = cv2.absdiff(frame, preframe)
            # 差分からフリッカ検出
            # しきい値以下の画素→0（黒）, それ以外を255（白）
            img_diff[img_diff >= frame - thresh] = 0
            img_diff[img_diff != 0] = 255
            print(str(i) + ":", end="")
            # flicker（ここではfler）というモジュールが存在していて、それを使っている。
            # ここに８０という引数を入力しているが、これはフリッカの許容量を示す数字（詳しくは該当モジュール参照）
            img_diff = fler.img_flicker(img_diff, thresh_fler)  # thickness, count_fli,

            # ----------------------------------------------------------------------------------------------------------
            # エラーが起きている画像を治す。
            # img_err : 異常が起きている（かもしれない）画像
            # フリッカに直行する部分を検出→エラー画像とみなし、前の画像で上書きするか、無視する。
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            # 検出後の画像を保存
            path_write = dir_path_diff + img_name + '_diff_%s.png' % str(i).zfill(4)
            cv2.imwrite(path_write, img_diff)
            # ----------------------------------------------------------------------------------------------------------
#            # Excelへの書き込み
#            Sheet_1.write(i + 1, 0, i)
#            if isinstance(thickness, list):  # isinstanceを使って、thicknessがlist型かどうかを確かめている。
#                for n, m in enumerate(thickness):
#                    Sheet_1.write(i + 1, n + 1, m)
#            elif isinstance(thickness, int):
#                Sheet_1.write(i + 1, 1, thickness)
#        else:
#            # Excelへの書き込み
#            Sheet_1.write(1, 0, 0)
#            Sheet_1.write(1, 1, 0)

# ----------------------------------------------------------------------------------------------------------
        # インクリメント→preframeを現在のフレームで上書き→次へ
        i += 1
        preframe = frame
# ----------------------------------------------------------------------------------------------------------

#    book.save(dir_path_diff + '_flicker.xls')
