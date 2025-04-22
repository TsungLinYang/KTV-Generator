import yt_dlp
import os

class MusicDownloader:
    def __init__(self):
        pass

    def download_music(self, youtube_url):
        os.makedirs('Downloaded_Music', exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'Downloaded_Music/%(title)s.%(ext)s',
        }

        # 先記住現有檔案集合
        existing_files = set(os.listdir("Downloaded_Music"))

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # 下載完後找出新增的檔案
        new_files = set(os.listdir("Downloaded_Music")) - existing_files
        mp3_files = [f for f in new_files if f.endswith(".mp3")]

        if not mp3_files:
            raise FileNotFoundError("❌ 沒有找到剛下載的 mp3 檔案")

        return os.path.join("Downloaded_Music", mp3_files[0])
        
    def download_video_no_audio(self, youtube_url):
        os.makedirs('Downloaded_Video', exist_ok=True)

        ydl_opts = {
            'format': 'bestvideo[ext=mp4][vcodec!=none][acodec=none]',  # video only
            'outtmpl': 'Downloaded_Video/%(title)s.%(ext)s',
        }

        existing_files = set(os.listdir("Downloaded_Video"))

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        new_files = set(os.listdir("Downloaded_Video")) - existing_files
        video_files = [f for f in new_files if f.endswith(".mp4")]

        if not video_files:
            raise FileNotFoundError("❌ 沒有找到剛下載的 video-only mp4 檔案")

        return os.path.join("Downloaded_Video", video_files[0])


    def close_driver(self):
        pass
