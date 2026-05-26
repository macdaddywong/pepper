
import sys
from typing import Any, TYPE_CHECKING, List
import time
from states.Currentstate import States
if TYPE_CHECKING:
    from .AI.chatbot import Chatbot
    from memory_logic.memory import Memory
    from classroom_logic.classroom import Classrooms

class Pepper:
    def __init__(self, classrooms:"Classrooms", memories:"Memory", chatbot:"Chatbot"):
        self.classrooms = classrooms
        self.memories = memories
        self.chatbot = chatbot
        self.state = States.OFFLINE

    # CHATBOT LOGIC
    def speak(self, prompt:str):
        
        self.chatbot.ask_pepper_to_speak(prompt)

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
                        self.chatbot.switch_second_mode(mode2=None)
                        return
                    
                    action = self.chatbot.get_actions(action=new_mode)
                    self.chatbot.switch_second_mode(mode2=action)
                    break 
    # MEMORY LOGIC
    def add_memory(self, ai_sum:dict):
        self.memories.add_to_memory(ai_summary=ai_sum)

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
        self.classrooms.add_class(period, list_of_students=list_of_students)
        self.memories.add_class()

    def remove_classroom(self, period:int):
        self.classrooms.remove_class(period)

    def remove_student(self, student:str,):
        self.classrooms.remove_student(student)

    def add_student(self, student:str):
        self.classrooms.add_student(student=student)





    def active(self, speak:bool=True):
        """The loop of pepper being active"""
        self.state = States.ONLINE
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

                if user.lower() in ["mode2", "mode 2", "change mode2", "change mode 2"]:
                    self.change_second_mode_sequence()
                    continue

                print("GETTING CHAT...")
                pepper = self.chatbot.simple_chat(user)
                response = pepper["response"]
                parse = pepper["parsed"]

                if speak:
                    self.chatbot.ask_pepper_to_speak(response)

                print(f"[pepper]: \n\t\u2022{response}\n\n")
                print(f"[pepper (parsed)]: \n\t\u2022{parse}")
                summary = self.chatbot.summary_of_chat({"user":user, "response": response})
                self.memories['chat_history'].append(summary['summary'])

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
