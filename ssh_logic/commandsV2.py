from naoqi import ALProxy
from time import sleep

IP = "127.0.0.1"
PORT = 9559
"""

from naoqi import ALProxy
IP = "127.0.0.1"
PORT = 9559
posture = ALProxy("ALRobotPosture", IP, PORT)
posture.goToPosture("StandInit", 0.5)

"""

motion = ALProxy("ALMotion", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)
life = ALProxy("ALAutonomousLife", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
leds = ALProxy("ALLeds", IP, PORT)

# =========================
# SAFE INIT
# =========================

life.setState("disabled")
motion.wakeUp()
posture.goToPosture("StandInit", 0.5)

# =========================
# TTS TEST
# =========================

tts.setLanguage("English")
tts.setVolume(0.8)
tts.setParameter("speed", 90)

tts.say("Speaking in Spanish")
sleep(2)

tts.say("Second sentence test")
sleep(2)

# =========================
# LED TEST
# =========================

tts.say("Changing LED lights")
sleep(1)

leds.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 1.0)
sleep(1)

leds.fadeRGB("FaceLeds", 0.0, 1.0, 0.0, 1.0)
sleep(1)

leds.fadeRGB("FaceLeds", 0.0, 0.0, 1.0, 1.0)
sleep(1)

# =========================
# POSTURE TEST
# =========================

posture.goToPosture("Sit", 0.5)
sleep(2)

posture.goToPosture("StandInit", 0.5)
sleep(2)

posture.goToPosture("Crouch", 0.5)
tts.setLanguage("English")