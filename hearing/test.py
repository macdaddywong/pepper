import subprocess
# qicli call ALTextToSpeech.say "I hear talking"
# qicli call ALTextToSpeech.say "listening"
PEPPER_IP = "172.17.10.113"

remote_cmd = r'''
qicli call ALAudioDevice.stopMicrophonesRecording 2>/dev/null


qicli call ALAudioDevice.startMicrophonesRecording /home/nao/input.wav

THRESHOLD=1000
MAX_SILENCE=2
COMMON_ENERGY_FOR_SILENCE=555826294
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
    f"nao@{PEPPER_IP}",
    remote_cmd
]

result = subprocess.run(cmd)