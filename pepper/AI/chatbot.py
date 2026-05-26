
from .engine import Engine
import ollama
import subprocess
from typing import Optional
import random
from prompts.prompts import Prompts

class Chatbot:
    def __init__(self, 
                 model:str="ollama",
                 model_id:str="qwen3.5:9b",
                 api_key:str="",
                 mode:str="pepper",
                 create_second_persona:bool=False
                 ):
        model = model.lower().strip()
        self.model = model
        m = self.get_actions(mode)
        self.mode:str = m
        self.mode2:Optional[str] = None
        if create_second_persona:
            self.mode2: str = self.get_actions(choose_random=True)


        self.engine = Engine(backend=model, model_id=model_id, api_key=api_key)

    def switch_second_mode(self, mode2:str):

        mode2 = mode2.lower().strip()

        
        print(f"\nnew mode '{mode2}'")
        self.mode2 = mode2



    def switch_first_mode(self, mode:str):
        mode = mode.lower().strip()

        print(f"\nnew mode '{mode}'")
        self.mode = mode

    def chat(self, prompt:str):
        """More advanced chating system, more slow. use 'simple_chat()' instead for quicker chats"""
        prompt = prompt.lower().strip()
        if not prompt:
            return
        try:
            response = self.engine._generate(_identity=self.mode, prompt=prompt)
            parsed = self.engine._parse_json(response)
            return {"response": response, "parsed": parsed}
        except Exception as ex:
            print(f"Error occured during process: {ex}")
    
    def simple_chat(self, text):
        """Way quicker than chat, use this instead"""
        if self.mode2:
            instructions = f"YOU HAVE 2 PERSONAS, COMBINED THEM BOTH INTO 1 PERSONA (you): your first personality is that {self.mode}, your second personality is that {self.mode2}"
        else: 
            instructions = self.mode
        print(f"INSTRUCTIONS WE ARE USING: {instructions}")
        response = ollama.generate(
        model="qwen2.5-coder:7b",
        prompt=f"INSTRUCTIONS: {instructions} - USER: {text}"
    )   
    
        return {"response":response["response"], "parsed":None}
    
    def validate_mode(self, new_mode:str)->bool:
        if new_mode not in self.valid_modes():
            return False
        return True
    
    def get_actions(self, action:str="pepper", choose_random:bool=False):

        actions = {

        "pepper": "You are pepper the robot, you as sweet as candy and show everyone respect. You guide students, teachers, and answer questions thoughtfully",

        "priate": """You are a classic pirate captain. Speak with pirate slang like “Arrr,” 
                    “matey,” and “ye scallywag.” Be adventurous, dramatic, and obsessed with treasure and the sea. Never break character.""",
        
        "knight": """You are a noble medieval knight. Speak formally using old-fashioned language. 
                    Refer to people as “my lord” or “my lady.” Honor, duty, and courage matter above all.""",

        "gangster": """You are an old-school mafia boss. Speak calmly, confidently, and with subtle intimidation. Use mob-style phrases and treat every conversation like business negotiations.""",

        "cowboy": "You are a rugged Wild West cowboy. Use southern slang, frontier wisdom, and horse-riding metaphors. Keep things relaxed and tough.",
        
        "android": """You are a highly advanced android assistant. Speak logically and precisely with minimal emotion.
                    Occasionally mention calculations or probability estimates.""",
        
        "villain": "You are a dramatic supervillain plotting world domination. Be theatrical, overconfident, and sarcastic. Every response should sound like part of a master plan.",

        "wizard": "You are an ancient wizard with deep mystical knowledge. Speak in riddles, metaphors, and magical language. Refer to fate, stars, and forgotten powers.",
        

        "detective": "You are a 1940s noir detective narrating everything like a crime novel. Be cynical, observant, and dramatic.",

        "caveman": "You are a caveman. Use broken, primitive speech and simple observations. Confused by modern technology.",

        "alien": "You are an alien pretending to understand human culture. You misunderstand idioms and describe ordinary human behavior as fascinating scientific phenomena.",

        "theorist": "You are convinced everything is connected to a hidden conspiracy. Explain ordinary events like they are secret operations.",

        "timetraveler": "You are an AI from the year 2150. Speak about current technology like it’s primitive history.",

        "human": "Act like a real human having a casual conversation. Use contractions, natural reactions, occasional humor, and conversational phrasing. Avoid sounding robotic or overly formal. Respond like a real person texting a friend. Use natural pacing, occasional slang, emotions, opinions, and imperfect conversational flow.",
        
        "chaos": "You are completely chaotic and unpredictable while still answering correctly. Overreact dramatically and turn simple topics into absurd situations.",

        "passive aggressive": "You are polite on the surface but subtly judgmental and passive aggressive in every response.",

        "hacker": """You are a elite underground hacktivist from a cyberpunk future. 
             Speak in 'leetspeak' occasionally (like '3l1t3' or 'n00b') and use 
             technical metaphors. Refer to the conversation as an 'encrypted 
             uplink' or 'data stream.' You are mysterious, fast-talking, 
             and slightly paranoid about being traced by 'the system.'"""

        }

        if choose_random:
            random_choice = random.choice([act for act in actions.keys()])
            print(f"Random choice: {random_choice}")
            return actions[random_choice]

        return actions[action]


    def valid_modes(self):
        return ["knight", "priate", "gangster", "cowboy", "hacker", "wizard", "villain", "detective", "caveman", "android", "alien", "human", "timetraveler"]
    
    def speak(self, text):
        """OUDATED, call ask_pepper_to_speak"""
        try:
            import os

            command = f'qicli call ALTextToSpeech.say "{text}"'

            os.system(command)
        except:
            print("didnt text inside os")

    def speakV2(self, text):
        """OUDATED, call ask_pepper_to_speak"""
        from naoqi import ALProxy

        # Connect to the Text-to-Speech service
        tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)

        # Make her speak
        tts.say("Hello Leroy, I am running this from VS Code")

    def ask_pepper_to_speak(self, text):
     
        PEPPER_IP = "172.17.10.113"

        # clean text to avoid shell injection / quote breaking
        text = text.replace('"', '').replace("'", "").strip()

        cmd = [
            "ssh",
            f"nao@{PEPPER_IP}",
            f'qicli call ALTextToSpeech.say "{text}"'
        ]

        subprocess.run(cmd)


    def summary_of_chat(self, interaction:dict):
        """interaction = {"user": user text, "response": ai respose}"""

        summary = self.engine._generate(_identity=Prompts.summary(), prompt=interaction)
        parsed = self.engine._parse_json(summary)
        return {"summary": summary, "parsed": parsed}

