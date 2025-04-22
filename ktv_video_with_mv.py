import subprocess
import os
import argparse

# 改為支援影片背景

parser = argparse.ArgumentParser()
parser.add_argument("--input_video", "-v", required=True)
parser.add_argument("--input_audio", "-a", required=True)
parser.add_argument("--input_subtitle", "-s", required=True)
parser.add_argument("--output_video", "-o", required=True)
args = parser.parse_args()

video_in_path = args.input_video
audio_path = args.input_audio
subtitle_path = args.input_subtitle
output_video = args.output_video

# bg_video = os.environ.get("KTV_BG_VIDEO", video_in_path)  # 預設背景影片名稱
bg_video = args.input_video

# 確認背景影片存在
if not os.path.exists(bg_video):
    raise FileNotFoundError("❌ 找不到背景影片，請先下載或指定 KTV_BG_VIDEO 環境變數。")

# 合成影片（使用背景影片）
print("🎬 開始合成 KTV 字幕影片（使用背景影片）...")
subprocess.run([
    "ffmpeg",
    "-i", bg_video,
    "-i", audio_path,
    "-vf", f"subtitles={subtitle_path}",
    "-shortest",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "-2",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    output_video
])
print(f"🎉 完成！影片已儲存為：{output_video}")

