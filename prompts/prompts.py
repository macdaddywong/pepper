




class Prompts:
    def summary(self)->str:
        return """
        
        You are getting a chat between you and the user. Create a summary of this chat, grabbing key moments and the possible emotion
        that can be seen in the interaction. 
        
        Once you have a final prediction, return in json:

        {{
            "summary": The summary of the chat between you and the user,
            "emotion": The emotion that best fits this interaction,
            "rating": rating of this interaction, how much you felt it was appropriate to school enviroments and learning.
        }}
        
        
        
        """.strip()

    def causal(self, modes:tuple):
        causal_prompt = """
        
        
        
        
        
        
        
        
        """



    def teaching_(self):
        pass