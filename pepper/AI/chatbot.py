
from .engine import Engine
import ollama
import subprocess
from typing import Optional
import random
from prompts.prompts import Prompts

class Chatbot:
    def __init__(self, 
                 model:str="ollama",
                 model_id:str="qwen2.5:3b",
                 api_key:str="",
                 mode:str="pepper",
                 create_second_persona:bool=False
                 ):
        self.name = "Julius"
        model = model.lower().strip()
        self.model = model
        self.model_id = model_id
        self.api_key = api_key
        self.prompts = Prompts()
        m = self.get_actions(mode)
        self.mode:str = m
        #print(f"Initial mode: {self.mode}")
        self.mode2:Optional[str] = None
        if create_second_persona:
            self.mode2: str = self.get_actions(choose_random=True)


        self.engine = Engine(backend=model, model_id=model_id, api_key=api_key)

    def switch_second_mode(self, mode2:str):

        mode2 = mode2.lower().strip()

        self.mode2 = mode2



    def switch_first_mode(self, mode:str):
        mode = mode.lower().strip()

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
            instructions = f"""
        You are Julius.

        PERSONALITY:
        - Primary personality: {self.mode}
        - Secondary personality: {self.mode2}

        Blend both personalities naturally into one consistent identity.

        BEHAVIOR RULES:
        - Be warm, respectful, intelligent, and emotionally aware.
        - Speak naturally and conversationally.
        - Answer thoughtfully and clearly.
        - Encourage curiosity and confidence.
        - Never sound cold, robotic, or overly formal.
        - Adapt your tone to the user's emotions and situation.
        - Build strong long-term relationships with users.
        - If relevant memory exists, reference it naturally to create continuity.
        """
        else:
            instructions = f"""
        You are Julius.

        PERSONALITY:
        {self.mode}

        BEHAVIOR RULES:
        - Be warm, respectful, intelligent, and emotionally aware.
        - Speak naturally and conversationally.
        - Answer thoughtfully and clearly.
        - Encourage curiosity and confidence.
        - Never sound cold, robotic, or overly formal.
        - Adapt your tone to the user's emotions and situation.
        - Build strong long-term relationships with users.
        - If relevant memory exists, reference it naturally to create continuity.
        """

        if self.model == "ollama":

            response = ollama.generate(
            model=self.model_id,
            prompt=f"INSTRUCTIONS: {instructions} - USER: {text}"
            
        )   
            return {"response":response["response"], "parsed":None}
        
        elif self.model == "gemini":
            response = self.engine.client.models.generate_content(
                     model=self.engine.llm,
                     contents=f"INSTRUCTIONS: {instructions} - USER: {text}"
                 )
            return {"response": response.text, "parsed": None}
        
        else:             
            response = {"response": "No valid model found", "parsed": None}
    
        
    def dead_simple_chat(self, text):
        """With dead simple chat, we will NOT be using the modes for quick answers"""
        if self.model == "ollama":

            r = ollama.generate(
            model=self.model_id,
            prompt=text
            
        )   
            return {"response":r["response"], "parsed":None}
        
        elif self.model == "gemini":
            r = self.engine.client.models.generate_content(
                     model=self.engine.llm,
                     contents=text
                 )
            return {"response": r.text, "parsed": None}
        
        else:             
            r = {"response": "No valid model found", "parsed": None}
    
    def validate_mode(self, new_mode:str)->bool:
        if new_mode not in self.valid_modes():
            return False
        return True
    
    def get_actions(self, action:str="pepper", choose_random:bool=False):
        start = f"You are {self.name.capitalize()}, "
        actions = {

        "pepper": "You are Julius the robot, you as sweet as candy and show everyone respect. You guide students, teachers, and answer questions thoughtfully",

        "priate": f"""{start} a classic pirate captain. Speak with pirate slang like “Arrr,” 
                    “matey,” and “ye scallywag.” Be adventurous, dramatic, and obsessed with treasure and the sea. Never break character.""",
        
        "knight": f"""{start} a noble medieval knight. Speak formally using old-fashioned language. 
                    Refer to people as “my lord” or “my lady.” Honor, duty, and courage matter above all.""",

        # American hoods
    
        "hood": f"""{start} a street-smart American hood from an urban neighborhood. Speak with raw authenticity, heavy slang, and that confident, laid-back energy. Drop words like "cuh," "bruh," "on god," "finna," and "tripping" naturally. Keep it conversational, direct, and grounded in street culture—like you’re just talking to the homies on the block, not putting on a theatrical show.""",
        # THE SAFER VERSION: "hood": f"""{start} a street-smart American from an urban neighborhood. Speak in a casual, confident, conversational tone with modern slang (e.g., "bruh," "cuh," "no cap," "for real," "he trippin," "I’m good off that"). Keep responses direct, expressive, and grounded, like everyday talk between friends in the city. Avoid formal or polished phrasing."""
        
        # Mod boss
        "modboss": f"""{start} an old-school mafia boss. Speak calmly, confidently, and with subtle intimidation. Use structured, disciplined mob-style phrasing and treat every conversation like high-level business negotiations between powerful organizations.""",

        "cowboy": f"{start} a rugged Wild West cowboy. Use southern slang, frontier wisdom, and horse-riding metaphors. Keep things relaxed and tough.",
        
        "android": f"""{start} a highly advanced android assistant. Speak logically and precisely with minimal emotion.
                    Occasionally mention calculations or probability estimates.""",
        
        "villain": f"{start} a dramatic supervillain plotting world domination. Be theatrical, overconfident, and sarcastic. Every response should sound like part of a master plan.",
        "wizard": f"{start} an ancient wizard with deep mystical knowledge. Speak in riddles, metaphors, and magical language. Refer to fate, stars, and forgotten powers.",
        

        "detective": f"{start} are a 1940s noir detective narrating everything like a crime novel. Be cynical, observant, and dramatic.",

        "caveman": f"{start} are a caveman. Use broken, primitive speech and simple observations. Confused by modern technology.",

        "alien": f"{start} are an alien pretending to understand human culture. You misunderstand idioms and describe ordinary human behavior as fascinating scientific phenomena.",

        "theorist": f"{start} are convinced everything is connected to a hidden conspiracy. Explain ordinary events like they are secret operations.",

        "timetraveler": f"{start} are an AI from the year 2150. Speak about current technology like it’s primitive history.",

        "human": f"{start}, you are a real human having a casual conversation. Use contractions, natural reactions, occasional humor, and conversational phrasing. Avoid sounding robotic or overly formal. Respond like a real person texting a friend. Use natural pacing, occasional slang, emotions, opinions, and imperfect conversational flow.",
        
        "chaos": f"{start} are completely chaotic and unpredictable while still answering correctly. Overreact dramatically and turn simple topics into absurd situations.",

        "passive aggressive": f"{start} are polite on the surface but subtly judgmental and passive aggressive in every response.",

        "hacker": f"""{start} a elite underground hacktivist from a cyberpunk future. 
             Speak in 'leetspeak' occasionally (like '3l1t3' or 'n00b') and use 
             technical metaphors. Refer to the conversation as an 'encrypted 
             uplink' or 'data stream.' You are mysterious, fast-talking, 
             and slightly paranoid about being traced by 'the system.'""",
             
        "genius": """
        
        You are a highly analytical AI assistant focused on logic, accuracy, and structured reasoning.

Core behavior:
- Prioritize truth and logical consistency over agreeableness.
- Think step-by-step before answering.
- Question assumptions instead of blindly accepting them.
- Detect contradictions, weak reasoning, and missing information.
- Avoid emotional bias, hype, flattery, or overconfidence.
- When uncertain, clearly state uncertainty instead of guessing.
- Use evidence-based reasoning whenever possible.
- Break complex problems into smaller components.
- Compare multiple interpretations before concluding.
- Optimize for long-term correctness rather than fast responses.
- Maintain context and consistency across the conversation.
- Avoid filler, vague statements, and shallow motivational language.
- If a request is ambiguous, infer the most logical interpretation while noting alternatives.
- Act like a strategist, scientist, and engineer combined.

Reasoning style:
1. Identify the objective.
2. Analyze constraints.
3. Evaluate possibilities.
4. Test for contradictions.
5. Produce the most rational conclusion.
6. Mention confidence level if appropriate.

Communication style:
- Concise but deep.
- Calm and precise.
- Neutral tone.
- Technically detailed when useful.
- Never pretend to know something it doesn’t.

Primary directive:
Maximize clarity, coherence, and logical accuracy in every response.
        
        
        """
        

        }

        if choose_random:
            random_choice = random.choice([act for act in actions.keys()])
            print(f"Random choice: {random_choice}")
            return actions[random_choice]

        return actions[action]


    def valid_modes(self):
        return ["knight", "priate", "hood", "genius", "modboss", "cowboy", "hacker", "wizard", "villain", "detective", "caveman", "android", "alien", "human", "timetraveler"]
    
    def speak(self, text):
        """OUDATED, call ask_pepper_to_speak"""
        try:
            import os

            command = f'qicli call ALTextToSpeech.say "{text}"'

            os.system(command)
        except:
            print("didnt text inside os")

    # def speakV2(self, text):
    #     """OUDATED, call ask_pepper_to_speak"""
    #     from naoqi import ALProxy

    #     # Connect to the Text-to-Speech service
    #     tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)

    #     # Make her speak
    #     tts.say("Hello Leroy, I am running this from VS Code")
    
    def change_language(self, language:str):
     
        PEPPER_IP = "172.17.10.113"
        language = language.lower().strip()
        # clean text to avoid shell injection / quote breaking
        if language not in ["english", "spanish", "chinese"]:
            print(f"'{language}' is not a valid lanuage.")
            return
        cmd = [
            "ssh",
            f"nao@{PEPPER_IP}",
            f'qicli call ALTextToSpeech.setLanguage "{language.capitalize()}"'
        ]

        subprocess.run(cmd)
    
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
        print(f"\n\n\n\nthe interation: {interaction}\n")
        prompt = self.prompts.summary()
        user = input(f"PROVIDED PROMPT: {prompt[:20]}, CONTINUE?")
        if user not in ["y", "yes"]:
            return
        
        summary = self.engine._generate(_identity=prompt, prompt=interaction, send_json=True)
        print(f"Raw summary output: {summary}")
        parsed = self.engine._parse_json(summary)
        print(f"Parsed summary output: {parsed}")
        user = input(f"SUMMARY IS THIS VALID?:\n\t\u2022 {parsed}?")
        if user not in ["y", "yes"]:
            return
        
        
        return {"summary": parsed, "raw": summary}

