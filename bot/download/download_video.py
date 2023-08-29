import datetime
import os

from ..config import VIDEO_DOWNLOAD_DIR


def download(yt, quality):
    video = yt.streams.filter(resolution=quality, progressive=True).first()
    datetimenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if video is not None:
        video_title = yt.title
        if "|" in video_title:
            video_title = video_title.replace("|", " ")
        video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title} {datetimenow}.mp4")
        video_path = os.path.join(VIDEO_DOWNLOAD_DIR,
                                  f"{video_title} {datetimenow}.mp4")
        return video_path
    else:
        raise Exception("Selected quality not available for download")
