import datetime
import os

from common.clean_title import replace_invalid_characters_with_space

from ..config import VIDEO_DOWNLOAD_DIR


def download_yt_video(yt, quality):
    datetimenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if not quality == "vc":
        video = yt.streams.filter(resolution=quality, progressive=True).first()
        if video is not None:
            video_title = replace_invalid_characters_with_space(yt.title)
            video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title} {datetimenow}.mp4")
            video_path = os.path.join(VIDEO_DOWNLOAD_DIR,
                                      f"{video_title} {datetimenow}.mp4")
            return video_path
        else:
            raise Exception("Selected quality not available for download")
    else:
        audio = yt.streams.filter(only_audio=True).last()
        if audio is not None:
            audio_title = replace_invalid_characters_with_space(yt.title)
            audio.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{audio_title} {datetimenow}.mp3")
            audio_path = os.path.join(VIDEO_DOWNLOAD_DIR,
                                      f"{audio_title} {datetimenow}.mp3")
            return audio_path
