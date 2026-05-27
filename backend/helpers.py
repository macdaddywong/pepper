
from fastapi import HTTPException
import json
from .routes_links import APIs
from typing import Union, List, Dict, Tuple



def valid_num(period:int):
    if not (1 <= period <= 7):
        raise HTTPException(
            status_code=422,
            detail=f"period '{period}' is not a valid period number, there are only 1 to 7 in 'burlington high school'."
        )
    return period


def valid_student(first_name: str, last_name: str = "") -> Tuple[bool, List[Union[str, None]]]:
    js = get_js(only_brain=True)
    if not js:
        return False, []
        
    possible_students = []
    # 'classes' is likely {"period_1": [["Julius", "C"], ["Alice", "W"]], ...}
    classes = js.get('classes', {}).get('students', {})[0]
    
    for period_name, student_list in classes.items():
        for stu in student_list:
            # stu is [first, last]
            first = stu[0]
            last = stu[1]
            
            # Check for a "fuzzy" match (just first name)
            if first.lower() == first_name.lower():
                # If last name is provided and matches, we found the exact person
                if last_name and last.lower() == last_name.lower():
                    return True, [stu]
                
                # Otherwise, add to possibilities
                possible_students.append(stu)
                
    return (True, possible_students) if possible_students else (False, [])


def get_js(only_brain:bool=False) -> Union[Dict, List, None]:
    try: 
        # Using 'with' is best practice for auto-closing the file
        with open(APIs.PEPPER_JSON, "r") as f:
            js = json.load(f)
        
        if js is None:
            raise HTTPException(status_code=500, detail="Pepper file couldn't be found")

        brain = js.get("brain", "")    
        if not brain:
            raise HTTPException(status_code=500, detail="Pepper file does not include the brain, please check on this issue.")
        
        
        return brain if only_brain else js

    except FileNotFoundError:
        print(f"Error: The file {APIs.PEPPER_JSON} was not found.")
    except json.JSONDecodeError:
        print(f"Error: {APIs.PEPPER_JSON} is not a valid JSON file.")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
    
    return None # Explicitly return None if any error occurs