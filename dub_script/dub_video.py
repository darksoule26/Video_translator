import os
import sys
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

# Check if the input arguments are provided
if len(sys.argv) < 3:
    print("Usage: python dub_video.py <input_video_path> <target_language>")
    sys.exit(1)

# Input video file and target language
input_video_path = sys.argv[1]  # Get the input video path from command line argument
target_language = sys.argv[2]  # Get the target language from command line argument

# Initialize speech recognition
recognizer = sr.Recognizer()

# Load the input video
video_clip = mp.VideoFileClip(input_video_path)

# Create a translator
translator = Translator()

# Process the audio of the video
audio_clip = video_clip.audio

# Save the audio as a temporary WAV file
temp_audio_path = 'media/temp_audio.wav'  # Store the temporary audio in the 'media' directory
audio_clip.write_audiofile(temp_audio_path, codec='pcm_s16le')

# Use speech recognition to transcribe the audio
with sr.AudioFile(temp_audio_path) as source:
    audio = recognizer.record(source)

# Translate the transcribed text to the target language
transcribed_text = recognizer.recognize_google(audio)
translated_text = translator.translate(transcribed_text, dest=target_language).text

# Generate the translated audio using gTTS
translated_audio_path = 'media/translated_audio.mp3'  # Store the translated audio in the 'media' directory
translated_audio = gTTS(translated_text, lang=target_language)
translated_audio.save(translated_audio_path)

# Replace the audio in the video with the translated audio
dubbed_video_clip = video_clip.set_audio(mp.AudioFileClip(translated_audio_path))

# Export the final dubbed video
output_video_path = 'media/dubbed_video.mp4'  # Store the dubbed video in the 'media' directory
dubbed_video_clip.write_videofile(output_video_path, codec='libx264')

# Clean up temporary audio files
os.remove(temp_audio_path)
os.remove(translated_audio_path)

print(f'Dubbing complete. The dubbed video is saved as {output_video_path}')
