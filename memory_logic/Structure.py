

from typing import Any, Dict
import uuid
from datetime import timezone, datetime


class Structure: 
    def build()->Dict[str,Any]:


        S = {
            "id":str(uuid.uuid4()),
            "brain": {
                "name": "Pepper the bot",
                "teachers": [],
                "classes":[],
                "student_assignemnts":[],
                "memories": [],
                "chat_history": [],
                "date_of_activation":str(datetime.now(tz=timezone.utc)),
                "core": ""
            }
        }



        return S