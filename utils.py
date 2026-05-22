from typing import Any

class Utils:
    def __init__(self):
        self.count = 1

    def new_doc(self, thing:str):
        l = len(thing)
        print("="*l*2)
        print(thing)
        print("="*l*2)
        print()
        
    def debug(self, thing:Any):
        print(f"[DEBUG {self.count}] \n\t\u2022{thing}\n")
        self.count==1

    def reset_counter(self):
        self.count = 0