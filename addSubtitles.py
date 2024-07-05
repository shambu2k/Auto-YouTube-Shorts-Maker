from moviepy.editor import *
import numpy as np
import os
from moviepy.config import change_settings

change_settings(
    {"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"}
)


def create_caption(
    word_info,
    framesize,
    font="Open Sans",
    color="white",
    highlight_color="yellow",
    stroke_color="black",
    stroke_width=1.5,
):
    full_duration = word_info["end"] - word_info["start"]

    word_clips = []
    xy_textclips_positions = []

    x_pos = 0
    y_pos = 0
    line_width = 0  # Total width of words in the current line
    frame_width = framesize[0]
    frame_height = framesize[1]

    fontsize = int(frame_height * 0.075)  # 7.5 percent of video height

    word_clip = (
        TextClip(
            word_info["word"],
            font=font,
            fontsize=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        .set_start(word_info["start"])
        .set_duration(full_duration)
    )
    word_width, word_height = word_clip.size

    xy_textclips_positions.append(
        {
            "x_pos": x_pos,
            "y_pos": y_pos,
            "width": word_width,
            "height": word_height,
            "word": word_info["word"],
            "start": word_info["start"],
            "end": word_info["end"],
            "duration": full_duration,
        }
    )
    word_clip = word_clip.set_position((x_pos, y_pos))
    word_clips.append(word_clip)

    return word_clips, xy_textclips_positions


# video_size,
from moviepy.editor import (
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    VideoFileClip,
    ColorClip,
)


def mute_and_attach_audio(video_path, audio_path):
    # Load video clip
    video_clip = VideoFileClip(video_path)

    # Mute the video clip
    muted_clip = video_clip.set_audio(
        AudioFileClip(audio_path).set_duration(video_clip.duration)
    )

    return muted_clip


def addSubtitlesAndAudio(
    video_path, audio_path, directory, output_file, word_level_subtitles
):
    input_video = mute_and_attach_audio(video_path, audio_path)
    audio = AudioFileClip(audio_path)
    if input_video.duration > audio.duration:
        input_video = input_video.subclip(0, audio.duration)
    frame_size = input_video.size
    all_word_level_splits = []
    # word_level_subtitles = [
    #     {"word": "Born", "start": 0.0, "end": 0.337},
    #     {"word": "and", "start": 0.372, "end": 0.441},
    #     {"word": "raised", "start": 0.499, "end": 0.766},
    #     {"word": "in", "start": 0.801, "end": 0.859},
    #     {"word": "the", "start": 0.894, "end": 0.964},
    #     {"word": "charming", "start": 0.998, "end": 1.335},
    #     {"word": "south,", "start": 1.405, "end": 1.927},
    #     {"word": "I", "start": 2.136, "end": 2.194},
    #     {"word": "can", "start": 2.264, "end": 2.38},
    #     {"word": "add", "start": 2.426, "end": 2.566},
    #     {"word": "a", "start": 2.601, "end": 2.624},
    #     {"word": "touch", "start": 2.67, "end": 2.879},
    #     {"word": "of", "start": 2.914, "end": 2.972},
    #     {"word": "sweet", "start": 3.042, "end": 3.332},
    #     {"word": "southern", "start": 3.39, "end": 3.692},
    #     {"word": "hospitality", "start": 3.738, "end": 4.447},
    #     {"word": "to", "start": 4.516, "end": 4.586},
    #     {"word": "your", "start": 4.656, "end": 4.76},
    #     {"word": "audiobooks", "start": 4.818, "end": 5.352},
    #     {"word": "and", "start": 5.387, "end": 5.457},
    #     {"word": "podcasts", "start": 5.503, "end": 6.548},
    # ]
    word_level_subtitles = word_level_subtitles
    for word_info in word_level_subtitles:
        out_clips, positions = create_caption(word_info, frame_size)
        clip_to_overlay = CompositeVideoClip(out_clips)
        clip_to_overlay = clip_to_overlay.set_position("center")
        all_word_level_splits.append(clip_to_overlay)

    input_video_duration = input_video.duration
    final_video = CompositeVideoClip([input_video] + all_word_level_splits)
    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(input_video.audio)
    # Save the final clip as a video file with the audio included
    output_path = os.path.join(directory, output_file)
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")


# test run

# word_level_subtitles = [
#     {"word": "Did", "start": 0.0, "end": 0.197},
#     {"word": "you", "start": 0.244, "end": 0.313},
#     {"word": "know", "start": 0.36, "end": 0.499},
#     {"word": "that", "start": 0.546, "end": 0.662},
#     {"word": "aliens", "start": 0.731, "end": 1.161},
#     {"word": "have", "start": 1.196, "end": 1.324},
#     {"word": "intergalactic", "start": 1.37, "end": 1.997},
#     {"word": "dance", "start": 2.055, "end": 2.31},
#     {"word": "parties,", "start": 2.345, "end": 2.705},
#     {"word": "but", "start": 2.74, "end": 2.879},
#     {"word": "they", "start": 2.914, "end": 3.053},
#     {"word": "always", "start": 3.111, "end": 3.448},
#     {"word": "insist", "start": 3.495, "end": 3.878},
#     {"word": "on", "start": 3.936, "end": 4.029},
#     {"word": "playing", "start": 4.087, "end": 4.354},
#     {"word": "the", "start": 4.4, "end": 4.47},
#     {"word": "Macarena", "start": 4.528, "end": 5.132},
#     {"word": "on", "start": 5.201, "end": 5.375},
#     {"word": "repeat?", "start": 5.457, "end": 6.06},
#     {"word": "🕺👽", "start": 6.211, "end": 6.211},
#     {"word": "Alien", "start": 6.211, "end": 6.583},
#     {"word": "spaceships", "start": 6.629, "end": 7.129},
#     {"word": "have", "start": 7.163, "end": 7.291},
#     {"word": "a", "start": 7.314, "end": 7.338},
#     {"word": "strict", "start": 7.407, "end": 7.755},
#     {"word": "no-bad-hair-day", "start": 7.848, "end": 8.742},
#     {"word": "policy,", "start": 8.8, "end": 9.404},
#     {"word": "enforced", "start": 9.439, "end": 9.915},
#     {"word": "by", "start": 9.938, "end": 10.031},
#     {"word": "their", "start": 10.077, "end": 10.228},
#     {"word": "advanced", "start": 10.275, "end": 10.728},
#     {"word": "hair-styling", "start": 10.786, "end": 11.389},
#     {"word": "technology.", "start": 11.436, "end": 12.26},
#     {"word": "💇\u200d♂️🚀", "start": 12.469, "end": 12.469},
#     {"word": "The", "start": 12.469, "end": 12.585},
#     {"word": "alien", "start": 12.666, "end": 12.991},
#     {"word": "fashion", "start": 13.049, "end": 13.374},
#     {"word": "trend", "start": 13.433, "end": 13.665},
#     {"word": "of", "start": 13.711, "end": 13.758},
#     {"word": "the", "start": 13.792, "end": 13.862},
#     {"word": "season", "start": 13.92, "end": 14.268},
#     {"word": "is", "start": 14.338, "end": 14.419},
#     {"word": "wearing", "start": 14.466, "end": 14.733},
#     {"word": "socks", "start": 14.814, "end": 15.174},
#     {"word": "with", "start": 15.209, "end": 15.348},
#     {"word": "sandals", "start": 15.395, "end": 15.824},
#     {"word": "while", "start": 15.871, "end": 16.045},
#     {"word": "cruising", "start": 16.08, "end": 16.393},
#     {"word": "through", "start": 16.428, "end": 16.614},
#     {"word": "the", "start": 16.637, "end": 16.707},
#     {"word": "galaxy", "start": 16.753, "end": 17.31},
#     {"word": "in", "start": 17.38, "end": 17.461},
#     {"word": "their", "start": 17.508, "end": 17.659},
#     {"word": "sleek,", "start": 17.717, "end": 18.158},
#     {"word": "spaceship-caricature", "start": 18.274, "end": 19.354},
#     {"word": "hybrids.", "start": 19.388, "end": 19.957},
#     {"word": "👽🧦🛸", "start": 20.004, "end": 20.004},
#     {"word": "Aliens", "start": 20.004, "end": 20.445},
#     {"word": "are", "start": 20.503, "end": 20.631},
#     {"word": "surprisingly", "start": 20.666, "end": 21.304},
#     {"word": "skilled", "start": 21.351, "end": 21.676},
#     {"word": "at", "start": 21.699, "end": 21.768},
#     {"word": "stand-up", "start": 21.815, "end": 22.198},
#     {"word": "comedy,", "start": 22.268, "end": 22.767},
#     {"word": "with", "start": 22.79, "end": 22.941},
#     {"word": "their", "start": 22.976, "end": 23.115},
#     {"word": "favorite", "start": 23.162, "end": 23.498},
#     {"word": "punchline", "start": 23.522, "end": 24.032},
#     {"word": "being,", "start": 24.079, "end": 24.474},
#     {"word": '"Why', "start": 24.508, "end": 24.741},
#     {"word": "did", "start": 24.799, "end": 24.915},
#     {"word": "the", "start": 24.95, "end": 25.019},
#     {"word": "moon", "start": 25.066, "end": 25.251},
#     {"word": "break", "start": 25.31, "end": 25.542},
#     {"word": "up", "start": 25.6, "end": 25.693},
#     {"word": "with", "start": 25.727, "end": 25.844},
#     {"word": "the", "start": 25.878, "end": 25.948},
#     {"word": "earth?", "start": 26.018, "end": 26.296},
#     {"word": "It", "start": 26.32, "end": 26.436},
#     {"word": "needed", "start": 26.482, "end": 26.738},
#     {"word": 'space!"', "start": 26.784, "end": 27.457},
#     {"word": "🌕🤣", "start": 27.782, "end": 27.782},
#     {"word": "Every", "start": 27.782, "end": 28.061},
#     {"word": "year,", "start": 28.119, "end": 28.456},
#     {"word": "aliens", "start": 28.514, "end": 28.99},
#     {"word": "host", "start": 29.048, "end": 29.292},
#     {"word": "the", "start": 29.327, "end": 29.408},
#     {"word": '"Extraterrestrial', "start": 29.466, "end": 30.453},
#     {"word": 'Bake-Off,"', "start": 30.522, "end": 31.765},
#     {"word": "where", "start": 34.563, "end": 34.748},
#     {"word": "they", "start": 34.783, "end": 34.888},
#     {"word": "compete", "start": 34.934, "end": 35.399},
#     {"word": "to", "start": 35.433, "end": 35.503},
#     {"word": "create", "start": 35.584, "end": 35.863},
#     {"word": "the", "start": 35.886, "end": 35.956},
#     {"word": "most", "start": 36.002, "end": 36.188},
#     {"word": "otherworldly", "start": 36.258, "end": 36.908},
#     {"word": "cakes", "start": 36.978, "end": 37.291},
#     {"word": "and", "start": 37.326, "end": 37.407},
#     {"word": "pastries.", "start": 37.465, "end": 38.231},
#     {"word": "🎂👾", "start": 38.231, "end": 38.313},
# ]

# addSubtitlesAndAudio(
#     os.path.join("temp_clips", "output.mp4"),
#     os.path.join("temp_clips", "output_audio.mp3"),
#     "temp_clips",
#     "final_video.mp4",
#     word_level_subtitles,
# )
