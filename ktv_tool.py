import subprocess
import os
import argparse
import sys
from yt_downloader import MusicDownloader

def run_pipeline(youtube_url, gpu_id, use_mv_background):
    print("🎵 偵測到 YouTube 連結，自動下載音樂中...")
    sys.stdout.flush()

    downloader = MusicDownloader()
    input_audio_path = downloader.download_music(youtube_url)
    input_video_path = downloader.download_video_no_audio(youtube_url) if use_mv_background else None
    downloader.close_driver()

    basename = os.path.splitext(os.path.basename(input_audio_path))[0]
    os.makedirs("output", exist_ok=True)

    # Step 1️⃣ 分離人聲與伴奏
    print("\n分離人聲與伴奏"); sys.stdout.flush()
    subprocess.run([
        "python", "-u", "inference.py",
        "--input", input_audio_path,
        "--gpu", str(gpu_id)
    ], check=True)

    # Step 2️⃣ 產生字幕檔
    print("\n生成字幕檔"); sys.stdout.flush()
    subprocess.run([
        "python", "-u", "generator_subtitle.py",
        "--input", f"output/{basename}_Vocals.wav",
        "--output", f"output/{basename}_subtitle.srt"
    ], check=True)

    # Step 3️⃣ 合成 KTV 影片（分兩種模式）
    print("\n合成 KTV 影片"); sys.stdout.flush()
    if use_mv_background:
        subprocess.run([
            "python", "-u", "ktv_video_with_mv.py",
            "--input_video", input_video_path,
            "--input_audio", f"output/{basename}_Instruments.wav",
            "--input_subtitle", f"output/{basename}_subtitle.srt",
            "--output_video", f"output/{basename}_video.mp4"
        ], check=True)
    else:
        subprocess.run([
            "python", "-u", "ktv_video_black.py",
            "--input_audio", f"output/{basename}_Instruments.wav",
            "--input_subtitle", f"output/{basename}_subtitle.srt",
            "--output_video", f"output/{basename}_video.mp4"
        ], check=True)

    print(f"\n✅ 全部完成！已產出影片：output/{basename}_video.mp4"); sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="YouTube 音樂網址")
    parser.add_argument("--gpu", type=int, default=-1, help="GPU 編號，-1 表示使用 CPU")
    parser.add_argument("--with_mv", action="store_true", help="使用原始 MV 當背景")
    args = parser.parse_args()

    run_pipeline(args.input, gpu_id=args.gpu, use_mv_background=args.with_mv)

