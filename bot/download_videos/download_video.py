import datetime
import os
import tempfile

from bot.common.utils import replace_invalid_characters_with_underscore
from moviepy.editor import VideoFileClip, AudioFileClip


def download_yt_video(yt, quality):
    datetimenow = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    download_video_dir = "/videos/"

    def download_stream(stream, filename):
        stream.download(output_path=download_video_dir, filename=filename)
        return os.path.join(download_video_dir, filename)

    if quality == "vc":
        audio = yt.streams.filter(only_audio=True).last()
        if audio is not None:
            audio_title = replace_invalid_characters_with_underscore(yt.title)
            audio_path = download_stream(audio, f"{audio_title} {datetimenow}.mp3")
            return audio_path

    if quality == "1080p":
        video = yt.streams.filter(resolution="1080p").first()
    else:
        video = yt.streams.filter(resolution=quality, progressive=True).first()

    video_title = replace_invalid_characters_with_underscore(yt.title)
    video_path = download_stream(video, f"{video_title} {datetimenow}.mp4")

    if quality == "1080p":
        audio_of_video = yt.streams.filter(only_audio=True).last()
        if audio_of_video is not None:
            audio_title = replace_invalid_characters_with_underscore(yt.title)
            audio_path = download_stream(audio_of_video, f"{audio_title} {datetimenow}.mp3")
            combined_output_path = os.path.join(download_video_dir, f"combined_{video_title}.mp4")

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file_path = temp_file.name

            combine_audio_video(video_path, audio_path, temp_file_path)
            os.replace(temp_file_path, combined_output_path)

            return combined_output_path

    return video_path


def combine_audio_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264')
