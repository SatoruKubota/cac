import cv2
import os

# 入力動画ファイルのパス
input_video_path = 'quvnu_ori.mp4'  # ここに入力動画ファイルのパスを指定
output_folder = 'quvnu_videos'  # 出力動画を保存するフォルダ

#CAC解析時のfps情報
cac_tracking_path = 'CAC_tracking.mp4'
cac_cap = cv2.VideoCapture(cac_tracking_path)
cac_fps = cac_cap.get(cv2.CAP_PROP_FPS)

# フォルダが存在しない場合は作成する
os.makedirs(output_folder, exist_ok=True)

# 動画ファイルを読み込む
cap = cv2.VideoCapture(input_video_path)

# 動画のフレームレートとフレーム総数を取得
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'ori_tatal_frame:{total_frames}')
cac_total_frames = int(cac_cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f'cac_tatal_frame:{cac_total_frames}')

#トラッキングビデオと入力動画のfpsを補正
fps_correct = fps/cac_fps
print(fps_correct)

# 切り取る基準のフレーム番号のリスト
#frame_list = [44790]  # 例: 基準となるフレーム番号のリスト
frame_list = [2130, 2580, 8430, 10740, 19470, 22530, 23610, 30150, 33120, 36360, 36870, 39720, 42270, 45570]
#correct_frame = [x * fps_correct for x in frame_list]
correct_frame_float = [x * fps_correct for x in frame_list]
correct_frame = [int(value) for value in correct_frame_float]

print(correct_frame)
# 60フレーム前から120フレーム後までの範囲を指定
offset_before = 60*int(round(fps_correct))
offset_after = 120*int(round(fps_correct))

# フレームリスト内の各フレーム番号に対して処理を行う
#for idx, frame_number in enumerate(frame_list):
for idx, frame_number in enumerate(correct_frame):
    start_frame = max(0, frame_number - offset_before)  # 30フレーム前（0未満にならないように）
    end_frame = min(total_frames - 1, frame_number + offset_after)  # 120フレーム後（総フレーム数を超えないように）

    # 出力動画のファイル名を設定
    #output_video_path = os.path.join(output_folder, f'output_{idx}.mp4')
    output_video_path = os.path.join(output_folder, f'nuvqu_{idx}.mp4')

    # 動画の書き出し用オブジェクトを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ))

    # 指定範囲のフレームを読み込んで保存する
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # 開始フレームにシーク

    for i in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)  # フレームを保存

    out.release()  # 出力動画を保存
    print(f'Video segment saved: {output_video_path}')
    

cap.release()
print('All segments have been processed and saved.')
