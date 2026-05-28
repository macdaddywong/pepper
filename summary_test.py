# summary testing

from pepper.AI.chatbot import Chatbot
from keys import get_gemini_key

key = get_gemini_key(2)


bot = Chatbot(model="gemini", api_key=key)
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        response = bot.chat(user_input)
        print(f"Bot: {response['response']}\n")
        if not response:
            input("RESPONSE IS NONE, PLEASE DOUBLE CHECK")
            break
        summary = bot.summary_of_chat({"user": user_input, "response": response['response']})
        print(f"Summary of interaction: {summary['summary']}")