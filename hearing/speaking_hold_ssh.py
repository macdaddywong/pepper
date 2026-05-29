# Pepper sound detection / auto-stop recording prototype
# Runs ON Pepper (Python 2.7)

from naoqi import ALProxy
import time

IP = "127.0.0.1"
PORT = 9559

audio = ALProxy("ALAudioDevice", IP, PORT)
try:
    audio.stopMicrophonesRecording()
except:
    pass

tts = ALProxy("ALTextToSpeech", IP, PORT)

OUTPUT = "/home/nao/input.wav"

# =========================
# SETTINGS
# =========================

THRESHOLD = 1400      # may need tuning
MAX_SILENCE = 2       # seconds before stopping
CHECK_DELAY = 0.1    # loop speed

# =========================
# START
# =========================

tts.say("listening")

audio.startMicrophonesRecording(OUTPUT)

speaking_started = False
silence_timer = 0.0

while True:

    # Pepper may support these methods
    # Try front mic first
    energy = audio.getFrontMicEnergy()

    print("Energy:", energy)

    # Human started speaking
    heard_talking = False
    if energy > THRESHOLD:
        if not heard_talking:
            # avoid repeatedly saying "I hear talking" if the person keeps talking
            heard_talking = True
            tts.say("I hear talking")
 
        print("Human is talking")
        speaking_started = True
        silence_timer = 0.0

    # Human stopped speaking
    elif speaking_started:
        
        silence_timer += CHECK_DELAY

    # enough silence -> stop
    if speaking_started and silence_timer >= MAX_SILENCE:
        print("HUMAN STOPPED SPEAKING")
        break

    time.sleep(CHECK_DELAY)

# =========================
# STOP RECORDING
# =========================

audio.stopMicrophonesRecording()

tts.say("Finished recording")

print("Recording saved:", OUTPUT)