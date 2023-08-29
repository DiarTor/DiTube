import os
from pathlib import Path
from ..config import VIDEO_DOWNLOAD_DIR


def download(yt, quality):
    video = yt.streams.filter(resolution=quality, progressive=True).first()
    if video is not None:
        video_title = yt.title
        if "|" in video_title:
            video_title = video_title.replace("|", " ")
        video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title}.mp4")
        video_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{video_title}.mp4")
        return video_path
    else:
        raise Exception("Selected quality not available for download")
