from faster_whisper import WhisperModel

model = WhisperModel("base")

segments, info = model.transcribe("input.wav")

text = ""
for s in segments:
    text += s.text

print(text)