from classroom_logic.classroom import Classrooms
from memory_logic.memory import Memory
from pepper.AI.chatbot import Chatbot
from pepper.pepper import Pepper


class1 = ["jhonny", "julius", "sophie", "rosa", "zoe", "jackie", "andrew"]


bot = Chatbot()
memory = Memory()
classrooms = Classrooms(memories=memory, ai=bot)



pepper = Pepper(classrooms=classrooms, memories=memory, chatbot=bot)


pepper.add_class(1, list_of_students=class1)



