from pepper.AI.chatbot import Chatbot
import time
import sys
import signal

def handle(sig, frame):
    """
    Handles the interrupt signal. 
    'sig' is the signal number, 'frame' is the current stack frame.
    """
    exit_text()

signal.signal(signal.SIGINT, handle)


def chatting():

    bot = Chatbot()
    while True:
        
        user = input("speak to pepper: ") 
        if user.lower() in ["q", "quit"]:
            exit_text()
            break
        if user.lower() in ["see modes", "see mode"]:
            print(f" \nmode 1 '{bot.mode}', mode 2 '{bot.mode2}'\n")
            continue
        if user.lower() in ["mode", "change mode"]:
            while True:
                print(f"current mode: {bot.mode}")
                new_mode = input(f"what personity would you like [{bot.valid_modes()}]: \n")
                if new_mode.lower().strip() in ["break", "back", "b", "q"]:
                    break
                if not bot.validate_mode(new_mode=new_mode):
                    print(f"\nmode '{new_mode}' is not valid, please choose what you see here: [{bot.valid_modes()}] \n")
                    continue
                action = bot.get_actions(action=new_mode)
                bot.switch_mode(mode=action)
                break
            continue

        if user.lower() in ["mode2", "mode 2", "change mode2", "change mode 2"]:
            while True:
                print(f"current mode: {bot.mode2}")
                new_mode = input(f"what personity would you like [{bot.valid_modes()}, none]: \n")
                if new_mode.lower().strip() in ["break", "back", "b", "q"]:
                    break
                if not bot.validate_mode(new_mode=new_mode):
                    print(f"\nmode '{new_mode}' is not valid, please choose what you see here: [{bot.valid_modes()}] ")
                    continue
                if new_mode.lower().strip() in ["none", "0"]:
                    bot.switch_mode(mode=bot.mode, mode2=None)
                    return
                
                action = bot.get_actions(action=new_mode)
                bot.switch_mode(mode=bot.mode, mode2=action)
                break
            continue

        print("GETTING CHAT...")
        pepper = bot.simple_chat(user)
        response = pepper["response"]
        parse = pepper["parsed"]
        bot.ask_pepper_to_speak(response)
        print(f"[pepper]: \n\t\u2022{response}\n\n")
        print(f"[pepper (parsed)]: \n\t\u2022{parse}")

def exit_text():
    print("\nchatbot software deactivated")
    time.sleep(1)
    print("thanks for chatting!")
    sys.exit(0) 


if __name__ in "__main__":
    chatting()


# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass     