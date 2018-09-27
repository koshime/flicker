import os
import shutil
import cv2

# グレースケール画像で動画をフレームごとに抽出するためのモジュール


def video_2_frames_and_grays(video_file: str, dir_name: str, img_name: str):
    # -------------------------------------------------------------
    # 入力をもとにディレクトリのパスを生成
    # ビデオのアドレス
    video_path = './'+video_file
    # 画像を保存するフォルダのアドレス
    dir_path = './' + dir_name + '/'
    # 保存画像の名前
    file_name = img_name + '_%s.png'
    # イメージを保存するディレクトリがすでにあったらディレクトリツリーを削除
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    # 存在しないなら作成
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
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
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:  # Is a frame left?
            break
        img = dir_path+file_name % str(i).zfill(4)
        cv2.imwrite(img, frame)  # Save a frame
        print('Save', img)
        i += 1
        num = i  # 画像数を保存し、次のグレースケール化で使用

    # 終了したら、動画の情報（アス比、フレーム数、フレームレート）を出力
    print('width：%s | height：%s | フレーム数：%s | フレームレート：%s' % (w, h, count, fps))
    cap.release()  # When everything done, release the capture

# ----------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # 読み出した画像のグレースケール化
    a = input("グレースケールにします")
    # グレイスケールのディレクトリへのパスを生成する
    dir_path_gray = './' + dir_name + "_gray" + '/'
    # グレイスケール画像用のディレクトリを、元画像ディレクトリと同じ場所に作成する
    if os.path.exists(dir_path_gray):
        shutil.rmtree(dir_path_gray)
    # Make the directory if it doesn't exist.
    if not os.path.exists(dir_path_gray):
        os.makedirs(dir_path_gray)
    # ----------------------------------------------------------------------------
    # グレースケール化を行う
    i = 0
    while i < num:  # num：前の作業で保存したフレームの数
        # 入力画像の読み込み→グレイスケール画像を,元画像から取り込み生成
        # img_file = img_file + '_%s.png'

        grayimg = cv2.imread(dir_path + file_name % str(i).zfill(4), 0)

        cv2.imwrite(dir_path_gray + img_name + '_gray_%s.png' % str(i).zfill(4), grayimg)  # 結果を出力
        print('Save', dir_path_gray + img_name + '_gray_%s.png' % str(i).zfill(4))  # 保存状態を出力
        i += 1

    return h, w, num, dir_path_gray, img_name, dir_name, fps   # グレースケール画像を保存したディレクトリを返して、検出のフローで使えるようにしたい



