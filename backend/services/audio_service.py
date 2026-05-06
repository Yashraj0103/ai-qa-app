import os
import tempfile
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def transcribe_audio(file_bytes: bytes, filename: str) -> dict:
    try:
        from deepgram import DeepgramClient
        from deepgram.audio.speaker import options

        deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

        payload = {"buffer": file_bytes}

        options = {
            "model": "nova-2",
            "smart_format": True,
            "utterances": True,
            "punctuate": True,
        }

        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        result = response.to_dict()

        full_text = result["results"]["channels"][0]["alternatives"][0]["transcript"]

        segments = []
        utterances = result["results"].get("utterances", [])
        for utt in utterances:
            segments.append({
                "start": utt["start"],
                "end": utt["end"],
                "text": utt["transcript"]
            })

        return {"full_text": full_text, "segments": segments}

    except Exception as e:
        print(f"Transcription error: {e}")
        return {"full_text": "Transcription failed", "segments": []}