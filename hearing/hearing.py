
from faster_whisper import WhisperModel
import subprocess


class Hearing:
    def __init__(self, model:str="base", ip:str="172.17.10.113"):
        self.model = WhisperModel(model)
        self.ip = ip

    def listen(self, path="wav/input.wav"):
        try:
            segments, info = self.model.transcribe(path)

            text = " ".join([s.text for s in segments]).strip()

            print(f"I heard the speaker say: '{text}'\n")
            return text

        except Exception as e:
            print("Whisper error:", e)
            return ""
        
    def access_microphone(self):
     
        PEPPER_IP = self.ip
        
        # ssh to pepper
        subprocess.run([
        "ssh",
        f"nao@{PEPPER_IP}",
        "python /home/nao/ssh_.py"
    ])

        # back to laptop
        subprocess.run([
            "scp",
            f"nao@{PEPPER_IP}:/home/nao/input.wav",
            "~/Psyche/peppers_system/hearing/wav/input.wav"
        ])