from classroom_logic.classroom import Classrooms
from memory_logic.memory import Memory
from pepper.AI.chatbot import Chatbot
from typing import TYPE_CHECKING
from keys import get_gemini_key
from pepper.pepper import Pepper


class1 = ["jhonny", "julius", "sophie", "rosa", "zoe", "jackie", "andrew"]

def setup(ip:str,ai:str="ollama", set_up_json:bool=False, model_id:str="qwen2.5:3b")->"Pepper":
    gem_key = get_gemini_key()
    if ai == "gemini" and not gem_key:
        print("Gemini API key not found. Please set it in the .env file.")
        exit(0)
    try:
        IP = ip
        print(f"1. building bot...")
        bot = Chatbot(model=ai, model_id=model_id, api_key=gem_key, mode="genius")

        print(f"2. building memory...")
        memory = Memory()

        print(f"3. building classroom...")
        classrooms = Classrooms(memories=memory)

        print(f"4. building Pepper...")
        pepper = Pepper(ip=IP, classrooms=classrooms, memories=memory, chatbot=bot)

        # print(f"5. building database...")
        # pepper.build_json()
        print("Structure check")
        m = pepper.memories.memories
        
        print(f"set up process successful: {m['id'] if m else 'memory check failed'}")
        return pepper
    except Exception as ex:
        print(f"ERRORS detected: {ex}")
        input("press ENTER knowledgement on the issue...")
        
def activate(self,force:str="on"):
    use_ears_or_not = input("Use ears? (Y/N): ").strip().lower() in ["y", "yes", "1", "true"]
    begin_searches = input("Use google searching? (Y/N): ").strip().lower() in ["y", "yes", "1", "true"]
    make_summary = input("Use google searching? (Y/N): ").strip().lower() in ["y", "yes", "1", "true"]

if __name__ == "__main__":
    use_ears_or_not = input("Use ears? (Y/N): ").strip().lower() in ["y", "yes", "1", "true"]
    begin_searches = input("Use google searching? (Y/N): ").strip().lower() in ["y", "yes", "1", "true"]
    
    pepper:"Pepper" = setup(ip="172.17.10.113", ai="ollama", model_id="qwen3:0.6b")
    if not pepper:
        print("Pepper failed to build, ending now...")
        exit(0)
    #pepper.add_class(1, list_of_students=class1)
    pepper.tablet_toggle()
    
    pepper.active(use_ears=use_ears_or_not, search=begin_searches, make_summary=False)


