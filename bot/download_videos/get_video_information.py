def get_video_options(yt):
    video_options = []
    for res in yt.streams.filter(progressive=True).order_by("resolution"):
        if res is not None:
            filesize = str(res.filesize // (1024 * 1024))
            video_options.append(res.resolution + ' ' + filesize + 'mb')
    return set(video_options)
