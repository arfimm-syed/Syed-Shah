from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os

app = FastAPI(
    title="Azaan Microservice",
    description="HTTP microservice providing Azaan text and audio streaming",
    version="2.0.0"
)

AUDIO_FILE_PATH = "audio/azaan.mp3"


class AzaanResponse(BaseModel):
    language: str
    lines: list[str]


AZAAN_ARABIC = [
    "الله أكبر الله أكبر",
    "الله أكبر الله أكبر",
    "أشهد أن لا إله إلا الله",
    "أشهد أن لا إله إلا الله",
    "أشهد أن محمدًا رسول الله",
    "أشهد أن محمدًا رسول الله",
    "حي على الصلاة",
    "حي على الصلاة",
    "حي على الفلاح",
    "حي على الفلاح",
    "الله أكبر الله أكبر",
    "لا إله إلا الله"
]

AZAAN_TRANSLITERATION = [
    "Allahu Akbar, Allahu Akbar",
    "Allahu Akbar, Allahu Akbar",
    "Ashhadu an la ilaha illa Allah",
    "Ashhadu an la ilaha illa Allah",
    "Ashhadu anna Muhammadan Rasul Allah",
    "Ashhadu anna Muhammadan Rasul Allah",
    "Hayya 'ala-s-Salah",
    "Hayya 'ala-s-Salah",
    "Hayya 'ala-l-Falah",
    "Hayya 'ala-l-Falah",
    "Allahu Akbar, Allahu Akbar",
    "La ilaha illa Allah"
]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/azaan", response_model=AzaanResponse)
def get_azaan(language: str = "arabic"):
    if language.lower() == "transliteration":
        return AzaanResponse(
            language="transliteration",
            lines=AZAAN_TRANSLITERATION
        )

    return AzaanResponse(
        language="arabic",
        lines=AZAAN_ARABIC
    )


def audio_streamer(file_path: str, chunk_size: int = 1024 * 1024):
    with open(file_path, mode="rb") as audio_file:
        while True:
            chunk = audio_file.read(chunk_size)
            if not chunk:
                break
            yield chunk


@app.get("/azaan/audio")
def stream_azaan_audio():
    if not os.path.exists(AUDIO_FILE_PATH):
        raise HTTPException(status_code=404, detail="Azaan audio file not found")

    return StreamingResponse(
        audio_streamer(AUDIO_FILE_PATH),
        media_type="audio/mpeg"
    )
