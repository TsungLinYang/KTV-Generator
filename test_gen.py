from faster_whisper import WhisperModel
from opencc import OpenCC
from tqdm import tqdm
import torch

# 設定模型與檔案路徑
device = torch.device('cpu')
if torch.cuda.is_available():
    print('cuda available!')
    device = torch.device('cuda')
else:
    print('cuda unvailable')

model = WhisperModel("small", device="cuda",device_index=0,compute_type="float16")  # 你可換成 tiny 或 medium

cc = OpenCC('s2t')

# 💾 寫死的檔案路徑
input_audio = "小星星 (Twinkle Twinkle Little Star) Chinese with Pinyin Subtitles Sing Along_Vocals.wav"
output_srt = "小星星 (Twinkle Twinkle Little Star) Chinese with Pinyin Subtitles Sing Along_Vocals.srt"

# 執行轉錄
print("🎙️ 開始轉錄音訊（含逐字時間）...")
segments, _ = model.transcribe(input_audio, word_timestamps=True)

# 格式化時間
def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

# 寫入 .srt
with open(output_srt, "w", encoding="utf-8") as f:
    for i, segment in enumerate(tqdm(segments, desc="📝 生成逐字 SRT")):
        words = segment.words
        if not words:
            continue
        start = format_timestamp(words[0].start)  # 🎯 以第一個字的時間為起點
        end = format_timestamp(words[-1].end)
        text = cc.convert("".join([w.word for w in words]).strip())
        f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")

print(f"✅ 精確逐字字幕儲存至：{output_srt}")

