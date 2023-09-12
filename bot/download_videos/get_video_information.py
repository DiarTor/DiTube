def get_video_options(yt):
    video_options = []
    for res in yt.streams.filter(progressive=True).order_by("resolution"):
        if res is not None:
            video_options.append(res.resolution)
    return set(video_options)