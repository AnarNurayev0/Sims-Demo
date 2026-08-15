from Exceptions import InvalidGradeError, EnrollmentError, NotFoundError
from abc import ABC, abstractmethod
import Other
import json
import sys
import os

PATH_STUDENTS = 'SAVES/students.json'; PATH_TEACHERS = 'SAVES/teachers.json'

#_______________________________________________________________________________________#

class _University:
    def __init__(self):
        ...

    #

    def show_student(self):
        if Other.is_student_file_exists():
            data = {}
            with open(PATH_STUDENTS,'r') as file:
                data = json.load(file)
            if not data:
                print('No Students found!')
            else:
                count = 1
                for key in data:
                    print(f'{count}-{key}',end=' ')
                    subjects = data[key]['student_subjects']
                    grades = data[key]['student_grades']
                    print(f'{data[key]['name']} {data[key]['surname']} - {data[key]['age']} | {data[key]['school']} - {data[key]['department']} - {data[key]['accepted_year']}')
                    if not subjects:
                        print('No Subjects found!')
                    else:
                        print(f'Subjects : ', end='')
                        print(*subjects, sep=', ')
                    if not grades:
                        print('No Grades found!')
                    else:
                        print('Grades 🠛')
                        for grade in grades:
                            print(f'{grade} -> {grades[grade]}')
                    print()
                    count+=1
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def add_student(self):
        if Other.is_student_file_exists():
            while True:
                print('----------------------------------------------')
                while True:
                    try:
                        count = input('Enter the amount of student(s) you want to add : ')
                        if int(count) > 0:
                            break
                    except ValueError:
                        print()
                        print('Please enter a valid positive integer')
                for st in range(int(count)):
                    ID = Other.id_generator_student()
                    name_check, surname_check, age_check, school_check, department_check= False, False, False, False, False
                    valid_name = valid_surname = valid_school = valid_department = ''
                    valid_age = -1
                    while True:
                        if name_check and surname_check and age_check and school_check and department_check:
                            break
                        else:
                            print()
                            print("Please enter valid name, surname, age, school and department")
                            print()
                            name = input('Enter the name of the student you want to add : ').strip().capitalize()
                            surname = input('Enter the surname of the student you want to add : ').strip().capitalize()
                            age = input('Enter the age of the student you want to add : ').strip()
                            schools_list = list(Other.School)
                            print("Schools 🠛")
                            for i, s in enumerate(schools_list, start=1):
                                print(f'{i} -> {s.value}')

                            school = input('Choose the school (1-6) : ').strip()

                            try:
                                school_index = int(school) - 1
                                if 0 <= school_index < len(schools_list):
                                    selected_school = schools_list[school_index].value
                                    if Other.school_check(selected_school):
                                        valid_school = selected_school
                                        school_check = True
                                else:
                                    print("Please choose a number between 1 and 6!")
                            except ValueError:
                                print("Please enter a valid number!")

                            if school_check:
                                dept_enum_class = Other.get_departments_for_school(valid_school)
                                if dept_enum_class is None:
                                    print("Something went wrong with the selected school, please try again!")
                                else:
                                    departments_list = list(dept_enum_class)

                                    print("Departments 🠛")
                                    for i, d in enumerate(departments_list, start=1):
                                        print(f'{i} -> {d.value}')

                                    department = input(f'Choose the department (1-{len(departments_list)}) : ').strip()

                                    try:
                                        dept_index = int(department) - 1
                                        if 0 <= dept_index < len(departments_list):
                                            selected_department = departments_list[dept_index].value
                                            if Other.department_check(valid_school, selected_department):
                                                valid_department = selected_department
                                                department_check = True
                                        else:
                                            print(f"Please choose a number between 1 and {len(departments_list)}!")
                                    except ValueError:
                                        print("Please enter a valid number!")

                            try:
                                age_int = int(age)
                                if 16 < age_int and Other.age_check(age_int):
                                    valid_age = age_int
                                    age_check = True
                            except ValueError:
                                print("Age must be a valid number!")
                            if isinstance(name, str) and name != '' and Other.name_check(name):
                                valid_name = name
                                name_check = True
                            if isinstance(surname, str) and surname != '' and Other.surname_check(surname):
                                valid_surname = surname
                                surname_check = True

                    if Other.is_student_file_exists() and os.path.getsize(PATH_STUDENTS) > 0:
                        with open(PATH_STUDENTS, 'r') as file:
                            students = json.load(file)
                    else:
                        students = {}

                    students[ID] = {
                        'name': valid_name,
                        'surname': valid_surname,
                        'age': valid_age,
                        'school': valid_school,
                        'department': valid_department,
                        'accepted_year': Other.get_time('year'),
                        'student_subjects': [ ],
                        'student_grades': { }
                    }

                    with open(PATH_STUDENTS, 'w') as file:
                        json.dump(students, file, indent=4)

                    print('\nStudent added successfully\n')

                print('\nAll students added successfully\n')
                print('You want to add more students now?\n')
                while True:
                    yesno = input('YES or NO? (Y/N) : ')
                    if yesno == 'Y' or yesno == 'y':
                        self.add_student()
                    elif yesno == 'N' or yesno == 'n':
                        print('\nSee you later !\n')
                        sys.exit()
                    else:
                        print('Please enter valid option!')
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def delete_student(self):
        if Other.is_student_file_exists():
            rand = [ ]
            with open(PATH_STUDENTS, 'r') as file:
                students = json.load(file)
                all_ids = [student for student in students]
            if not rand:
                print('No students found to delete!')
                sys.exit()
            else:
                while True:
                    print('----------------------------------------------')
                    print()
                    delete_int = -1
                    valid_delete_count = False
                    while not valid_delete_count:
                        delete_count = input('Enter the number of students to delete : ')
                        try:
                            delete_count = int(delete_count)
                            if 0 < delete_count :
                                delete_int = delete_count
                                valid_delete_count = True
                            else:
                                print("Age must be a valid positive number!")
                        except ValueError:
                            print("Age must be a valid positive number!")
                    all_ids = [ ]
                    students = {}
                    count = 1
                    with open(PATH_STUDENTS, 'r') as file:
                        students = json.load(file)
                        all_ids = [student for student in students]
                        print('All Students 🠛')
                        for student in students:
                            print(f'{count}-{student} {students[student]['name']} {students[student]['surname']} {students[student]['age']} | {students[student]['school']} - {students[student]['department']} - {students[student]['accepted_year']}')
                            count+=1
                    print()
                    delete = False
                    with open(PATH_STUDENTS, 'w') as file:
                        for i in range(delete_int):
                            id = input("Enter the id of the student you want to delete (exp : S0000) : ")
                            if id in all_ids:
                                students.pop(id)
                                delete = True
                            else:
                                print('Student not found!')
                                i+=1
                        json.dump(students, file, indent=4)
                        if delete:
                            print("\nStudent(s) deleted successfully\n")
                        else:
                            print("\nStudent(s) not deleted\n")
                    print('You want to delete more students now?\n')
                    while True:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.delete_student()
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            sys.exit()
                        else:
                            print('Please enter valid option!')
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def show_teacher(self):
        if Other.is_teacher_file_exists():
            data = {}
            with open(PATH_TEACHERS, 'r') as file:
                data = json.load(file)

            if not data:
                print("No teachers found!")
            else:
                count = 1
                for key in data:
                    print(f'{count}-{key}', end=' ')
                    subjects = data[key]['teacher_subjects']
                    print(f'{data[key]['name']} {data[key]['surname']} - {data[key]['age']} | {data[key]['salary']}$ - {data[key]['school']}')
                    if not subjects:
                        print('No Subjects found!')
                    else:
                        print(f'Subjects : ', end='')
                        print(*subjects, sep=', ')
                    print()
                    count += 1
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def add_teacher(self):
        if Other.is_teacher_file_exists():
            while True:
                print('----------------------------------------------')
                while True:
                    try:
                        count = input('Enter the amount of teacher(s) you want to add : ')
                        if int(count) > 0:
                            break
                    except ValueError:
                        print()
                        print('Please enter a valid positive integer')
                for st in range(int(count)):
                    ID = Other.id_generator_teacher()
                    name_check, surname_check, age_check, school_check, salary_check = False, False, False, False, False
                    valid_name = valid_surname = valid_school = ''
                    valid_age = valid_salary = -1
                    while True:
                        if name_check and surname_check and age_check and school_check and salary_check:
                            break
                        else:
                            print()
                            print("Please enter valid name, surname, age, school and salary")
                            print()
                            name = input('Enter the name of the student you want to add : ').strip().capitalize()
                            surname = input('Enter the surname of the student you want to add : ').strip().capitalize()
                            age = input('Enter the age of the student you want to add : ').strip()
                            schools_list = list(Other.School)
                            print("Schools 🠛")
                            for i, s in enumerate(schools_list, start=1):
                                print(f'{i} -> {s.value}')

                            school = input('Choose the school (1-6) : ').strip()

                            try:
                                school_index = int(school) - 1
                                if 0 <= school_index < len(schools_list):
                                    selected_school = schools_list[school_index].value
                                    if Other.school_check(selected_school):
                                        valid_school = selected_school
                                        school_check = True
                                else:
                                    print("Please choose a number between 1 and 6!")
                            except ValueError:
                                print("Please enter a valid number!")

                            if school_check:
                                dept_enum_class = Other.get_departments_for_school(valid_school)
                                if dept_enum_class is None:
                                    print("Something went wrong with the selected school, please try again!")
                                else:
                                    salary = input('Enter the salary of the teacher you want to add : ').strip()

                                    try:
                                        salary_int = int(salary)
                                        if salary_int > 0:
                                            valid_salary = salary_int
                                            salary_check = True
                                        else:
                                            print("Salary must be a valid positive number!")
                                    except ValueError:
                                        print("Salary must be a valid positive number!")
                            try:
                                age_int = int(age)
                                if 16 < age_int and Other.age_check(age_int):
                                    valid_age = age_int
                                    age_check = True
                            except ValueError:
                                print("Age must be a valid number!")
                            if isinstance(name, str) and name != '' and Other.name_check(name):
                                valid_name = name
                                name_check = True
                            if isinstance(surname, str) and surname != '' and Other.surname_check(surname):
                                valid_surname = surname
                                surname_check = True

                    if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
                        with open(PATH_TEACHERS, 'r') as file:
                            teachers = json.load(file)
                    else:
                        teachers = {}

                    teachers[ID] = {
                        'name': valid_name,
                        'surname': valid_surname,
                        'age': valid_age,
                        'school': valid_school,
                        'accepted_year': Other.get_time('year'),
                        'teacher_subjects': [],
                        'salary': valid_salary
                    }

                    with open(PATH_TEACHERS, 'w') as file:
                        json.dump(teachers, file, indent=4)

                    print('\nTeacher(s) added successfully\n')

                print('\nAll teacher(s) added successfully\n')
                print('You want to add more teacher(s) now?\n')
                while True:
                    yesno = input('YES or NO? (Y/N) : ')
                    if yesno == 'Y' or yesno == 'y':
                        self.add_student()
                    elif yesno == 'N' or yesno == 'n':
                        print('\nSee you later !\n')
                        sys.exit()
                    else:
                        print('Please enter valid option!')
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def delete_teacher(self):
        if Other.is_teacher_file_exists():
            rand = [ ]
            with open(PATH_TEACHERS, 'r') as file:
                teachers = json.load(file)
                rand = [teacher for teacher in teachers]
            if not rand:
                print('No teachers found to delete!')
                sys.exit()
            else:
                while True:
                    print('----------------------------------------------')
                    print()
                    delete_int = -1
                    valid_delete_count = False
                    while not valid_delete_count:
                        delete_count = input('Enter the number of teacher(s) to delete : ')
                        try:
                            delete_count = int(delete_count)
                            if 0 < delete_count:
                                delete_int = delete_count
                                valid_delete_count = True
                            else:
                                print("Input must be a valid positive number!")
                        except ValueError:
                            print("Input must be a valid positive number!")
                    all_ids = []
                    teachers = {}
                    count = 1
                    with open(PATH_TEACHERS, 'r') as file:
                        teachers = json.load(file)
                        all_ids = [teacher for teacher in teachers]
                        if teachers:
                            print('All Teachers 🠛')
                            for teacher in teachers:
                                print(
                                    f'{count}-{teacher} {teachers[teacher]['name']} {teachers[teacher]['surname']} {teachers[teacher]['age']} | {teachers[teacher]['school']} - {teachers[teacher]['accepted_year']}')
                                count += 1
                        else:
                            print('No teacher(s) found!')
                    print()
                    delete = False
                    with open(PATH_TEACHERS, 'w') as file:
                        for i in range(delete_int):
                            id = input("Enter the id of the teacher you want to delete (exp : S0000) : ")
                            if id in all_ids:
                                teachers.pop(id)
                                delete = True
                            else:
                                print('Teacher not found!')
                                i += 1
                        json.dump(teachers, file, indent=4)
                        if delete:
                            print("\nTeacher(s) deleted successfully\n")
                        else:
                            print("\nTeacher(s) not deleted\n")
                    print('You want to delete more teacher(s) now?\n')
                    while True:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.delete_student()
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            sys.exit()
                        else:
                            print('Please enter valid option!')
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def add_subjects_to_student(self):
        if Other.is_student_file_exists():
            ...

        else:
            raise NotFoundError('The STUDENT file is not exist!')

if __name__ == '__main__':
    uni = _University()
    # uni.add_student()
    # uni.show_student()
    # uni.delete_student()
    # uni.show_teacher()
    # uni.add_teacher()
    # uni.delete_teacher()