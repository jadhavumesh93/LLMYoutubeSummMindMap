from fastapi import FastAPI
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .VideoProcess import VideoProcess

app = FastAPI()

@app.get("/")
def home():
    video_url = "https://www.youtube.com/watch?v=Q81RR3yKn30"
    video_process = VideoProcess()
    summary = video_process.summary(video_url)
    
    return summary
