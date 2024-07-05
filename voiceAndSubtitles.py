import requests
import json
import base64
from dotenv import load_dotenv
import os

load_dotenv()


def callElevenLabs(text, directory, output_audio_file):

    # VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
    VOICE_ID = "yl2ZDV1MzN4HbQJbMihG"  # Alex
    YOUR_XI_API_KEY = os.environ["ELEVEN_LABS_API"]

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"

    headers = {"Content-Type": "application/json", "xi-api-key": YOUR_XI_API_KEY}

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
    )

    if response.status_code != 200:
        print(
            f"Error encountered, status: {response.status_code}, "
            f"content: {response.text}"
        )
        quit()

    # convert the response which contains bytes into a JSON string from utf-8 encoding
    json_string = response.content.decode("utf-8")

    # parse the JSON string and load the data as a dictionary
    response_dict = json.loads(json_string)

    # the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string,
    # we need to decode it into bytes in order to save the audio as a file
    audio_bytes = base64.b64decode(response_dict["audio_base64"])
    output_audio_path = os.path.join(directory, output_audio_file)
    with open(output_audio_path, "wb") as f:
        f.write(audio_bytes)

    # the 'alignment' entry contains the mapping between input characters and their timestamps
    print(response_dict["alignment"])
    return convert_to_word_timestamps(response_dict["alignment"])


# callElevenLabs("do")


character_mapping = {
    "characters": [
        "B",
        "o",
        "r",
        "n",
        " ",
        "a",
        "n",
        "d",
        " ",
        "r",
        "a",
        "i",
        "s",
        "e",
        "d",
        " ",
        "i",
        "n",
        " ",
        "t",
        "h",
        "e",
        " ",
        "c",
        "h",
        "a",
        "r",
        "m",
        "i",
        "n",
        "g",
        " ",
        "s",
        "o",
        "u",
        "t",
        "h",
        ",",
        " ",
        "I",
        " ",
        "c",
        "a",
        "n",
        " ",
        "a",
        "d",
        "d",
        " ",
        "a",
        " ",
        "t",
        "o",
        "u",
        "c",
        "h",
        " ",
        "o",
        "f",
        " ",
        "s",
        "w",
        "e",
        "e",
        "t",
        " ",
        "s",
        "o",
        "u",
        "t",
        "h",
        "e",
        "r",
        "n",
        " ",
        "h",
        "o",
        "s",
        "p",
        "i",
        "t",
        "a",
        "l",
        "i",
        "t",
        "y",
        " ",
        "t",
        "o",
        " ",
        "y",
        "o",
        "u",
        "r",
        " ",
        "a",
        "u",
        "d",
        "i",
        "o",
        "b",
        "o",
        "o",
        "k",
        "s",
        " ",
        "a",
        "n",
        "d",
        " ",
        "p",
        "o",
        "d",
        "c",
        "a",
        "s",
        "t",
        "s",
    ],
    "character_start_times_seconds": [
        0.0,
        0.174,
        0.221,
        0.279,
        0.337,
        0.372,
        0.395,
        0.418,
        0.441,
        0.499,
        0.546,
        0.604,
        0.65,
        0.685,
        0.743,
        0.766,
        0.801,
        0.836,
        0.859,
        0.894,
        0.917,
        0.94,
        0.964,
        0.998,
        1.045,
        1.091,
        1.138,
        1.184,
        1.242,
        1.289,
        1.312,
        1.335,
        1.405,
        1.451,
        1.567,
        1.625,
        1.683,
        1.753,
        1.927,
        2.136,
        2.194,
        2.264,
        2.299,
        2.345,
        2.38,
        2.426,
        2.485,
        2.531,
        2.566,
        2.601,
        2.624,
        2.67,
        2.705,
        2.752,
        2.798,
        2.844,
        2.879,
        2.914,
        2.937,
        2.972,
        3.042,
        3.1,
        3.158,
        3.228,
        3.286,
        3.332,
        3.39,
        3.425,
        3.483,
        3.518,
        3.553,
        3.576,
        3.599,
        3.646,
        3.692,
        3.738,
        3.773,
        3.843,
        3.913,
        3.982,
        4.04,
        4.11,
        4.226,
        4.284,
        4.3,
        4.389,
        4.447,
        4.516,
        4.551,
        4.586,
        4.656,
        4.679,
        4.702,
        4.737,
        4.76,
        4.818,
        4.853,
        4.911,
        4.957,
        5.027,
        5.108,
        5.166,
        5.213,
        5.248,
        5.306,
        5.352,
        5.387,
        5.41,
        5.433,
        5.457,
        5.503,
        5.55,
        5.666,
        5.747,
        5.817,
        5.991,
        6.06,
        6.177,
    ],
    "character_end_times_seconds": [
        0.174,
        0.221,
        0.279,
        0.337,
        0.372,
        0.395,
        0.418,
        0.441,
        0.499,
        0.546,
        0.604,
        0.65,
        0.685,
        0.743,
        0.766,
        0.801,
        0.836,
        0.859,
        0.894,
        0.917,
        0.94,
        0.964,
        0.998,
        1.045,
        1.091,
        1.138,
        1.184,
        1.242,
        1.289,
        1.312,
        1.335,
        1.405,
        1.451,
        1.567,
        1.625,
        1.683,
        1.753,
        1.927,
        2.136,
        2.194,
        2.264,
        2.299,
        2.345,
        2.38,
        2.426,
        2.485,
        2.531,
        2.566,
        2.601,
        2.624,
        2.67,
        2.705,
        2.752,
        2.798,
        2.844,
        2.879,
        2.914,
        2.937,
        2.972,
        3.042,
        3.1,
        3.158,
        3.228,
        3.286,
        3.332,
        3.39,
        3.425,
        3.483,
        3.518,
        3.553,
        3.576,
        3.599,
        3.646,
        3.692,
        3.738,
        3.773,
        3.843,
        3.913,
        3.982,
        4.04,
        4.11,
        4.226,
        4.284,
        4.331,
        4.389,
        4.447,
        4.516,
        4.551,
        4.586,
        4.656,
        4.679,
        4.702,
        4.737,
        4.76,
        4.818,
        4.853,
        4.911,
        4.957,
        5.027,
        5.108,
        5.166,
        5.213,
        5.248,
        5.306,
        5.352,
        5.387,
        5.41,
        5.433,
        5.457,
        5.503,
        5.55,
        5.666,
        5.747,
        5.817,
        5.991,
        6.06,
        6.177,
        6.548,
    ],
}


