#指定したフレームがどうなってるかを確かめるプログラム
import cv2
import pandas as pd

# CSVファイルを読み込み
#df = pd.read_csv('cac_test.csv')
#df = pd.read_csv('filtered_data.csv')
#df = pd.read_csv('0_4999_coord.csv')
df = pd.read_csv('quvnu_coord.csv')#テスト


def show_frame(video_path, frame_number):
    # 動画ファイルを読み込み
    cap = cv2.VideoCapture(video_path)
    
    # 動画が正しく読み込めたか確認
    if not cap.isOpened():
        print("Error: 動画ファイルを開けませんでした")
        return
    
    # 指定したフレームに移動
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # フレームを取得
    ret, frame = cap.read()
    
    # フレームが正しく取得できたか確認
    if not ret:
        print(f"Error: フレーム {frame_number} を取得できませんでした")
        return
    
    # フレームを表示
    
    # 指定されたフレームの x, y 座標をリスト形式で取得
    
    x_coords = df[df['frameIndex'] == frame_number]['x'].to_list()
    y_coords = df[df['frameIndex'] == frame_number]['y'].to_list()


    # x, y 座標をペアにしてリスト形式で取得
    coords = list(zip([int(x) for x in x_coords], [int(y) for y in y_coords]))
    for coord in coords:
        cv2.circle(frame, coord, 5, (0,255,0), 2)
    
    cv2.imshow(f'Frame {frame_number}', frame)
    
    # キーが押されるのを待つ
    cv2.waitKey(0)
    
    # ウィンドウを閉じる
    cv2.destroyAllWindows()
    
    # キャプチャを解放
    cap.release()

# 使用例
video_path = 'CAC_tracking.mp4'
frame_number = 45570# 表示したいフレーム番号を指定
show_frame(video_path, frame_number)

video_path_ori = 'quvnu_ori.mp4'
#frame_number_ori = frame_number*2
frame_number_ori = 91048

show_frame(video_path_ori, frame_number_ori)


