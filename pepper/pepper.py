
import sys
from typing import Any, TYPE_CHECKING, List
import subprocess
import time
from hearing.hearing import Hearing
from .tablet.tablet import Tablet
from states.Currentstate import States
if TYPE_CHECKING:
    from .AI.chatbot import Chatbot
    from memory_logic.memory import Memory
    from classroom_logic.classroom import Classrooms

class Pepper:
    def __init__(self, 
                 ip,
                 classrooms:"Classrooms", 
                 memories:"Memory", 
                 chatbot:"Chatbot",
                 only_ears:bool=False):
        
        self.ip = ip
        self.classrooms = classrooms
        self.memories = memories
        self._only_ears_ = only_ears
        self.chatbot = chatbot
        self.ears = Hearing()
        self.table_on:bool = False
        self.state = States.OFFLINE
        self.tablet = Tablet(bot=chatbot)


    # CHATBOT LOGIC
    def search(self, text):
        self.tablet.search(text)
        
    def speak(self, prompt:str):
        
        self.chatbot.ask_pepper_to_speak(prompt)
        
    def tablet_toggle(self):
        if not self.table_on:
            self.table_on = True
            subprocess.run(["ssh", f"nao@{self.ip}", "qicli call ALTabletService._openSettings"])
        else:
            self.table_on = False
            subprocess.run(["ssh", f"nao@{self.ip}", "qicli call ALTabletService._openSettings"])

    def wav_breakdown(self, path="wav/input.wav"):
        self.ears.wav_breakdown(path=path)
        
    def chat(self,prompt:str):
        self.chatbot.simple_chat(prompt)

    def see_modes(self):

        print(f" \nmode 1 '{self.chatbot.mode}', mode 2 '{self.chatbot.mode2}'\n")
        
    def change_first_mode_sequence(self):
         while True:
                print(f"current mode: {self.chatbot.mode}")
                new_mode = input(f"what personity would you like [{self.chatbot.valid_modes()}]: \n")
                if new_mode.lower().strip() in ["break", "back", "b", "q"]:
                    break
                if not self.chatbot.validate_mode(new_mode=new_mode):
                    print(f"\nmode '{new_mode}' is not valid, please choose what you see here: [{self.chatbot.valid_modes()}] \n")
                    continue
                action = self.chatbot.get_actions(action=new_mode)
                self.chatbot.switch_first_mode(mode=action)
                break
            
    def change_second_mode_sequence(self):
        while True:
                    print(f"current mode: {self.chatbot.mode2}")
                    new_mode = input(f"what personity would you like [{self.chatbot.valid_modes()}, none]: \n")
                    if new_mode.lower().strip() in ["break", "back", "b", "q"]:
                        break

                    if not self.chatbot.validate_mode(new_mode=new_mode):
                        print(f"\nmode '{new_mode}' is not valid, please choose what you see here: [{self.chatbot.valid_modes()}] ")
                        continue
                    if new_mode.lower().strip() in ["none", "0"]:
                        print("Node 2 being removed, to readd recall mode 2")
                        self.chatbot.switch_second_mode(mode2="")
                        return
                    
                    action = self.chatbot.get_actions(action=new_mode)
                    self.chatbot.switch_second_mode(mode2=action)
                    break 
    # MEMORY LOGIC
    def add_memory(self, ai_sum:dict):
        self.memories.AI_add_to_memory(ai_summary=ai_sum)

    def add_to_json(self, what:Any):
        pass

    def get_brain(self):
        return self.memories._get_brain()
    
    def commit(self):
        self.memories.commit()

    def build_json(self):
        self.memories._build_json()

    # CLASSROOM LOGIC
    def add_teacher(self, teacher:str):
        self.classrooms.add_teacher(teacher)

    def add_class(self, period:int, list_of_students:List[str]):
        cl = self.classrooms.add_class(period, list_of_students=list_of_students)
        self.memories.add_class(cl)

    def remove_classroom(self, period:int):
        self.classrooms.remove_class(period)

    def remove_student(self, student:str,):
        self.classrooms.remove_student(student)

    def add_student(self, period, student:str):
        self.classrooms.add_student(period=period, student=student)


    def change_language(self, language:str):
        self.chatbot.change_language(language)
        
    def vaild_whisper(self, text:str):
        text = text.lower().strip()
        invaild =  [
            ".",
            '%'
        ]
        
        if text == "" or not text:
            return False
        
        if "%" in text:
            return False
        
        if text == any(i for i in invaild):
            return False
        return True
        
    def _hear(self, speak:bool=True):
        try:
            while True:
                # print("=================================")
                # print("HEARING FOR USER INPUT TEST PHASE")
                # print("=================================\n")
                # keeping_going = input("keep going? (Y/N) ")
                # if keeping_going.lower().strip() not in ["y", 'yes', "keep going"]:
                #     break
                #time.sleep(1)
                user = self.ears.listen_then_respond() 
                if not user or user == "." or "%" in user:
                    print("Heard nothing, restarting loop")
                    continue
                # print(f"We were returned this as text:")
                # print("\n\t\u2022RAW:", user)
                # print("\n\t\u2022CLEAN:", self.ears.clean(user))
                # n = input("\nvalid? (Y/N/Q) ")
                # n = n.lower().strip()
                # if n in ['q', 'quit', 'break', 'b', '0', 'end', 'stop', 'finish', 'off']:
                #     exit(self.exit_text())
                # if n not in ['y', 'yes', 'yy','1']:
                #     continue
                
                #time.sleep(1)
                self.search(user)
                pepper = self.chatbot.dead_simple_chat(user)
                if not pepper:
                    print(f"Pepper return nothing for text, please double check on this issue: {pepper if pepper else 'Pepper said nothing'}")
                    break
                response = pepper["response"]
                #parse = pepper["parsed"]

                if speak:
                    self.chatbot.ask_pepper_to_speak(response)

                print(f"[pepper]: \n\t\u2022{response}\n\n")
                #print(f"[pepper (parsed)]: \n\t\u2022{parse}")
        except Exception as ex:
            print(f"There was an error during hearing process: {ex}\n")
            input("please hit ENTER for knowledgement on the issue")
            return
        
    def active(self, speak:bool=True, use_ears:bool=False, search:bool=False,response_strength:int=1, make_summary:bool=True):
        """The loop of pepper being active"""
        response_strength = 2 if response_strength > 2 else 1
       
        summary_broke:bool = False
        self.state = States.ONLINE
        strength = str(response_strength)
        if self._only_ears_ or use_ears:
            self._hear(speak=speak)
            self.exit_text()
            return
        
        try:
            while True:
                user = input("speak to pepper: ") 
                if user.lower() in ["q", "quit"]:
                    self.state = States.OFFLINE
                    self.exit_text()
                    break
                if user.lower() in ["see modes", "see mode"]:
                    self.see_modes()
                    continue
                
                if user.lower() in ["mode", "change mode"]:
                    self.change_first_mode_sequence()
                    continue
                
                if user.lower().strip() in ["tablet", "toggle", "toggle tablet"]:
                    self.tablet_toggle()
                    continue
                
                if user.lower().strip() in ["language", "change language"]:
                    continue
                
                if user.lower() in ["search", 'google', 'google search']:
                    while True:
                        searching = input("search (q to quit): ")
                        if searching.lower() in ["q", "quit",]:
                            break
                        self.tablet.google_search(searching)
                        
                        continue
                    continue
                        
                if user.lower() in ["mode2", "mode 2", "change mode2", "change mode 2"]:
                    self.change_second_mode_sequence()
                    continue
                if not user:
                    continue
                print("GETTING CHAT...")
                chats = {
                    "1": self.chatbot.dead_simple_chat,
                    "2": self.chatbot.simple_chat,
                   # "3": self.chatbot.chat
                }
           
                pepper = chats[strength](user)
                if not pepper:
                    print("Pepper didnt send any response, please double check")
                    exit(self.exit_text())
                    
                response = pepper["response"]
                parse = pepper["parsed"]

                if speak:
                    
                    self.chatbot.ask_pepper_to_speak(response)
                print("SEARCHING INSIDE def active()")
                if search:
                    self.search(user)


                print(f"[pepper]: \n\t\u2022{response}\n\n")
                #print(f"[pepper (parsed)]: \n\t\u2022{parse}")

                if make_summary:
                    if not summary_broke:
                        print("creating summary...")
                        summary = self.chatbot.summary_of_chat({"user":user, "response": response})
                    else:
                        continue
                    if not summary:
                        summary_broke = True
                        print("Summary process broke somewhere, continuing loop")
                        continue
                    print(f"summary: {summary['summary']}\n")
                    print("adding summary to memory")
                    self.memories.add_to_chat_history(summary['summary'])
                    print("memory process done, saving changes")
                    self.commit()
                continue

        except Exception as ex:
            print(f"ERROR: \n\t\u2022{ex}")
            user = input("Keep going? (Y/N)")

            if user.lower().strip() != 'y':
                self.state = States.OFFLINE
                return
            self.active()
            


    def exit_text(self):
        print("\nchatbot software deactivated")
        time.sleep(1)
        print("thanks for chatting!")
        sys.exit(0) 

    def _user_text_sequence(self, user:str):
        if user.lower() in ["q", "quit"]:
            self.state = States.OFFLINE
            self.exit_text()
            exit(0)
            
        if user.lower() in ["see modes", "see mode"]:
            self.see_modes()
            return True
        
        if user.lower() in ["mode", "change mode"]:
            self.change_first_mode_sequence()
            return True

        if user.lower() in ["mode2", "mode 2", "change mode2", "change mode 2"]:
            self.change_second_mode_sequence()
            return True
                    
        if not user:
            return False