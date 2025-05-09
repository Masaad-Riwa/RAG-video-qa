from pytubefix import YouTube
import whisper
import os

def transcribe_video(url: str) -> str:
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    filename = "audio-file.mp4"
    audio.download(filename=filename)

    model = whisper.load_model("base")
    result = model.transcribe(filename, fp16=False)
    os.remove(filename)
    print("Transcription successfull")
    return result["text"]
