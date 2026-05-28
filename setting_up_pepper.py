from classroom_logic.classroom import Classrooms
from memory_logic.memory import Memory
from pepper.AI.chatbot import Chatbot
from typing import TYPE_CHECKING
from keys import get_gemini_key
from pepper.pepper import Pepper


class1 = ["jhonny", "julius", "sophie", "rosa", "zoe", "jackie", "andrew"]

def setup(ai:str="ollama", set_up_json:bool=False)->"Pepper":
    gem_key = get_gemini_key()
    if ai == "gemini" and not gem_key:
        print("Gemini API key not found. Please set it in the .env file.")
        return None
    try:
        
        print(f"1. building bot...")
        bot = Chatbot(model=ai, api_key=gem_key, mode="genius")

        print(f"2. building memory...")
        memory = Memory()

        print(f"3. building classroom...")
        classrooms = Classrooms(memories=memory)

        print(f"4. building Pepper...")
        pepper = Pepper(classrooms=classrooms, memories=memory, chatbot=bot)

        # print(f"5. building database...")
        # pepper.build_json()
        print("Structure check")
        m = pepper.memories.memories
        print(m['brain']['name'])
        print(m['brain']['teachers'])
        print(f"set up process successful: {pepper.memories.memories['id']}")
        return pepper
    except Exception as ex:
        print(f"ERRORS detected: {ex}")
        input("press ENTER knowledgement on the issue...")


if __name__ == "__main__":
    pepper:"Pepper" = setup(ai="ollama")
    if not pepper:
        exit(0)
    #pepper.add_class(1, list_of_students=class1)

    pepper.active(use_ears=True)


