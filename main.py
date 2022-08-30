import os
from webbrowser import get
from youtube_transcript_api import YouTubeTranscriptApi as Transcript
import openai

MAX_TOKENS = 400

video_link = "https://www.youtube.com/watch?v=rw_f8RRSVrU"


#openai.api_key = os.environ.get('GPT_3_API_KEY')
openai.api_key = input("Enter your GPT_3 API KEY")


def get_text(video_link):
    video_id = video_link.split("=")[1]
    transcript = Transcript.get_transcript(video_id)
    #merging text from the dictionary
    text = ""
    for element in transcript:
        text += element["text"] + " "
    return text

def get_summary(text):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="summarize the transcript of the video in 200 words:\n\n" + text,
    temperature=0.8,
    max_tokens=MAX_TOKENS,
    top_p=1.0,
    frequency_penalty=0.1,
    presence_penalty=0.1
)
    return response

video_link = input("paste a link of a youtube video: ")

text = get_text(video_link)
response = get_summary(text)



print("\n\n")
print(response.choices[0].text)
