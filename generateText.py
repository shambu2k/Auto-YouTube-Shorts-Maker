# this code adds facts audio with subtitles generated using AI and the machine voice
# this code generates fact, title and description using AI
# Import everything
from dotenv import load_dotenv
import random
import os
from openai import AsyncOpenAI
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from textwrap import dedent
import re
import config
from moviepy.video.tools.subtitles import SubtitlesClip
import speech_recognition as sr
import asyncio
from pydub import AudioSegment
import time
import wave
import contextlib
from moviepy.config import change_settings

change_settings(
    {"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"}
)
load_dotenv()


def get_video_length(file_path):
    with VideoFileClip(file_path) as video:
        duration = video.duration  # Duration in seconds
    return duration


async def generateWithAI(directory, clip_name, video_metadata):

    video_path = os.path.join(directory, clip_name)
    duration = get_video_length(video_path)
    title = video_metadata["title"]
    prompt = f"""As a funny fact generator, your role is to entertain and surprise with quirky and amusing facts. 
    You have been designed to create humor-infused content that captivates and delights the audience. 
    Your task is to generate fun facts based on a given title and duration in seconds. 
    I will provide you with blanks to fill in the specifics.
    Title: {title}
    Duration: {duration}
    Your goal is to provide me with humorous and captivating facts based on the provided title and duration.
    Ensure that the facts are light-hearted, creative, and amusing to keep the audience 
    entertained. Let your wit and creativity shine through as you craft the facts for 
    maximum enjoyment."""
    # Strip indentation using textwrap.dedent
    dedented_prompt = dedent(prompt)
    # Generate content using OpenAI API
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API"])
    ### MAKE .env FILE AND SAVE YOUR API KEY ###
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    time.sleep(5)

    content = completion.choices[0].message.content
    return content
    #     yes_no = input("\nIs this fine? (yes/no) >  ")
    #     if yes_no == "yes":
    #         content = completion.choices[0].message.content
    #     else:
    #         content = input("\nEnter >  ")
    # else:
    #     content = input("\nEnter the content of the video >  ")

    # # Generate speech for the video
    # speech = gTTS(text=content, lang="en", tld="ca", slow=False)
    # speech.save("temp_clips/speech.mp3")

    # audio_clip = AudioFileClip("temp_clips/speech.mp3")

    # if audio_clip.duration > duration:
    #     print(
    #         "\nSpeech too long!\n"
    #         + str(audio_clip.duration)
    #         + " seconds\n"
    #         + " but it can take up to "
    #         + str(duration)
    #         + " seconds\n"
    #     )
    #     exit()

    # print("\n")

    ### VIDEO EDITING ###
    # audio_path = os.path.join(directory, "speech.mp3")
    # subtitles_path = os.path.join(directory, "subtitles.srt")
    # Transcribe audio
    # transcribed_text = transcribe_audio(audio_path)
    # Create subtitles
    # create_subtitles(transcribed_text, os.path.join(directory, "subtitles.srt"))
    # Mute video and attach audio
    # video_clip_with_added_voice = mute_and_attach_audio(video_path, audio_path)
    # Add subtitles
    # video_with_subtitles = add_subtitles(video_clip_with_added_voice, subtitles_path)

    # # Trim a random part of minecraft gameplay and slap audio on it
    # video_clip = VideoFileClip("gameplay/gameplay_" + gp + ".mp4").subclip(
    #     start_point, start_point + audio_clip.duration + 1.3
    # )
    # final_clip = video_clip.set_audio(audio_clip)

    # # Resize the video to 9:16 ratio
    # w, h = final_clip.size
    # target_ratio = 1080 / 1920
    # current_ratio = w / h

    # if current_ratio > target_ratio:
    #     # The video is wider than the desired aspect ratio, crop the width
    #     new_width = int(h * target_ratio)
    #     x_center = w / 2
    #     y_center = h / 2
    #     final_clip = crop_vid.crop(
    #         final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center
    #     )
    # else:
    #     # The video is taller than the desired aspect ratio, crop the height
    #     new_height = int(w / target_ratio)
    #     x_center = w / 2
    #     y_center = h / 2
    #     final_clip = crop_vid.crop(
    #         final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center
    #     )

    # Write the final video
    # video_with_subtitles.write_videofile(
    #     os.path.join(directory, output_name), codec="libx264", audio_codec="aac"
    # )


# final_clip.write_videofile(
#     "generated/" + title + ".mp4",
#     codec="libx264",
#     audio_codec="aac",
#     temp_audiofile="temp-audio.m4a",
#     remove_temp=True,
# )


# {'title': 'Exploring the Wacky World of Bananas', 'description': '\nWelcome to the wacky world of bananas, where this fruit takes on a whole new level of silliness and surprises. Join us on a journey filled with fun facts that will make you go bananas with laughter!\n', 'facts': '\n1. Did you know that bananas are technically berries? That\'s right, these yellow wonders fall into the botanical category of berries, making them quite the fruity imposters!\n \n2. In Japan, there is a special technique called "banana art" where the skin of the banana is used as a canvas for intricate designs. Who knew bananas could double as both a snack and an art medium?\n'}

# for demo output
print(
    asyncio.run(
        generateWithAI(
            "temp_clips",
            "output.mp4",
            {
                "url": "https://v.redd.it/8flh2t3ffd9d1",
                "title": "Brutal 👽🛸 (via caricatureparty)",
                "author": "flyingfux",
            },
        )
    )
)
