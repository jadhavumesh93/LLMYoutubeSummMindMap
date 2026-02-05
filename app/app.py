from fastapi import FastAPI
# app.py
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Services.YoutubeService import YoutubeService

app = FastAPI()

@app.get("/")
def home():
    youtube_service = YoutubeService()
    full_transcript = youtube_service.getYoutubeVideoUrl("https://www.youtube.com/watch?v=Q81RR3yKn30&t=743s")
    #return "Hello World"
    return full_transcript
