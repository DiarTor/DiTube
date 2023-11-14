import datetime
import os

from config.config import VIDEO_DOWNLOAD_DIR
from moviepy.editor import VideoFileClip, AudioFileClip
from bot.common.utils import replace_invalid_characters_with_underscore


def download_yt_video(yt, quality):
    datetimenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if not quality == "vc":
        if not quality == "1080p":
            video = yt.streams.filter(resolution=quality, progressive=True).first()
            video_title = replace_invalid_characters_with_underscore(yt.title)
            video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title} {datetimenow}.mp4")
            video_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{video_title} {datetimenow}.mp4")
            return video_path
        else:
            video = yt.streams.filter(resolution="1080p").first()
            audio_of_video = yt.streams.filter(only_audio=True).last()

            video_title = replace_invalid_characters_with_underscore(yt.title)
            video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title} {datetimenow}.mp4")
            video_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{video_title} {datetimenow}.mp4")

            audio_title = replace_invalid_characters_with_underscore(yt.title)
            audio_of_video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{audio_title} {datetimenow}.mp3")
            audio_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{audio_title} {datetimenow}.mp3")

            combined_output_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"combined_{video_title}.mp4")
            combine_audio_video(video_path, audio_path, combined_output_path)
            return combined_output_path

    else:
        audio = yt.streams.filter(only_audio=True).last()
        if audio is not None:
            audio_title = replace_invalid_characters_with_underscore(yt.title)
            audio.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{audio_title} {datetimenow}.mp3")
            audio_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{audio_title} {datetimenow}.mp3")
            return audio_path


def combine_audio_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264')
