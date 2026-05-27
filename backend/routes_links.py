
#from enum import StrEnum
from strenum import StrEnum

class APIs(StrEnum):
    PEPPER_JSON = "Pepper.json"
    CHAT_HISTORY = "/chat_history"
    BRAIN = "/json"
    ID = "/Id"
    CHAT_LOGS = "/chat_logs"
    RATINGS = "/ratings"
    OVERALL_RATING = "/ratings/overall"
    STUDENTS = "/students"
    TEACHERS = '/teachers'
    TEACHER = "/teacher/<name>"
    STUDENT = "/students/<id>"
    CHAT = "/chat"
    PERIODS = "/periods"
    PERIOD = "/periods/<number>"
    GET_ASSIGNMENTS_ON_GOOGLE_CLASSROOM = "/classroom"
    def format(self, **kwargs):
        return self.value.format(**kwargs)