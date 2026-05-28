from naoqi import ALProxy
from time import sleep
IP = "127.0.0.1"
PORT = 9559

# =========================
# CORE PROXIES
# =========================

motion = ALProxy("ALMotion", IP, PORT)
posture = ALProxy("ALRobotPosture", IP, PORT)
life = ALProxy("ALAutonomousLife", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
tracker = ALProxy("ALTracker", IP, PORT)
memory = ALProxy("ALMemory", IP, PORT)
audio = ALProxy("ALAudioDevice", IP, PORT)
people = ALProxy("ALPeoplePerception", IP, PORT)
face = ALProxy("ALFaceDetection", IP, PORT)
video = ALProxy("ALVideoDevice", IP, PORT)
leds = ALProxy("ALLeds", IP, PORT)
battery = ALProxy("ALBattery", IP, PORT)
tablet = ALProxy("ALTabletService", IP, PORT)

# =========================
# TEXT TO SPEECH
# =========================

tts.setLanguage("English")
tts.setVolume(0.8)
tts.setParameter("speed", 90)
tts.say("Speaking in english")
sleep(2)
tts.setVoice("naojpn")
sleep(2)
tts.say("Speaking with the naojpn voice")
sleep(2)
tts.setLanguage("Spanish")
tts.say("This is a speaking test")
sleep(2)
tts.say("Hablando en español")

tts.say("Changing Led lights")
sleep(2)
leds.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 1.0)
sleep(2)
leds.fadeRGB("FaceLeds", 0.0, 1.0, 0.0, 1.0)
sleep(2)
leds.fadeRGB("FaceLeds", 0.0, 0.0, 1.0, 1.0)
sleep(2)


# =========================
# BASIC BODY CONTROL
# =========================

# motion.wakeUp()
# motion.rest()
# motion.stopMove()

# =========================
# POSTURES
# =========================

posture.goToPosture("Stand", 0.5)
sleep(2)
posture.goToPosture("StandInit", 0.5)
sleep(2)
posture.goToPosture("Sit", 0.5)
sleep(2)
posture.goToPosture("Crouch", 0.5)

# =========================
# AUTONOMOUS LIFE
# =========================

# life.setState("disabled")
# life.setState("interactive")
# life.getState()

# =========================
# MOVEMENT
# =========================

# moveTo = pathfinding movement
# moveToward = live velocity movement

# motion.moveTo(0.2, 0.0, 0.0)

# FORWARD
# motion.moveToward(0.5, 0.0, 0.0)

# BACKWARD
# motion.moveToward(-0.5, 0.0, 0.0)

# LEFT / RIGHT STRAFE
# motion.moveToward(0.0, 0.3, 0.0)
# motion.moveToward(0.0, -0.3, 0.0)

# ROTATE
# motion.moveToward(0.0, 0.0, 0.4)
# motion.moveToward(0.0, 0.0, -0.4)

# STOP
# motion.stopMove()

# =========================
# HEAD CONTROL
# =========================

# motion.setAngles("HeadYaw", 0.5, 0.2)
# motion.setAngles("HeadPitch", -0.2, 0.2)

# =========================
# ARM CONTROL
# =========================

# motion.setAngles("LShoulderPitch", 1.0, 0.2)
# motion.setAngles("RShoulderPitch", 1.0, 0.2)

# =========================
# TRACKING / FOLLOWING
# =========================

# tracker.registerTarget("Face", 0.1)
# tracker.track("Face")
# tracker.stopTracker()
# tracker.unregisterAllTargets()

# =========================
# AUDIO / MICROPHONE
# =========================

# audio.setOutputVolume(80)
# audio.getOutputVolume()

# RECORD AUDIO
# audio.startMicrophonesRecording(
#     "/home/nao/test.wav",
#     "wav",
#     16000,
#     [1,1,1,1]
# )

# audio.stopMicrophonesRecording()

# =========================
# MEMORY / EVENTS
# =========================

# memory.getData("FrontTactilTouched")
# memory.getData("MiddleTactilTouched")
# memory.getData("RearTactilTouched")

# =========================
# LED CONTROL
# =========================

# leds.fadeRGB("FaceLeds", 1.0, 0.0, 0.0, 1.0)
# leds.fadeRGB("FaceLeds", 0.0, 1.0, 0.0, 1.0)
# leds.fadeRGB("FaceLeds", 0.0, 0.0, 1.0, 1.0)

# =========================
# BATTERY
# =========================

# print(battery.getBatteryCharge())

# =========================
# TABLET
# =========================

# tablet.showWebview("https://google.com")
# tablet.hideWebview()

# =========================
# CAMERA ACCESS
# =========================

# print(video.getSubscribers())

# =========================
# SYSTEM HELPERS
# =========================

# print(dir(motion))
# print(dir(tts))
# print(dir(audio))
# print(dir(tracker))

# =========================
# SIMPLE STARTUP EXAMPLE
# =========================

# life.setState("disabled")
# motion.wakeUp()
# posture.goToPosture("StandInit", 0.5)
# tts.say("Systems online")
# motion.moveToward(0.3, 0.0, 0.0)
