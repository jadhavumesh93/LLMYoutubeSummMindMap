from youtube_transcript_api import YouTubeTranscriptApi
from YoutubeUtility.Utility import YoutubeUtility
from urllib.parse import urlparse, parse_qs

class YoutubeService:
    def __init__(self):
        self.token_size = 500
        self.token_threshold = 5000
        self.youtube_root = "https://www.youtube.com/watch"
        self.youtube_utility = YoutubeUtility()
        
    def checkValidURL(self, video_url : str = None):
        if(not video_url.startswith(self.youtube_root)):
            return ("error", self.youtube_utility.error_codes("ERR_2"))
        else:
            return ("success", True)
    
    def extractVideoIdFromUrl(self, video_url : str = None):
        try:
            result = urlparse(video_url)
            if(all([result.scheme, result.netloc])):
                vid_que_str : dict = parse_qs(result.query)
                if(vid_que_str.keys().__contains__("v")):
                    #print(vid_que_str["v"])
                    return ("success", vid_que_str['v'][0])
                else:
                    print("No V present")
                    return ("error", self.youtube_utility.error_codes("ERR_3"))
        except Exception as ex:
            return ("error", ex)
        
    def videoTranscriptGen(self, video_id = None):
        try:
            yt_tr_api = YouTubeTranscriptApi()
            video_transcript = yt_tr_api.fetch(video_id)
            
            full_transcript = ""
            for snippets in video_transcript:
                #print(snippets.text, end="\n")
                full_transcript += snippets.text + " "
            
            return ("success", full_transcript)
        except Exception as ex:
            print(f"execption = {ex}")
            return ("error", "ERR_4")
                
    def generateChunks(self, full_transcript : str = None):
        if(full_transcript == None):
            return None
        
    
    def process(self, video_url : str = None):
        # 1. Check if URL is provided
        if(video_url == None):
            return ("error", self.youtube_utility.error_codes("ERR_1"))
        
        # 2. Check if URL is valid Youtube URL
        (status, res) = self.checkValidURL(video_url)
        if(status == "error"):
            return (status, res)
        
        # 3. Extract Video ID from URL
        (status, res) = self.extractVideoIdFromUrl(video_url)
        if(status == "error"):
            return (status, res)
        
        # 4. Generate Long text video transcript
        (status, res) = self.videoTranscriptGen(res)
        return (status, res)