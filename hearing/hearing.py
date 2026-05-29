
from faster_whisper import WhisperModel
import subprocess
import re
import os


class Hearing:
    def __init__(self, model:str="base", ip:str="172.17.10.113", wav_path:str="~/Psyche/peppers_system/hearing/wav/input.wav"):
        self.model = WhisperModel(model)
        self.wav_path = self._transform_path(wav_path)
        self.ip = ip
        
    def listen_then_respond(self):
        try:
            self.listen_for_speech()
            text = self.wav_breakdown(path=self.wav_path)
            return text
        except Exception as ex:
            print(f"Error during listening loop: {ex}")
            return ""
        
    def wav_breakdown(self, path="hearing/wav/input.wav"):
        try:
            segments, info = self.model.transcribe(path)

            text = " ".join([s.text for s in segments]).strip()

            print(f"I heard the speaker say: '{text}'\n")
            return text

        except Exception as e:
            print("Whisper error:", e)
            return ""
    
    def listen_for_speech(self):
        remote_cmd = r'''
qicli call ALAudioDevice.stopMicrophonesRecording 2>/dev/null


qicli call ALAudioDevice.startMicrophonesRecording /home/nao/input.wav

THRESHOLD=1000
MAX_SILENCE=2
COMMON_ENERGY_FOR_SILENCE=500000000
CHECK_DELAY=0.1

speaking_started=0
heard_talking=0
silence_time=0

while true
do
    energy=$(qicli call ALAudioDevice.getFrontMicEnergy | tr -dc '0-9')

    echo "Energy: $energy"
    
    
    

    if [ "$energy" -gt "$THRESHOLD" ]; then

        if [ "$heard_talking" -eq 0 ]; then
            
            heard_talking=1
        fi

        echo "Human is talking"

        speaking_started=1
        silence_time=0

    elif [ "$speaking_started" -eq 1 ]; then

        silence_time=$(awk "BEGIN {print $silence_time + $CHECK_DELAY}")

    fi

    stop=$(awk "BEGIN {print ($silence_time >= $MAX_SILENCE)}")

    if [ "$energy" -lt "$COMMON_ENERGY_FOR_SILENCE" ]; then
    
        echo "HUMAN STOPPED SPEAKING"
        
        sleep $CHECK_DELAY
        
        energy=$(qicli call ALAudioDevice.getFrontMicEnergy | tr -dc '0-9')
        
        if [ "$energy" -gt "$COMMON_ENERGY_FOR_SILENCE" ]; then
            echo "HUMAN started speaking again, repeating loop"
            continue
        fi
        
        break
    fi
    
    

    sleep $CHECK_DELAY
done

qicli call ALAudioDevice.stopMicrophonesRecording

echo "No more talking detected"

echo "Recording saved: /home/nao/input.wav"
'''

        # qicli call ALTextToSpeech.say "Finished recording"
        cmd = [
            "ssh",
            f"nao@{self.ip}",
            remote_cmd
        ]

        result = subprocess.run(cmd)
        if result.returncode != 0:
            print("SSH recording failed")
            return
        print("Recording finished. Pulling WAV...")
        self.pull_wav(self.ip)
        
        
    def turn_on_microphone(self):
        PEPPER_IP = self.ip

        print("Going into Pepper recording...")
        cmd = [
            "ssh",
            f"nao@{PEPPER_IP}",
            "qicli call ALAudioDevice.startMicrophonesRecording /home/nao/input.wav; sleep 2.5; qicli call ALAudioDevice.stopMicrophonesRecording"
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
        try:
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
            return True # success
        except Exception as ex:
            print(f"Error was detected while grabbing .wav file: {ex}")
            return False # failure
        
    def change_local_path(self, path:str):
        self.wav_path = self._transform_path(path)
        
    def _transform_path(self, path:str):
        return os.path.expanduser(path)
    


    def clean(self,text):
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text