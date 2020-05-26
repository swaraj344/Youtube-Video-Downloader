from pytube import YouTube

class ytdata:
    url=None
    video_title = None
    thumbnail_url = None
    streamsList = None
    yt = None

    
    def load_data(self):
        self.yt=YouTube(self.url)
        self.video_title = self.yt.title
        self.thumbnail_url = self.yt.thumbnail_url
        self.streamsList = self.yt.streams.filter(progressive=True)     

    def __init__(self,url):
        self.url = url


