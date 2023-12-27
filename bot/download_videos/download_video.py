import os

import jdatetime
from bot.common.utils import replace_invalid_characters_with_underscore
from pytube import YouTube


def download_yt_video(link, quality):
    """
    This function download the YouTube Link with the specefic quality
    :param link: YouTube Video Link
    :param quality: Wanted Quality (1080p,etc... or vc for audio)
    :return: The Downloaded Video Path In Disk
    """
    yt = YouTube(link)
    datetimenow = jdatetime.datetime.now().strftime("%Y%m%d%H%M%S")
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

    if quality != "1080p":
        video = yt.streams.filter(resolution=quality, progressive=True).first()
        video_title = replace_invalid_characters_with_underscore(yt.title)
        video_path = download_stream(video, f"{video_title} {datetimenow}.mp4")
        return video_path

    # if quality == "1080p":
    #     video = yt.streams.filter(resolution="1080p").first()
    #     if video is not None:
    #         video_title = replace_invalid_characters_with_underscore(yt.title)
    #         video_path = download_stream(video, f"{video_title} {datetimenow}.mp4")
    #
    #         audio_of_video = yt.streams.filter(only_audio=True).last()
    #         if audio_of_video is not None:
    #             audio_title = replace_invalid_characters_with_underscore(yt.title)
    #             audio_path = download_stream(audio_of_video, f"{audio_title} {datetimenow}.mp3")
    #
    #             combined_output_path = os.path.join(download_video_dir, f"combined_{video_title}.mp4")
    #
    #             with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
    #                 temp_file_path = temp_file.name
    #
    #             combine_audio_video(video_path, audio_path, temp_file_path)
    #             shutil.copy(temp_file_path, combined_output_path)
    #             os.remove(temp_file_path)
    #             return combined_output_path
    # return None


def combine_audio_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264')