def convert_to_word_timestamps(character_mapping):
    words = []
    current_word = ""
    word_start_time = None
    word_end_time = None

    for i, char in enumerate(character_mapping["characters"]):
        if char == " " and current_word:
            words.append(
                {"word": current_word, "start": word_start_time, "end": word_end_time}
            )
            current_word = ""
            word_start_time = None
            word_end_time = None
        else:
            current_word += char
            if word_start_time is None:
                word_start_time = character_mapping["character_start_times_seconds"][i]
            word_end_time = character_mapping["character_end_times_seconds"][i]

    # Add the last word if there is one
    if current_word:
        words.append(
            {"word": current_word, "start": word_start_time, "end": word_end_time}
        )
    return words


# word_timestamps = convert_to_word_timestamps(character_mapping)
# print(word_timestamps)
# for word, start, end in word_timestamps:
#     print(f"Word: {word}, Start: {start}, End: {end}")

# test run
print(
    callElevenLabs(
        """Did you know that aliens have intergalactic dance parties, but they always insist on playing the Macarena on repeat? 🕺👽 Alien spaceships have a strict no-bad-hair-day policy, enforced by their advanced hair-styling technology. 💇‍♂️🚀 The alien fashion trend of the season is wearing socks with sandals while cruising through the galaxy in their sleek, spaceship-caricature hybrids. 👽🧦🛸 Aliens are surprisingly skilled at stand-up comedy, with their favorite punchline being, "Why did the moon break up with the earth? It needed space!" 🌕🤣 Every year, aliens host the "Extraterrestrial Bake-Off," where they compete to create the most otherworldly cakes and pastries. 🎂👾""",
        "temp_clips",
        "output_audio.mp3",
    )
)
