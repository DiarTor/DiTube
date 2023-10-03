from pytube import YouTube
def get_video_options(yt):
    video_options = []
    for res in yt.streams.filter(progressive=True).order_by("resolution"):
        if res is not None:
            filesize_in_bytes = res.filesize
            filesize_in_kb = filesize_in_bytes / 1024
            formatted_filesize = "{:.1f}".format(filesize_in_kb / 1024)
            video_options.append(res.resolution + ' ' + formatted_filesize + 'mb')
    return set(video_options)
def get_only_filesize(url, res_code = None):
    yt = YouTube(url)
    if res_code:
        filesize = yt.streams.filter(resolution=res_code, progressive=True).first().filesize_mb
    else:
        filesize = yt.streams.filter(only_audio=True).last().filesize_mb
    return filesize