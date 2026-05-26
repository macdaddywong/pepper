from classroom_logic.classroom import Classrooms
from memory_logic.memory import Memory
from pepper.AI.chatbot import Chatbot
from pepper.pepper import Pepper


class1 = ["jhonny", "julius", "sophie", "rosa", "zoe", "jackie", "andrew"]

def setup()->"Pepper":
    try:
        print(f"1. building bot...")
        bot = Chatbot()

        print(f"2. building memory...")
        memory = Memory()

        print(f"3. building classroom...")
        classrooms = Classrooms(memories=memory, ai=bot)

        print(f"4. building Pepper...")
        pepper = Pepper(classrooms=classrooms, memories=memory, chatbot=bot)

        print(f"5. building database...")
        pepper.build_json()

        print(f"set up process successful")
        return pepper
    except Exception as ex:
        print(f"ERRORS detected: {ex}")
        input("press ENTER knowledgement on the issue...")


if __name__ == "__main__":
    pepper:Pepper = setup()
    if not pepper:
        exit(0)
    pepper.add_class(1, list_of_students=class1)

    pepper.active()


