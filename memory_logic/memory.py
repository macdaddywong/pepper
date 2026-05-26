
import json
from .Structure import Structure
from datetime import datetime, timezone
class Memory:
    def __init__(self, Brain:None=None):
        """'Brain' is a future import of Julius's Psyche software"""
        self.memories = {}
        self.file_name = "Pepper.json"


    def AI_add_to_memory(self, ai_summary:dict):
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
            print("SAVED SUMMARY")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 


    def add_teacher(self, teacher:str):
        
        try:
            self.memories[0]['brain']['teachers'].append(teacher)
            self.commit()
            print("SAVED TEACHER")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 

    def add_class(self, cl:dict):
        
        try:
            self.memories[0]['brain']['classes'].append(cl)
            self.commit()
            print("SAVED CLASS")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 

    def add_assigment(self, assigment:dict):
        """{
        
            "title": title of the assignment,\n
            "percentage_of_grade": percentage of grade it handles,\n
            "assign_date": the date it was assigned,\n
            "due": the date it is due

        }"""
        try:
            self.memories[0]['brain']['student_assignemnts'].append(assigment)
            self.commit()
            print("SAVED ASSIGNMENT")
        except Exception as ex:
            print(f"ERROR occured during adding memory process: {ex}") 
   
    def _build_json(self):
        import os
        data = Structure.build()
        if os.path.exists(self.file_name):
            return 
            
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)  # Added indent for readability

        self.memories = data


    def commit(self) -> None:
        try:
            with open(self.file_name, "w") as f:
                json.dump(self.memories, f, indent=4)
        except Exception as ex:
            # Avoid infinite loops; log the error and let the user acknowledge it once
            print(f"Failed to commit changes: {ex}")
            input("Press Enter to acknowledge and continue...")

    def _get_brain(self):
        return self.memories[0]["brain"]