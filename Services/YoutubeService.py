from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

class YoutubeService:
    def __init__(self):
        self.token_size = 500
        self.token_threshold = 5000
    
    def getYoutubeVideoUrl(self, video_url : str = None):
        if(video_url == None):
            return None
        
        return self.extractVideoIdFromUrl(video_url)
        
    def extractVideoIdFromUrl(self, video_url : str = None):
        if(video_url == None):
            return None
        try:
            result = urlparse(video_url)
            if(all([result.scheme, result.netloc])):
                vid_que_str : dict = parse_qs(result.query)
                if(vid_que_str.keys().__contains__("v")):
                    #print(vid_que_str["v"])
                    return self.videoTranscriptGen(vid_que_str['v'][0])
                else:
                    print("No V present")
        except:
            pass
        
    def videoTranscriptGen(self, video_id = None):
        if(video_id == None):
            return None
        
        else:
            try:
                yt_tr_api = YouTubeTranscriptApi()
                video_transcript = yt_tr_api.fetch(video_id)
                #print(video_transcript)
                full_transcript = ""
                for snippets in video_transcript:
                    #print(snippets.text, end="\n")
                    full_transcript += snippets.text + " "
                
                #print(full_transcript)
                return full_transcript
            except Exception as ex:
                print(f"execption = {ex}")
                
    def generateChunks(self, full_transcript : str = None):
        if(full_transcript == None):
            return None
        
        