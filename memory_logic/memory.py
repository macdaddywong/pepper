
import json
from .stucture import Stucture
from datetime import datetime, timezone
class Memory:
    def __init__(self, Brain:None=None):
        """'Brain' is a future import of Julius's Psyche software"""
        self.memories = {}
        self.file_name = "Pepper.json"


    def add_to_memory(self, ai_summary:dict):
        """ai_summary = {
        
            "summary": "pepper summary",
            "mode": "mode it was in", 
            "student_connection": "true or false"
            
            }"""
        try:
            self.memories["memories"].append(
                {
                    "summary": ai_summary['summary'],
                    "mode": ai_summary["mode"],
                    "date": datetime.now(timezone.utc)
                }
            )
            self.commit()
            print("SAVED MEMORY")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 




    def _build_json(self):
        with open(self.file_name, "w") as f:
            self.memories = json.dump(Stucture.build(), f)


    def _get_brain(self):
        return self.memories[0]["brain"]
    
    def commit(self)->None:
        try:
            with open(self.file_name, "w") as f:
                json.dump(self.memories, f)
        except Exception as ex:
            while True:

                hold = input(f"ERROR: {ex}")