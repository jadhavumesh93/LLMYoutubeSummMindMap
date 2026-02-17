from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from YoutubeUtility.YoutubeUtility import YoutubeUtility
from urllib.parse import urlparse, parse_qs
#from pytube import YouTube
import requests

class YoutubeService:
    def __init__(self, video_url):
        self.youtube_utility = YoutubeUtility()
        self.youtube_root = "https://www.youtube.com/watch"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })
        self.video_url = video_url

    
    def extract_video_id(self):
        try:
            result = urlparse(self.video_url)
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
    
    def extract_video_title(self):
        try:
            endpoint = "https://www.youtube-nocookie.com/oembed"
            params = {
                "url": self.video_url,
                "format": "json"
            }

            response = requests.get(endpoint, params=params, timeout=10)
            data = response.json()
            print(f"Video Title = {data['title']}")
            return ("success", data["title"])
        
        except Exception as ex:
            #return ("error", ex)
            return ("error", "Youtube Title")
    
    # Commented because PyTube not giving Video Title
    '''
    def extract_video_title(self, video_url):
        try:
            result = urlparse(video_url)
            if(all([result.scheme, result.netloc])):
                yt = YouTube(video_url)
                print(f"yt = {yt.metadata} | {yt._title}")
                return ("success", yt.title)
            return ("error", "No video title")
        except Exception as ex:
            return ("error", ex)
    '''
    
    def get_video_transcript(self, video_id : str = None):
        try:
            print("transcript 1")
            #yrt = YouTubeTranscriptApi(proxy_config=WebshareProxyConfig(proxy_username="lyvwipom", proxy_password="02i9mix8en65", proxy_port=6754))
            yrt = YouTubeTranscriptApi()
            print("transcript 2")
            print(f"Video Id = {video_id}")
            transcript = yrt.fetch(video_id)
            print("transcript 3")
            transcript_list = transcript.to_raw_data()
            print("transcript 4")
            # Create proper Document objects with page_content and metadata
            documents = []
            full_text = ""

            for entry in transcript_list:
                text = entry['text']
                full_text += text + " "
            
            return ("success", full_text)
        except Exception as ex:
            print(f"{ex}")
            return ("error", ex)
    
    def check_valid_url(self):
        if(not self.video_url.startswith(self.youtube_root)):
            print(f"Valid URL = {self.video_url.startswith(self.youtube_root)}")
            return ("error", self.youtube_utility.error_codes("ERR_2"))
        else:
            return ("success", True)
        
    def process(self):
        print("Called process")
        if(self.video_url == None or self.video_url == ""):
            return ("error", self.youtube_utility.error_codes("ERR_1"))
        
        print("Called process 1")
        (status, res) = self.check_valid_url()
        if(status == "error"):
            return (status, res)
        
        print("Called process 2")
        (status, res) = self.extract_video_id()
        if(status == "error"):
            return (status, res)
        
        print("Called process 3")
        (status, res) = self.get_video_transcript(res)
        print("Called process 4")
        return (status, res)