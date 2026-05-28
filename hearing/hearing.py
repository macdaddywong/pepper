
from faster_whisper import WhisperModel
import subprocess
import re
import os


class Hearing:
    def __init__(self, model:str="base", ip:str="172.17.10.113", wav_path:str="~/Psyche/peppers_system/hearing/wav/input.wav"):
        self.model = WhisperModel(model)
        self.wav_path = self._transform_path(wav_path)
        self.ip = ip

    def listen(self, path="hearing/wav/input.wav"):
        try:
            segments, info = self.model.transcribe(path)

            text = " ".join([s.text for s in segments]).strip()

            print(f"I heard the speaker say: '{text}'\n")
            return text

        except Exception as e:
            print("Whisper error:", e)
            return ""
        
    def turn_on_microphone(self):
        PEPPER_IP = self.ip

        print("Going into Pepper recording...")
        cmd = [
            "ssh",
            f"nao@{PEPPER_IP}",
            "qicli call ALAudioDevice.startMicrophonesRecording /home/nao/input.wav; sleep 9; qicli call ALAudioDevice.stopMicrophonesRecording"
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("SSH recording failed")
            return
        print("Recording finished. Pulling WAV...")

        self.pull_wav(PEPPER_IP)

        
    def old_turn_on_microphone(self):

        PEPPER_IP = self.ip

        print("Going into Pepper recording...")

        # run recording on Pepper (BLOCKING)
        result = subprocess.run([
            "ssh",
            f"nao@{PEPPER_IP}",
            "python /home/nao/ssh_.py"
        ])

        if result.returncode != 0:
            print("SSH recording failed")
            return

        print("Recording finished. Pulling WAV...")

        self.pull_wav(PEPPER_IP)


    def pull_wav(self, ip: str):

        local = os.path.expanduser(
            "~/Psyche/peppers_system/hearing/wav/input.wav"
        )

        remote = f"nao@{ip}:/home/nao/input.wav"

        result = subprocess.run([
            "scp",
            remote,
            local
        ])

        if result.returncode != 0:
            print("SCP failed")
            return

        print("WAV successfully retrieved")
        
        
    def change_local_path(self, path:str):
        self.wav_path = self._transform_path(path)
        
    def _transform_path(self, path:str):
        return os.path.expanduser(path)
    


    def clean(self,text):
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text