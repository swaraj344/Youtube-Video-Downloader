from pytube import YouTube
# url='https://www.youtube.com/watch?v=Y9VgmhxtJFk'
# yt = YouTube(url)
# streams = yt.streams.filter(progressive=True)
# print(type(streams))
# for i in streams:

#     print(i)

# def get_length():
#     return len(streams)

class ytdata:
    url=None
    video_title = None
    thumbnail_url = None
    streamsList = None



    def load_data(self):
        yt=YouTube(self.url)
        self.video_title = yt.title
        self.thumbnail_url = yt.thumbnail_url
        self.streamsList = yt.streams.filter(progressive=True)


    
        

    def __init__(self,url):
        self.url = url

if __name__ == "__main__":
    obh=ytdata("www.google.com")
    print(obh.url)
