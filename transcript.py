
import sys
from faster_whisper import WhisperModel


def transcribe(path: str, model_size: str = "small"):
    # int8 keeps it fast and light on CPU
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(path, vad_filter=True)
    print(f"Detected language: {info.language} ({info.language_probability:.0%})\n")
    results = []
    for seg in segments:
        results.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})
        print(f"[{seg.start:6.1f}s -> {seg.end:6.1f}s] {seg.text.strip()}")
    return results


"""if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python transcribe.py path/to/clip.wav")
    transcribe(sys.argv[1])"""

test = transcribe('siralex.wav')

print (test) 