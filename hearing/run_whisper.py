from faster_whisper import WhisperModel
from .hearing import Hearing


ears = Hearing()
print(ears.listen())


if __name__ == "__main__":
    use_microphone = input("Use microphone?")
    use_microphone = use_microphone.lower().strip()
    if use_microphone not in ['y', 'yes', "use", "use_microphone", "use microphone"]:
        exit(0)
        
    ears.access_microphone()
    

