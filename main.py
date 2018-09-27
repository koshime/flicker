from M2FandG import video_2_frames_and_grays as gray
from F_D_deguchi import deguchi

if __name__ == "__main__":
    # 動画ファイルの指定
    vid_file = input('ファイル名（拡張子も含む）:')
    print(vid_file)

    # 保存フォルダの指定
    frame_dir = input('抽出画像の保存フォルダ：')
    print(frame_dir)

    # 抽出画像の名前の指定
    frame_file = input('抽出画像の名前:')
    print(frame_file)

    # 設定したように出力し、resultに動画の情報を格納
    result1 = gray(vid_file, frame_dir, frame_file)

    # 検出
    deguchi(result1[0], result1[1], result1[2], result1[3], result1[4], result1[5])