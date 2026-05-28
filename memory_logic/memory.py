
import json
import os
from .Structure import Structure
from datetime import datetime, timezone


class Memory:
    def __init__(self, Brain:None=None):
        """'Brain' is a future import of Julius's Psyche software"""
        self.file_name = "Pepper.json"
        self.memories = None
        self._load_json()


    def AI_add_to_memory(self, ai_summary:dict):
        """ai_summary = {
        
            "summary": "pepper summary",
            "mode": "mode it was in", 
            "student_connection": "true or false"
            
            }"""
        try:
            self.memories['brain']["memories"].append(
                {
                    "summary": ai_summary['summary'],
                    "mode": ai_summary["mode"],
                    "date": datetime.now(timezone.utc).isoformat()
                }
            )
            self.commit()
            print("SAVED SUMMARY")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 


    def add_teacher(self, teacher:str):
        
        try:
            if teacher in self.memories['brain']['teachers']:
                print(f"teacher already inside database")
                return
            self.memories['brain']['teachers'].append(teacher)
            self.commit()
            print("SAVED TEACHER")
        except Exception as ex:
            print(f"ERROR occured during adding teacher to memory process: {ex}") 

    def add_class(self, cl): # dict
        
        try:
            if cl in self.memories['brain']['classes']['students']:
                print(f"class and students already inside database")
                return
            self.memories['brain']['classes']['students'].append(cl)
            self.commit()
            print("SAVED CLASS")
        except Exception as ex:
            print(f"ERROR occured during adding class to memory process: {ex}") 

    def add_assigment(self, assigment:dict):
        """{
        
            "title": title of the assignment,\n
            "percentage_of_grade": percentage of grade it handles,\n
            "assign_date": the date it was assigned,\n
            "due": the date it is due

        }"""
        try:
            self.memories['brain']['student_assignments'].append(assigment)
            self.commit()
            print("SAVED ASSIGNMENT")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 
   
    def _build_json(self):

        data = Structure.build()
            
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)  # Added indent for readability

        self.memories = data

    def _load_json(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r") as f:
                    self.memories = json.load(f)
                return
            except json.JSONDecodeError:
          
                print("Corrupted memory file, resetting...")
                
        self._build_json()

    def commit(self) -> None:
        try:
            with open(self.file_name, "w") as f:
                json.dump(self.memories, f, indent=4)
        except Exception as ex:
            # Avoid infinite loops; log the error and let the user acknowledge it once
            print(f"Failed to commit changes: {ex}")
            input("Press Enter to acknowledge and continue...")

    def add_to_chat_history(self, info):
        print(f"THE type of info in add_to_chat_history in memory.py: {type(info)}\n")
        print(f"THE content of info in add_to_chat_history in memory.py: {info}")
        d = self.breakdown_dict(info)
        self.memories['brain']['chat_history'].append(d)
    
    def breakdown_dict(self, thing:dict):
        s = {}
        for key, value in thing.items():
            s[key] = value
        return s
    
    def _get_brain(self):
        return self.memories["brain"]