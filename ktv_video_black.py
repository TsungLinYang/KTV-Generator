import subprocess
import os
import argparse
import wave

# 取得音訊長度
def get_audio_duration(audio_path):
    with wave.open(audio_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

# 處理參數
parser = argparse.ArgumentParser()
parser.add_argument("--input_audio", "-a", required=True)
parser.add_argument("--input_subtitle", "-s", required=True)
parser.add_argument("--output_video", "-o", required=True)
args = parser.parse_args()

bg_image = os.environ.get("KTV_BG_IMAGE", "black.jpg")
audio_path = args.input_audio
subtitle_path = args.input_subtitle
output_video = args.output_video

# 檢查背景圖
if not os.path.exists(bg_image):
    raise FileNotFoundError("❌ 找不到背景圖片：", bg_image)

duration = get_audio_duration(audio_path)
# print("testttttttt" + str(duration))

# 開始合成影片
print("🎬 開始合成 KTV 字幕影片（黑底模式）...")
subprocess.run([
    "ffmpeg",
    "-loop", "1",
    "-i", bg_image,
    "-i", audio_path,
    "-vf", f"subtitles={subtitle_path}",
    "-t", str(duration),           # ✅ 精準指定長度
    "-c:v", "libx264",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    output_video
])
print(f"🎉 完成！影片已儲存為：{output_video}")

