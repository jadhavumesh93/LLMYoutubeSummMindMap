import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Services.YoutubeService import YoutubeService
from Services.LLMService import LLMService

class VideoProcess:
    def __init__(self):
        pass
    
    def summary(self, video_url : str = None):
        # 1. Youtube Service
        youtube_service = YoutubeService()
        (yt_status, yt_res) = youtube_service.process(video_url)
        if(yt_status == "error"):
            return (yt_status, yt_res)
        
        # 2. LLM Service
        llm_service = LLMService()
        (llm_status, llm_res) = llm_service.process(yt_res)
        return (llm_status, llm_res)
        