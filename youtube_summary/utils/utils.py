import os
from webbrowser import get
from youtube_transcript_api import YouTubeTranscriptApi as Transcript
import openai
from dotenv import load_dotenv

from youtube_summary.db.database import SessionLocal

load_dotenv()

MAX_TOKENS = 400
openai.api_key = os.getenv('GPT_3_API_KEY')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_transcript(video_link: str) -> str:
    video_id = video_link.split("=")[1]
    transcript = Transcript.get_transcript(video_id)
    # merging text from the dictionary
    text = ""
    for element in transcript:
        text += element["text"] + " "
    return text


def get_summary(text: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="summarize the transcript of the video in 200 words:" + text,
        temperature=0.8,
        max_tokens=MAX_TOKENS,
        top_p=1.0,
        frequency_penalty=0.1,
        presence_penalty=0.1
    )
    return response.choices[0].text
