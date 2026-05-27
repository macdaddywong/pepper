
from typing import Tuple, Any, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from memory_logic.memory import Memory

class Classrooms:
    def __init__(self, memories:"Memory", ai, api_key="", Brain:None=None):
        """'Brain' is a future import of Julius's Psyche software"""

        self.summary_of_each_student:dict[str,list[str]] = {}
        """{"name of student: "summary of student"} """
        self.teachers = []
        self.students_periods:dict[str, list[str]] = {}
        """{"period number (e.q. period_4): "[list of students inside that period]"} """

    def add_class(self, period:int, list_of_students:list):

        self._period_check(period)

        C = f"period_{period}"
        period_check = self.students_periods.get(C, "")
        if period_check:
            while True:
                user = input(f"period {period} already exist (students {period_check}), update? (Y/N)")
                user = user.lower().strip()
                if user != "y":
                    return
                self.students_periods[C] = [i for i in list_of_students]
                return

        new_class = {
            f"period_{period}": [self.get_first_and_last_name(i) for i in list_of_students]
        }
        user = input(f"CLASS {period}, is this correct? (Y/N): \n\t\u2022{new_class} ")
        user = user.strip().lower()
        if user != "y":
            print('please insert correct students names')
            students = []

            while True:
                user = input(f"CLASS {period}, STUDENT NAME: ")
                user = user.strip().lower()
                if not user:
                    continue
                students.append(user)
                more = input("add another?: (Y/N")
                more = user.strip().lower()
                if more != "y":
                    break
                continue
        return new_class
    
    def get_first_and_last_name(self, student:Union[str,tuple]):
        if isinstance(student, tuple):
            # We are ignoring anything greater than 2
            first_name = student[0]
            last_name = student[1]
            return first_name, last_name
        
        half = student.split()
        if len(half) > 1:
            # We are ignoring anything greater than 2
            return half[0], half[1]
        print("Just the first name")
        return student, ""
    
    def remove_class(self, period:int):
        self._period_check(period)
        self._class_exist(period)
        del self.students_periods[f"period_{period}"]

    def add_student(self, student:str, period:int):
        """Period isnt required as the system auto detects if you're not certain"""

        self._period_check(period)
        self._class_exist(period)

        check, c = self._student_in_database(student)
        if check and c[-1] == period:
            highlighted_students = [
                f'\033[31m{s}\033[0m' if s == student else s
                for s in self.students_periods[c]
            ]

            print(
                f"Student is inside provided class already: {highlighted_students}"
            )
            return

        Class = self.students_periods.get(c,None)
        if not Class:
            raise ValueError("Class not found")
        self.students_periods[c] = Class.append(student)
        return student

    def remove_student(self, student:str, period:int=0):
        """Period isnt required as the system auto detects if you're not certain"""
        if period:
            self._period_check(period)
            self._class_exist(period)

        check, c = self._student_in_database(student)
        if not check:
            print("Student is not inside any class")
            return
        if c != f"period_{period}":
            print(f"[WARNING] Student was found in period {c[-1]} but you provided {period}, we'll go with {c[-1]} for now")

        Class = self.students_periods.get(c,None)
        if not Class:
            raise ValueError("Class not found")
        self.students_periods[c] = Class.remove(student)

        
    def add_teacher(self, teacher:str):
        check = self.teachers(teacher)
        if check:
            print("Teacher is already inside system")
            return
        self.teachers.append(teacher)
        return teacher

    def remove_teacher(self, teacher:str):
        check = self.teachers(teacher)
        if not check:
            print("Teacher is not inside system")
            return
        self.teachers.remove(teacher)


    def _period_check(self, period):
        if period < 0 or period > 7:
            raise ValueError(f"There are 7 periods inside burlington high school, not {len(period)}")
        
    def _class_exist(self, period:int) -> bool:
        C = self.students_periods.get(f"period_{period}", None)
        if C is None:
           raise ValueError(f"There is no period {period}")
    
    def _student_in_database(self, student:str)->Tuple[bool, str]:
        student=student.lower().strip()
        for classroom, students in self.students_periods.items():
            if student not in students:
                continue
            print(f"student is in {classroom}")
            return True, classroom
        return False, ""
    
    def _teacher_in_database(self, teacher:str)->Tuple[bool, str]:
        teacher = teacher.lower().strip()
        if teacher not in self.teachers:
            return False
        return True