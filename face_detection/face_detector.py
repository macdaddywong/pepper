import subprocess



class FaceDector:
    """Pepper has a built in face tracker"""
    def __init__(self, ip:str="172.17.10.113"):
        self.ip = ip
        
    def lock_face(self):
        cmd = [
            'ssh',
        ]