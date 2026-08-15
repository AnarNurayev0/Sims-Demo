from enum import Enum, Flag, auto
import time
import os
import re

PATH_STUDENTS = 'SAVES/students.json'; PATH_TEACHERS = 'SAVES/teachers.json'

#_______________________________________________________________________________________#

def id_generator_student():

    FILE_S = 'IDS/last_id_s.txt'

    if os.path.exists(FILE_S):
        with open(FILE_S, "r") as f:
            last_id = int(f.read().strip())
    else:
        last_id = 0

    new_id = last_id + 1

    with open(FILE_S, "w") as f:
        f.write(str(new_id))

    return f"S{new_id:04d}"

#_______________________________________________________________________________________#

def id_generator_teacher():

    FILE_T = 'IDS/last_id_t.txt'

    if os.path.exists(FILE_T):
        with open(FILE_T, "r") as f:
            last_id = int(f.read().strip())
    else:
        last_id = 0

    new_id = last_id + 1

    with open(FILE_T, "w") as f:
        f.write(str(new_id))

    return f"T{new_id:04d}"

#_______________________________________________________________________________________#

def name_check(name):

    pattern = re.compile(r'^[A-Z][a-z]+$')

    if pattern.match(name) and name != ' ':
        return True
    return False

#_______________________________________________________________________________________#

def age_check(age):

    age = str(age)

    pattern = re.compile(r'^\d{1,3}$')

    if pattern.match(age):
        return True
    return False

#_______________________________________________________________________________________#

def surname_check(surname):

    pattern = re.compile(r'^[A-Z][a-z]+$')

    if pattern.match(surname):
        return True
    return False

#_______________________________________________________________________________________#

class School(Enum):
    SCIENCE_ENGINEERING = "School of Science and Engineering"
    ECONOMICS_MANAGEMENT = "School of Economics and Management"
    HUMANITIES_EDUCATION = "School of Humanities, Education and Social Sciences"
    GRAD_SCIENCE_ART_TECH = "Graduate School of Science, Art and Technology"
    GRAD_ECONOMICS_BUSINESS = "Graduate School of Economics and Business"
    VETERINARY_MEDICINE = "Hasvet School of Veterinary Medicine"

def school_check(school):
    try:
        School(school)
        return True
    except ValueError:
        return False

#_______________________________________________________________________________________#

class Departments:
    class SCHOOL_OF_SCIENCE_AND_ENGINEERING(Enum):
        LIFE_SCIENCE = "Life Sciences"
        COMPUTER_SCIENCE = "Computer Science"
        PHYSICS_AND_ELECTRONICS = "Physics and Electronics"
        CIVIL_ENGINEERING = "Civil Engineering"
        PETROLEUM_ENGINEERING = "Petroleum Engineering"
        CHEMISTRY_AND_CHEMICAL_ENGINEERING = "Chemistry and Chemistry Engineering"
        MECHANICAL_ENGINEERING = "Mechanical Engineering"
        MATHEMATICS = "Mathematics"
        GEOGRAPHY_AND_ENVIRONMENT = "Geography and Environment"
        ARCHITECTURE_AND_DESIGN = "Architecture and Design"

    class SCHOOL_OF_ECONOMICS_AND_MANAGEMENT(Enum):
        ECONOMICS = "Economics"
        MANAGEMENT = "Management"
        MARKETING = "Marketing"
        ACCOUNTING_AND_FINANCE = "Accounting and Finance"

    class SCHOOL_OF_HUMANITIES_EDUCATION_AND_SOCIAL_SCIENCES(Enum):
        LAW = "Law"
        LANGUAGES_AND_LITERATURES = "Languages and Literatures"
        EDUCATION = "Education"
        ENGLISH_LANGUAGE_AND_LITERATURE = "English Language and Literature"
        HISTORY_AND_ARCHAEOLOGY = "History and Archaeology"
        MUSIC_AND_FINE_ARTS = "Music and Fine Arts"
        POLITICAL_SCIENCE_AND_PHILOSOPHY = "Political Science and Philosophy"
        PSYCHOLOGY = "Psychology"

    class GRADUATE_SCHOOL_OF_SCIENCE_ART_AND_TECHNOLOGY(Enum):
        COMPUTER_ENGINEERING = "Computer Engineering"
        DATA_SCIENCE_AND_AI = "Data Science and Artificial Intelligence"
        BIOTECHNOLOGY = "Biotechnology"
        ENERGY_ENGINEERING = "Energy Engineering"
        DESIGN_AND_INNOVATION = "Design and Innovation"

    class GRADUATE_SCHOOL_OF_ECONOMICS_AND_BUSINESS(Enum):
        BUSINESS_ADMINISTRATION = "Business Administration"
        FINANCE_AND_BANKING = "Finance and Banking"
        APPLIED_ECONOMICS = "Applied Economics"
        INTERNATIONAL_TRADE = "International Trade"

    class HASVET_SCHOOL_OF_VETERINARY_MEDICINE(Enum):
        VETERINARY_MEDICINE = "Veterinary Medicine"
        ANIMAL_SCIENCE = "Animal Science"
        VETERINARY_PUBLIC_HEALTH = "Veterinary Public Health"

SCHOOL_DEPARTMENTS_MAP = {
    School.SCIENCE_ENGINEERING: Departments.SCHOOL_OF_SCIENCE_AND_ENGINEERING,
    School.ECONOMICS_MANAGEMENT: Departments.SCHOOL_OF_ECONOMICS_AND_MANAGEMENT,
    School.HUMANITIES_EDUCATION: Departments.SCHOOL_OF_HUMANITIES_EDUCATION_AND_SOCIAL_SCIENCES,
    School.GRAD_SCIENCE_ART_TECH: Departments.GRADUATE_SCHOOL_OF_SCIENCE_ART_AND_TECHNOLOGY,
    School.GRAD_ECONOMICS_BUSINESS: Departments.GRADUATE_SCHOOL_OF_ECONOMICS_AND_BUSINESS,
    School.VETERINARY_MEDICINE: Departments.HASVET_SCHOOL_OF_VETERINARY_MEDICINE,
}

def get_departments_for_school(school_value):
    try:
        school_enum = School(school_value)
    except ValueError:
        return None
    return SCHOOL_DEPARTMENTS_MAP.get(school_enum)

def department_check(school_value, department_value):
    dept_enum_class = get_departments_for_school(school_value)
    if dept_enum_class is None:
        return False
    try:
        dept_enum_class(department_value)
        return True
    except ValueError:
        return False

#_______________________________________________________________________________________#

def exiting():

    print('\nGoodbye!')
    print('Exiting', end='')

    for i in range(3):
        time.sleep(0.5)
        print('.', end='')

#_______________________________________________________________________________________#

def is_student_file_exists():
    if os.path.exists(PATH_STUDENTS):
        return True
    return False

#_______________________________________________________________________________________#

def is_teacher_file_exists():
    if os.path.exists(PATH_TEACHERS):
        return True
    return False

#_______________________________________________________________________________________#

def get_time(tm):
    TIME = [time.localtime().tm_year,
    time.localtime().tm_mon,
    time.localtime().tm_mday,
    time.localtime().tm_hour,
    time.localtime().tm_min,
    time.localtime().tm_sec ]

    match tm:
        case 'year':
            return TIME[0]
        case 'month':
            return TIME[1]
        case 'day':
            return TIME[2]
        case 'hour':
            return TIME[3]
        case 'minute':
            return TIME[4]
        case 'second':
            return TIME[5]
        case _:
            return None