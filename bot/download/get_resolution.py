def get_resolution_options(yt):
    resolution_options = []
    for res in yt.streams.filter(progressive=True).order_by("resolution"):
        if res is not None:
            resolution_options.append(res.resolution)
    return set(resolution_options)