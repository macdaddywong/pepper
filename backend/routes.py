from .config import app
from .helpers import get_js, valid_num,valid_student
import logging
from fastapi import HTTPException, Depends
from .routes_links import APIs
from pydantic import BaseModel


logger = logging.getLogger(__name__)



class ChatRequest(BaseModel):
    message: str

# get id
@app.get(APIs.BRAIN)
async def get_Id(js:dict=Depends(get_js)):
    if js is None:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    
    return {"message":"success", "json":js}

# get id
@app.get(APIs.ID)
async def get_Id(js:dict=Depends(get_js)):
    return {"message":"success", "id":js["id"]}

# get chat history
@app.get(APIs.CHAT_HISTORY)
async def get_chat_history(js:dict = Depends(get_js)):
    if js is None:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    
    brain = js.get("brain", "")
    if not brain:
        raise HTTPException(status_code=404, detail="Database or JSON is missing componets")
    
    history = brain['chat_history']
    """
    [{
                "summary": "The user initiated a chat by typing 'just say the word \"test\"' and the response was simply 'Test'. This interaction is brief and lacks context or depth.",
                "emotion": "Neutral",
                "rating": 1
    }],
    
    
    """
    return {"message": "success", "history":history[:10]} # last 10



# get periods
@app.get(APIs.PERIODS)
async def get_all_periods(js = Depends(lambda: get_js(True))):
    if not js:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    
    classes = js.get('classes', {}).get('students', {})
    return {"message":"success", "classes": classes, "amount":len(classes)}


# get a single period (e.g. period 1)
@app.get(APIs.PERIOD)
async def get_period(
    period: int,
    js: dict = Depends(lambda: get_js(only_brain=True))
):
    if not js:
        raise HTTPException(status_code=500, detail="Configuration unavailable")

    valid_num(period)

    classes = js['classes']['students'][0]

    the_class = classes.get(f"period_{period}")

    if not the_class:
        raise HTTPException(
            status_code=404,
            detail=f"Classes period {period} doesn't exist."
        )

    return {
        "message": "success",
        "classes": the_class,
        "amount_of_students": len(the_class)
    }

# get students
@app.get(APIs.STUDENTS)
async def get_all_students(js:dict=Depends(lambda:get_js(True))):
    if not js:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    
    classes = js['classes']['students']
    all_students = []
    for _ in classes:
        students:list = classes.values()
        for student in students:
            all_students.append(student)
    return {"message":"success", "students": all_students}


# get a single student (e.g. only Julius)
@app.get(APIs.STUDENT)
async def get_student(student:str, js:dict=Depends(lambda:get_js(True))):
    there, l = valid_student(student)
    if there:
        return {"message":"success", "possible_students":l[0]}
    
    return  {"message":"success", "possible_students":l}

 # get teachers
@app.get(APIs.TEACHERS)
async def get_all_teachers(js:dict=Depends(lambda:get_js(True))):
    if not js:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    teachers = js["teachers"]
    return {"message":"success", "teachers": teachers}   

# get a single teacher (e.g. only Mr. Wong)
@app.get(APIs.TEACHER)
async def get_teachert(teacher:str, js:dict=Depends(lambda:get_js(True))):
    if not js:
        raise HTTPException(status_code=500, detail="Configuration unavailable")
    
    if teacher not in js['teachers']:
        raise HTTPException(status_code=404, detail=f"The teacher '{teacher}' is not found in the database.")
    return {"message":"success", "teacher":teacher}


