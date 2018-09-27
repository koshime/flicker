import os
import shutil
import cv2
from F_D_deguchi import deguchi

# グレースケール画像で動画をフレームごとに抽出するためのモジュール
# 基本的にはM2FandGのほうが正規のプログラムで、こっちは簡易にグレースケール画像のみを生み出すことを目的としたプログラム（あくまで今のところは）

def video_2_grays(video_file: str, name: str):
    # -------------------------------------------------------------
    # 入力をもとにディレクトリのパスを生成
    # ビデオのアドレス
    video_path = './movie/' + video_file
    # 画像を保存するフォルダのアドレス
    dir_path_gray = './' + name + '_gray/'
    # 保存画像の名前
    file_name = name + '_gray' + '_%s.png'
    # イメージを保存するディレクトリがすでにあったらディレクトリツリーを削除
    if os.path.exists(dir_path_gray):
        shutil.rmtree(dir_path_gray)
    # 存在しないなら作成
    if not os.path.exists(dir_path_gray):
        os.makedirs(dir_path_gray)
    # -------------------------------------------------------------

    # ディレクトリパスで示されたファイルを取得
    i = 0
    cap = cv2.VideoCapture(video_path)

    # 幅
    w: int = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 高さ
    h: int = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # 総フレーム画像数
    count: int = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)

    num = 0

    # フレームを保存→次のフレームへ


    while cap.isOpened():
        img_gray = dir_path_gray + file_name % str(i).zfill(4)
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:  # Is a frame left?
            count = i
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(img_gray, gray)  # Save a frame
        print('Save as : ', img_gray)

        i += 1

    # 終了したら、動画の情報（アス比、フレーム数、フレームレート）を出力
    print('width：%s | height：%s | フレーム数：%s | フレームレート：%s' % (w, h, count, fps))
    cap.release()  # When everything done, release the capture

    return h, w, num, dir_path_gray, name, fps   # グレースケール画像を保存したディレクトリを返して、検出のフローで使えるようにしたい


if __name__ == "__main__":
    # 動画ファイルの指定
    vid_file = input('ファイル名（拡張子も含む）:')
    print(vid_file)

    # 保存フォルダおよびファイル名の指定
    name_img = input('抽出画像の保存フォルダ（フォルダ名がファイル名になります）：')
    print(name_img)

    # 設定したように出力し、resultに動画の情報を格納
    result1 = video_2_grays(vid_file, name_img)

    deguchi(result1[0], result1[1], result1[2], result1[3], result1[4], result1[5])
