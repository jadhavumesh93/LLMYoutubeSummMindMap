from youtube_transcript_api import YouTubeTranscriptApi
from YoutubeUtility.YoutubeUtility import YoutubeUtility
from urllib.parse import urlparse, parse_qs

class YoutubeService:
    def __init__(self):
        self.youtube_utility = YoutubeUtility()
        self.youtube_root = "https://www.youtube.com/watch"
    
    def extract_video_id(self, video_url):
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
        
    def get_video_transceipt(self, video_id : str = None):
        try:
            yrt = YouTubeTranscriptApi()
            transcript = yrt.fetch(video_id)
            transcript_list = transcript.to_raw_data()

            # ✅ FIX: Create proper Document objects with page_content and metadata
            documents = []
            full_text = ""

            for entry in transcript_list:
                text = entry['text']
                full_text += text + " "
            
            return ("success", full_text)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
    
    def check_valid_url(self, video_url : str = None):
        if(not video_url.startswith(self.youtube_root)):
            return ("error", self.youtube_utility.error_codes("ERR_2"))
        else:
            return ("success", True)
        
    def process(self, video_url : str = None):
        if(video_url == None or video_url == ""):
            return ("error", self.youtube_utility.error_codes("ERR_1"))
        
        (status, res) = self.check_valid_url(video_url)
        if(status == "error"):
            return (status, res)
        
        (status, res) = self.extract_video_id(video_url)
        if(status == "error"):
            return (status, res)
        
        (status, res) = self.get_video_transceipt(res)
        return (status, res)