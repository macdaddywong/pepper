from naoqi import ALProxy
import time

audio = ALProxy("ALAudioDevice", "127.0.0.1", 9559)

audio.startMicrophonesRecording("/home/nao/input.wav")

time.sleep(5)

audio.stopMicrophonesRecording()