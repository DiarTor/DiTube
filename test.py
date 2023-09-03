from pytube import YouTube

link = input("Enter the link: ")
yt = YouTube(link)
res = yt.streams.filter(progressive=True).order_by("resolution").last()
res.download(output_path="videos", filename="test.mp4")
