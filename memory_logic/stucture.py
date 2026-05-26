

from typing import Any, Dict
import uuid
from datetime import timezone, datetime


class Stucture: 
    def build(self, name)->Dict[str,Any]:


        S = {
            "id":str(uuid.uuid4()),
            "brain": {
                "name": name,
                "teachers": [],
                "memories": [],
                "chat_history": [],
                "date_of_activation":datetime.today(tz=timezone.utc),
                "core": ""
            }
        }



        return S