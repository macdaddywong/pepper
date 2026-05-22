import subprocess
import ollama
from pepper.AI.chatbot import Chatbot

PEPPER_IP = "172.17.10.113"

def ask_pepper_to_speak(text):
    # clean text to avoid shell injection / quote breaking
    text = text.replace('"', '').replace("'", "").strip()

    cmd = [
        "ssh",
        f"nao@{PEPPER_IP}",
        f'qicli call ALTextToSpeech.say "{text}"'
    ]

    subprocess.run(cmd)

# 1. Get response from Ollama
bot = Chatbot()
while True:
    user = input("TEXT (prototype): ")
    response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=f"Respond to the user directtly: {user}"
    )

    # 2. Send to Pepper
    ask_pepper_to_speak(response["response"])