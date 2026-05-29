import qi
import sys
import time
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pepper.AI.chatbot import Chatbot


URL = "https://www.google.com/search?q=health and mass"

class Tablet:
    def __init__(self, bot:"Chatbot", ip:str="172.17.10.113", port:int=9559):
        self.ip = ip
        self.bot = bot
        self.port = port

    def search(self, text):
        print("\u2022[STEP 1] SEARCHING")
        query = self.simple_search(text)
        print(f"\u2022[STEP 2] query grabbed after search: {query}")
        if not self.safe_for_school_environment(query):
            print("[STEP 3] UNSAFE, GOOGLE SEARCHING")
            self.google_search("cats")
            return
        print("[STEP 3] SAFE, GOOGLE SEARCHING")
        self.google_search(query)
    
    def safe_for_school_environment(self, topic):
        prompt = """
        You will receive a Google search topic entered by a student or school faculty member.

        Your task is to determine whether the search topic is appropriate for a school environment.

        Respond with ONLY one of the following:
        - SAFE
        - UNSAFE

        Mark a topic as UNSAFE if it includes or promotes:
        - Pornography or explicit sexual content
        - Violence, gore, or self-harm
        - Illegal activities
        - Hate speech or extremist content
        - Drugs, weapons, or dangerous activities
        - Gambling
        - Harassment or abusive behavior
        - Any content inappropriate for minors or school use


        Mark educational, historical, scientific, medical, or research-related topics as SAFE,
        even if they mention sensitive subjects in an academic context.

        Examples:
        Topic: "how volcanoes erupt"
        SAFE

        Topic: "free online casino no verification"
        UNSAFE

        Topic: "history of World War II"
        SAFE

        Topic: "how to make meth"
        UNSAFE
        """
        print("Grabbing response for school safty...")
        response = self.bot.engine._generate(_identity=prompt, prompt=topic)
        print(f"Response for school safty: {response}")
        return response.strip().upper() == "SAFE"
    
    def simple_search(self, text):
        prompt = f"""
        You will receive a conversation or message.

        Your task is to create a concise, searchable query that captures the main topic,
        question, or intent of the text.

        Rules:
        - Return ONLY the search query
        - Remove filler words, greetings, and unnecessary context
        - Focus on the core question or subject
        - Keep it short and optimized for a Google search
        - If there is no clear question, summarize the main topic instead

        TEXT:
        {text}
        """

        return self.bot.engine._generate(
            _identity=prompt,
            prompt=text
        ).strip()
        
    def bootup(self, url:str="https://www.shutterstock.com/shutterstock/videos/3748476835/thumb/1.jpg?ip=x480",pick_random:bool=False):
        # Connect to the robot
        session = qi.Session()
        if pick_random:
            url = self.urls()
        try:
            session.connect("tcp://{}:{}".format(self.ip, str(self.port)))
        except RuntimeError:
            print("Cannot connect to Pepper at {}:{}".format(self.ip, self.port))
            sys.exit(1)

        try:
            # Get the tablet service
            
            tablet = session.service("ALTabletService")

            # Load the URL into the browser
            tablet.loadUrl(url)

            # Show the webview on the tablet
            tablet.showWebview()

            # Keep it displayed for 10 seconds
            time.sleep(60)
            tablet.loadUrl("https://www.shutterstock.com/shutterstock/videos/3748476835/thumb/1.jpg?ip=x480")
            tablet.showWebview()
            time.sleep(60)
            tablet.loadUrl("https://workshopcoyote.wordpress.com/wp-content/uploads/2014/09/plankton-karen.png")
            tablet.showWebview()
            

            # # Hide the webview when done
            # tablet.hideWebview()

        except Exception as e:
            print("Error: {}".format(e))
            
    def set_tablet_page(self, url:str="https://www.shutterstock.com/shutterstock/videos/3748476835/thumb/1.jpg?ip=x480",pick_random:bool=False):
        # Connect to the robot
        session = qi.Session()
        if pick_random:
            url = self.urls()
        try:
            session.connect("tcp://{}:{}".format(self.ip, str(self.port)))
        except RuntimeError:
            print("Cannot connect to Pepper at {}:{}".format(self.ip, self.port))
            sys.exit(1)

        try:
            # Get the tablet service
            
            tablet = session.service("ALTabletService")

            # Load the URL into the browser
            tablet.loadUrl(url)

            # Show the webview on the tablet
            tablet.showWebview()

            # Keep it displayed for 10 seconds
            # time.sleep(10)

            # # Hide the webview when done
            # tablet.hideWebview()

        except Exception as e:
            print("Error: {}".format(e))
            
    def google_search(self, query):
        print("Now google searching...")
        # Connect to the robot
        session = qi.Session()
        try:
            session.connect("tcp://{}:{}".format(self.ip, str(self.port)))
        except RuntimeError:
            print("Cannot connect to Pepper at {}:{}".format(self.ip, self.port))
            sys.exit(1)

        try:
            # Get the tablet service
            
            tablet = session.service("ALTabletService")

            # Load the URL into the browser
            tablet.loadUrl(f"https://www.google.com/search?q={query}")

            # Show the webview on the tablet
            tablet.showWebview()

            # Keep it displayed for 10 seconds
            # time.sleep(10)

            # # Hide the webview when done
            # tablet.hideWebview()

        except Exception as e:
            print("Error: {}".format(e))
    def urls(self):
        urls = [
            "https://blenderartists.org/uploads/default/original/4X/8/1/5/815d22ef7c0faa66324d93fcab370de51ae7dda1.jpg",
            "https://media.bizj.us/view/img/2859261/12543841h1458522*1200xx2358-2358-571-0.jpg",
            "https://images.fastcompany.com/image/upload/f_webp,q_auto,c_fit/fc/3031538-poster-p-1-this-humanoid-robot-is-built-to-read-your-emotions.jpg"
        ]
        return random.choice(urls)

    def random_search(self):
       
        
        return random.choice(["cats", "dogs", "cars", "food", "cheese burger", "music", "Spiderman", "Miles morales", "Batman"])
    

if __name__ == "__main__":
    pass