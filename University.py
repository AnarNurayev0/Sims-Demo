from Exceptions import NotFoundError
import Other
import json
import os

PATH_STUDENTS = 'SAVES/students.json'; PATH_TEACHERS = 'SAVES/teachers.json'; PATH_SAVES = 'SAVES'; PATH_IDS = 'IDS'

#_______________________________________________________________________________________#

class _University:

    def __init__(self):

        os.makedirs(PATH_SAVES, exist_ok=True)

        os.makedirs(PATH_IDS, exist_ok=True)

        if not os.path.exists(PATH_STUDENTS):
            with open(PATH_STUDENTS, 'w') as file:
                json.dump({}, file)

        if not os.path.exists(PATH_TEACHERS):
            with open(PATH_TEACHERS, 'w') as file:
                json.dump({}, file)

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
            return
        else:
            raise NotFoundError('The STUDENT file is not exist!')


    #

    def show_student_only(self, id):
        if Other.is_student_file_exists() and os.path.exists(PATH_STUDENTS) > 0:
            data = {}
            with open(PATH_STUDENTS, 'r') as file:
                data = json.load(file)
            if not data:
                print('No Students found!')
            else:
                print(f'{id}', end=' ')
                subjects = data[id]['student_subjects']
                grades = data[id]['student_grades']
                print(
                    f'{data[id]['name']} {data[id]['surname']} - {data[id]['age']} | {data[id]['school']} - {data[id]['department']} - {data[id]['accepted_year']}')
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
                        return
                    else:
                        print('Please enter valid option!')
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def change_student(self):
        if Other.is_student_file_exists() and os.path.getsize(PATH_STUDENTS) > 0:
            with open(PATH_STUDENTS, 'r') as file:
                students = json.load(file)
            if not students:
                print('No students found to change!')
                return
            else:
                while True:
                    print('----------------------------------------------')
                    print()

                    all_ids = []
                    students = {}
                    with open(PATH_STUDENTS, 'r') as file:
                        students = json.load(file)
                        all_ids = [student for student in students]

                    change_int = -1
                    valid_change_count = False
                    while not valid_change_count:
                        change_count = input('Enter the number of students you want to change : ')
                        try:
                            change_count = int(change_count)
                            if change_count <= 0:
                                print("Input must be a valid positive number!")
                            elif change_count > len(all_ids):
                                print('There are less student(s) than that you want to change!')
                            else:
                                change_int = change_count
                                valid_change_count = True
                        except ValueError:
                            print("Input must be a valid positive number!")

                    count = 1
                    if students:
                        print('All Students 🠛')
                        for student in students:
                            print(
                                f'{count}-{student} {students[student]["name"]} {students[student]["surname"]} {students[student]["age"]} | {students[student]["school"]} - {students[student]["department"]} - {students[student]["accepted_year"]}')
                            count += 1
                    else:
                        print('No students found!')
                    print()

                    change = False
                    ct = 0
                    tries = 0
                    while ct < change_int:
                        id = input("Enter the id of the student you want to change (exp : S1234) : ")
                        if id in all_ids:
                            Other.clear_screen()
                            print('-----------------------------------------------------')
                            print('This is the information about the student you want to change!')
                            self.show_student_only(id)
                            print('-----------------------------------------------------')
                            name_check, surname_check, age_check, school_check, department_check = False, False, False, False, False
                            valid_name = valid_surname = valid_school = valid_department = ''
                            valid_age = -1
                            while True:
                                if name_check and surname_check and age_check and school_check and department_check:
                                    break
                                else:
                                    print()
                                    print("Please enter valid name, surname, age, school and department")
                                    print()
                                    name = input(
                                        'Enter the name of the student you want to change : ').strip().capitalize()
                                    surname = input(
                                        'Enter the surname of the student you want to change : ').strip().capitalize()
                                    age = input('Enter the age of the student you want to change : ').strip()
                                    schools_list = list(Other.School)
                                    print("Schools 🠛")
                                    for si, s in enumerate(schools_list, start=1):
                                        print(f'{si} -> {s.value}')

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
                                            for di, d in enumerate(departments_list, start=1):
                                                print(f'{di} -> {d.value}')

                                            department = input(
                                                f'Choose the department (1-{len(departments_list)}) : ').strip()

                                            try:
                                                dept_index = int(department) - 1
                                                if 0 <= dept_index < len(departments_list):
                                                    selected_department = departments_list[dept_index].value
                                                    if Other.department_check(valid_school, selected_department):
                                                        valid_department = selected_department
                                                        department_check = True
                                                else:
                                                    print(
                                                        f"Please choose a number between 1 and {len(departments_list)}!")
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

                            students[id]['name'] = valid_name
                            students[id]['surname'] = valid_surname
                            students[id]['age'] = valid_age
                            students[id]['school'] = valid_school
                            students[id]['department'] = valid_department

                            print('\nStudent changed successfully\n')
                            change = True
                            ct += 1
                        else:
                            print('Student not found!')
                            tries += 1
                            if tries > 3:
                                print('Too many tries!')
                                print('Please try again')
                                with open(PATH_STUDENTS, 'w') as file:
                                    json.dump(students, file, indent=4)
                                Other.exiting()
                                return
                    with open(PATH_STUDENTS, 'w') as file:
                        json.dump(students, file, indent=4)
                    if change:
                        print("\nStudent(s) changed successfully\n")
                    else:
                        print("\nStudent(s) not changed\n")

                    print('You want to change more student(s) now?\n')
                    while True:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.change_student()
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            return
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
                return
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
                                print("Input must be a valid positive number!")
                        except ValueError:
                            print("Input must be a valid positive number!")
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
                            return
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

    def show_teacher_only(self, id):
        if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
            data = {}
            with open(PATH_TEACHERS, 'r') as file:
                data = json.load(file)
            if not data:
                print('No teachers found!')
            else:
                print(f'{id}', end=' ')
                subjects = data[id]['teacher_subjects']
                print(
                    f'{data[id]['name']} {data[id]['surname']} - {data[id]['age']} | {data[id]['salary']}$ - {data[id]['school']}')
                if not subjects:
                    print('No Subjects found!')
                else:
                    print(f'Subjects : ', end='')
                    print(*subjects, sep=', ')
                print()
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
                            name = input('Enter the name of the teacher you want to add : ').strip().capitalize()
                            surname = input('Enter the surname of the teacher you want to add : ').strip().capitalize()
                            age = input('Enter the age of the teacher you want to add : ').strip()
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
                                    salary = input('Enter the salary($) of the teacher you want to add : ').strip()

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
                        return
                    else:
                        print('Please enter valid option!')
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def change_teacher(self):
        if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
            with open(PATH_TEACHERS, 'r') as file:
                teachers = json.load(file)
            if not teachers:
                print('No teachers found to change!')
                return
            else:
                while True:
                    print('----------------------------------------------')
                    print()

                    all_ids = []
                    teachers = {}
                    with open(PATH_TEACHERS, 'r') as file:
                        teachers = json.load(file)
                        all_ids = [teacher for teacher in teachers]

                    change_int = -1
                    valid_change_count = False
                    while not valid_change_count:
                        change_count = input('Enter the number of teachers you want to change : ')
                        try:
                            change_count = int(change_count)
                            if change_count <= 0:
                                print("Input must be a valid positive number!")
                            elif change_count > len(all_ids):
                                print('There are less teacher(s) than that you want to change!')
                            else:
                                change_int = change_count
                                valid_change_count = True
                        except ValueError:
                            print("Input must be a valid positive number!")

                    count = 1
                    if teachers:
                        print('All Teachers 🠛')
                        for teacher in teachers:
                            print(
                                f'{count}-{teacher} {teachers[teacher]["name"]} {teachers[teacher]["surname"]} {teachers[teacher]["age"]} | {teachers[teacher]["salary"]}$ - {teachers[teacher]["school"]} - {teachers[teacher]["accepted_year"]}')
                            count += 1
                    else:
                        print('No teachers found!')
                    print()

                    change = False
                    ct = 0
                    tries = 0
                    while ct < change_int:
                        id = input("Enter the id of the teacher you want to change (exp : T1234) : ")
                        if id in all_ids:
                            Other.clear_screen()
                            print('-----------------------------------------------------')
                            print('This is the information about the teacher you want to change!')
                            self.show_teacher_only(id)
                            print('-----------------------------------------------------')
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
                                    name = input(
                                        'Enter the name of the teacher you want to change : ').strip().capitalize()
                                    surname = input(
                                        'Enter the surname of the teacher you want to change : ').strip().capitalize()
                                    age = input('Enter the age of the teacher you want to change : ').strip()
                                    schools_list = list(Other.School)
                                    print("Schools 🠛")
                                    for si, s in enumerate(schools_list, start=1):
                                        print(f'{si} -> {s.value}')

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
                                            salary = input(
                                                'Enter the salary($) of the teacher you want to change : ').strip()

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

                            teachers[id]['name'] = valid_name
                            teachers[id]['surname'] = valid_surname
                            teachers[id]['age'] = valid_age
                            teachers[id]['school'] = valid_school
                            teachers[id]['salary'] = valid_salary

                            print('\nTeacher changed successfully\n')
                            change = True
                            ct += 1
                        else:
                            print('Teacher not found!')
                            tries += 1
                            if tries > 3:
                                print('Too many tries!')
                                print('Please try again')
                                with open(PATH_TEACHERS, 'w') as file:
                                    json.dump(teachers, file, indent=4)
                                Other.exiting()
                                return

                    with open(PATH_TEACHERS, 'w') as file:
                        json.dump(teachers, file, indent=4)
                    if change:
                        print("\nTeacher(s) changed successfully\n")
                    else:
                        print("\nTeacher(s) not changed\n")

                    print('You want to change more teacher(s) now?\n')
                    while True:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.change_teacher()
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            return
                        else:
                            print('Please enter valid option!')
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def delete_teacher(self):
        if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
            rand = [ ]
            with open(PATH_TEACHERS, 'r') as file:
                teachers = json.load(file)
                rand = [teacher for teacher in teachers]
            if not rand:
                print('No teacher(s) found to delete!')
                return
            else:
                while True:
                    print('----------------------------------------------')
                    print()

                    all_ids = []
                    teachers = {}
                    with open(PATH_TEACHERS, 'r') as file:
                        teachers = json.load(file)
                        all_ids = [teacher for teacher in teachers]

                    delete_int = -1
                    valid_delete_count = False
                    while not valid_delete_count:
                        delete_count = input('Enter the number of teacher(s) to delete : ')
                        try:
                            delete_count = int(delete_count)
                            if delete_count <= 0:
                                print("Input must be a valid positive number!")
                            elif delete_count > len(all_ids):
                                print('There are less teacher(s) than that you want to delete!')
                            else:
                                delete_int = delete_count
                                valid_delete_count = True
                        except ValueError:
                            print("Input must be a valid positive number!")

                    count = 1
                    if teachers:
                        print('All Teachers 🠛')
                        for teacher in teachers:
                            print(
                                f'{count}-{teacher} {teachers[teacher]['name']} {teachers[teacher]['surname']} {teachers[teacher]['age']} | {teachers[teacher]['school']}/{teachers[teacher]['salary']} - {teachers[teacher]['accepted_year']}')
                            count += 1
                    else:
                        print('No teacher(s) found!')
                    print()
                    delete = False
                    with open(PATH_TEACHERS, 'w') as file:
                        ct = 0
                        tries = 0
                        while ct < delete_int:
                            id = input("Enter the id of the teacher you want to delete (exp : T1234) : ")
                            if id in all_ids:
                                teachers.pop(id)
                                ct += 1
                                delete = True
                            else:
                                print('Teacher not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(teachers, file, indent=4)
                                    Other.exiting()
                                    return
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
                            return
                        else:
                            print('Please enter valid option!')
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def add_subjects_to_student(self):
        if Other.is_student_file_exists() and os.path.getsize(PATH_STUDENTS) > 0:
            rand = []
            with open(PATH_STUDENTS, 'r') as file:
                students = json.load(file)
                rand = [student for student in students]
            if not rand:
                print('No student(s) found to make changes!')
                return
            all_ids = []
            while True:
                print('-------------------------------------------')
                print()
                tries = 1
                students = {}
                with open(PATH_STUDENTS, 'r') as file:
                    students = json.load(file)
                    all_ids = [student for student in students]
                change_int = -1
                valid_change_count = False
                while not valid_change_count:
                    change_count = input('Enter the number of student(s) that you want to make changes : ')
                    try:
                        change_count = int(change_count)
                        if change_count <= 0:
                            print("Input must be a valid positive number!")
                            tries+=1
                        elif change_count > len(all_ids):
                            print('There are less student(s) than that you want to make changes!')
                            tries += 1
                        else:
                            change_int = change_count
                            valid_change_count = True
                        if tries > 3:
                            print('Too many tries!')
                            Other.exiting()
                            return
                    except ValueError:
                        print("Input must be a valid positive number!")
                count = 1
                if students:
                    print('All Student(s) 🠛')
                    for student in students:
                        subjects = students[student]['student_subjects']
                        print(f'{count}-{student} {students[student]['name']} {students[student]['surname']} {students[student]['age']} | {students[student]['school']}/{students[student]['department']}')
                        if not subjects:
                            print('No subject(s) found!')
                        else:
                            count_subjects = 1
                            for subject in subjects:
                                print(f'{count_subjects} -> {subject}')
                                count_subjects += 1
                    change = False
                    with open(PATH_STUDENTS, 'r') as file:
                        students = json.load(file)
                    with open(PATH_STUDENTS, 'w') as file:
                        Other.clear_screen()
                        print('---------------------------------------------------')
                        ct = 0
                        tries = 1
                        subjects_int = -1
                        while ct < change_int:
                            tries_subject = 1
                            id = input("Enter the id of the student you want to add subject(s) (exp : S1234) : ")
                            if id in all_ids:
                                okay = False
                                while not okay:
                                    subject_count = input('Enter the number of subject(s) you want to add to this student : ')
                                    try:
                                        int(subject_count)
                                        if int(subject_count) > 0:
                                            subjects_int = int(subject_count)
                                            okay = True
                                        else:
                                            print('Input must be a valid positive integer!')
                                            tries_subject += 1
                                    except ValueError:
                                        print("Input must be a valid positive integer!")
                                        tries_subject += 1
                                    if tries_subject > 3:
                                        print('Too many tries!')
                                        print('Please try again')
                                        json.dump(students, file, indent=4)
                                        Other.exiting()
                                        return
                                ct_subject = 0
                                all_subjects = students[id]['student_subjects']
                                while ct_subject < subjects_int:
                                    Other.clear_screen()
                                    print('-------------------------------------------------------')
                                    new_subject = input('Enter the new subject you want to add to this student : ')
                                    ct_subject += 1
                                    change = True
                                    all_subjects.append(new_subject)
                                students[id]['student_subjects'] = all_subjects
                                ct += 1
                            else:
                                print('Student not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(students, file, indent=4)
                                    Other.exiting()
                                    return
                        json.dump(students, file, indent=4)
                        if change:
                            print("\nSubject(s) added successfully\n")
                        else:
                            print("\nSubject(s) not added\n")
                    print('You want to add more subject(s) now?\n')
                    ifyesno = False
                    while not ifyesno:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.add_subjects_to_student()
                            ifyesno = True
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            ifyesno = True
                            return
                        else:
                            print('Please enter valid option!')
                else:
                    print('No student(s) found!')
                    print('Please try again!')
                    Other.exiting()
                    return
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def add_subjects_to_teachers(self):
        if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
            rand = []
            with open(PATH_TEACHERS, 'r') as file:
                teachers = json.load(file)
                rand = [teacher for teacher in teachers]
            if not rand:
                print('No teacher(s) found to make changes!')
                return
            all_ids = []
            while True:
                print('-------------------------------------------')
                print()
                tries = 1
                teachers = {}
                with open(PATH_TEACHERS, 'r') as file:
                    teachers = json.load(file)
                    all_ids = [teacher for teacher in teachers]
                change_int = -1
                valid_change_count = False
                while not valid_change_count:
                    change_count = input('Enter the number of teacher(s) that you want to make changes : ')
                    try:
                        change_count = int(change_count)
                        if change_count <= 0:
                            print("Input must be a valid positive number!")
                            tries += 1
                        elif change_count > len(all_ids):
                            print('There are less teacher(s) than that you want to make changes!')
                            tries += 1
                        else:
                            change_int = change_count
                            valid_change_count = True
                        if tries > 3:
                            print('Too many tries!')
                            Other.exiting()
                            return
                    except ValueError:
                        print("Input must be a valid positive number!")
                count = 1
                if teachers:
                    print('All Teacher(s) 🠛')
                    for teacher in teachers:
                        subjects = teachers[teacher]['teacher_subjects']
                        print(
                            f'{count}-{teacher} {teachers[teacher]['name']} {teachers[teacher]['surname']} {teachers[teacher]['age']} | {teachers[teacher]['salary']}$ - {teachers[teacher]['school']}')
                        if not subjects:
                            print('No subject(s) found!')
                        else:
                            count_subjects = 1
                            for subject in subjects:
                                print(f'{count_subjects} -> {subject}')
                                count_subjects += 1
                        count += 1
                    change = False
                    with open(PATH_TEACHERS, 'r') as file:
                        teachers = json.load(file)
                    with open(PATH_TEACHERS, 'w') as file:
                        Other.clear_screen()
                        print('---------------------------------------------------')
                        ct = 0
                        tries = 1
                        subjects_int = -1
                        while ct < change_int:
                            tries_subject = 1
                            id = input("Enter the id of the teacher you want to add subject(s) (exp : T1234) : ")
                            if id in all_ids:
                                okay = False
                                while not okay:
                                    subject_count = input(
                                        'Enter the number of subject(s) you want to add to this teacher : ')
                                    try:
                                        int(subject_count)
                                        if int(subject_count) > 0:
                                            subjects_int = int(subject_count)
                                            okay = True
                                        else:
                                            print('Input must be a valid positive integer!')
                                            tries_subject += 1
                                    except ValueError:
                                        print("Input must be a valid positive integer!")
                                        tries_subject += 1
                                    if tries_subject > 3:
                                        print('Too many tries!')
                                        print('Please try again')
                                        json.dump(teachers, file, indent=4)
                                        Other.exiting()
                                        return
                                ct_subject = 0
                                all_subjects = teachers[id]['teacher_subjects']
                                while ct_subject < subjects_int:
                                    Other.clear_screen()
                                    print('-------------------------------------------------------')
                                    new_subject = input('Enter the new subject you want to add to this teacher : ')
                                    ct_subject += 1
                                    change = True
                                    all_subjects.append(new_subject)
                                teachers[id]['teacher_subjects'] = all_subjects
                                ct += 1
                            else:
                                print('Teacher not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(teachers, file, indent=4)
                                    Other.exiting()
                                    return
                        json.dump(teachers, file, indent=4)
                        if change:
                            print("\nSubject(s) added successfully\n")
                        else:
                            print("\nSubject(s) not added\n")
                    print('You want to add more subject(s) now?\n')
                    ifyesno = False
                    while not ifyesno:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.add_subjects_to_teachers()
                            ifyesno = True
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            ifyesno = True
                            return
                        else:
                            print('Please enter valid option!')
                else:
                    print('No teacher(s) found!')
                    print('Please try again!')
                    Other.exiting()
                    return
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

    def add_grades_to_student(self):
        if Other.is_student_file_exists() and os.path.getsize(PATH_STUDENTS) > 0:
            rand = []
            with open(PATH_STUDENTS, 'r') as file:
                students = json.load(file)
                rand = [student for student in students]
            if not rand:
                print('No student(s) found to make changes!')
                return
            all_ids = []
            while True:
                print('-------------------------------------------')
                print()
                tries = 1
                students = {}
                with open(PATH_STUDENTS, 'r') as file:
                    students = json.load(file)
                    all_ids = [student for student in students]
                change_int = -1
                valid_change_count = False
                while not valid_change_count:
                    change_count = input('Enter the number of student(s) that you want to make changes : ')
                    try:
                        change_count = int(change_count)
                        if change_count <= 0:
                            print("Input must be a valid positive number!")
                            tries += 1
                        elif change_count > len(all_ids):
                            print('There are less student(s) than that you want to make changes!')
                            tries += 1
                        else:
                            change_int = change_count
                            valid_change_count = True
                        if tries > 3:
                            print('Too many tries!')
                            Other.exiting()
                            return
                    except ValueError:
                        print("Input must be a valid positive number!")
                count = 1
                if students:
                    print('All Student(s) 🠛')
                    for student in students:
                        grades = students[student]['student_grades']
                        print(
                            f'{count}-{student} {students[student]['name']} {students[student]['surname']} {students[student]['age']} | {students[student]['school']}/{students[student]['department']}')
                        if not grades:
                            print('No grade(s) found!')
                        else:
                            for grade in grades:
                                print(f'{grade} -> {grades[grade]}')
                        count += 1
                    change = False
                    with open(PATH_STUDENTS, 'r') as file:
                        students = json.load(file)
                    with open(PATH_STUDENTS, 'w') as file:
                        Other.clear_screen()
                        print('---------------------------------------------------')
                        ct = 0
                        tries = 1
                        grades_int = -1
                        while ct < change_int:
                            tries_grade = 1
                            id = input("Enter the id of the student you want to add grade(s) (exp : S1234) : ")
                            if id in all_ids:
                                all_subjects = students[id]['student_subjects']
                                if not all_subjects:
                                    print('This student has no subject(s) to add a grade for!')
                                    ct += 1
                                    continue

                                okay = False
                                while not okay:
                                    grade_count = input(
                                        f'Enter the number of grade(s) you want to add to this student (max {len(all_subjects)}) : ')
                                    try:
                                        grade_count = int(grade_count)
                                        if grade_count <= 0:
                                            print('Input must be a valid positive integer!')
                                            tries_grade += 1
                                        elif grade_count > len(all_subjects):
                                            print(
                                                f'This student only has {len(all_subjects)} subject(s), you cannot add more grades than that!')
                                            tries_grade += 1
                                        else:
                                            grades_int = grade_count
                                            okay = True
                                    except ValueError:
                                        print("Input must be a valid positive integer!")
                                        tries_grade += 1
                                    if tries_grade > 3:
                                        print('Too many tries!')
                                        print('Please try again')
                                        json.dump(students, file, indent=4)
                                        Other.exiting()
                                        return

                                ct_grade = 0
                                all_grades = students[id]['student_grades']
                                while ct_grade < grades_int:
                                    Other.clear_screen()
                                    print('-------------------------------------------------------')
                                    print('Subject(s) 🠛')
                                    for i, subj in enumerate(all_subjects, start=1):
                                        print(f'{i} -> {subj}')

                                    subject = input(
                                        'Enter the subject you want to add a grade for : ').strip().capitalize()

                                    if subject not in all_subjects:
                                        print('This subject is not assigned to this student, please add it first!')
                                        continue

                                    grade_ok = False
                                    while not grade_ok:
                                        grade = input(f'Enter the grade for {subject} (0-100) : ').strip()
                                        try:
                                            grade_int = int(grade)
                                            if 0 <= grade_int <= 100:
                                                all_grades[subject] = grade_int
                                                grade_ok = True
                                            else:
                                                print('Grade must be between 0 and 100!')
                                        except ValueError:
                                            print('Grade must be a valid number!')

                                    ct_grade += 1
                                    change = True
                                students[id]['student_grades'] = all_grades
                                ct += 1
                            else:
                                print('Student not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(students, file, indent=4)
                                    Other.exiting()
                                    return
                        json.dump(students, file, indent=4)
                        if change:
                            print("\nGrade(s) added successfully\n")
                        else:
                            print("\nGrade(s) not added\n")
                    print('You want to add more grade(s) now?\n')
                    ifyesno = False
                    while not ifyesno:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.add_grades_to_student()
                            ifyesno = True
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            ifyesno = True
                            return
                        else:
                            print('Please enter valid option!')
                else:
                    print('No student(s) found!')
                    print('Please try again!')
                    Other.exiting()
                    return
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def remove_subject_from_student(self):
        if Other.is_student_file_exists() and os.path.getsize(PATH_STUDENTS) > 0:
            rand = []
            with open(PATH_STUDENTS, 'r') as file:
                students = json.load(file)
                rand = [student for student in students]
            if not rand:
                print('No student(s) found to make changes!')
                return
            all_ids = []
            while True:
                print('-------------------------------------------')
                print()
                tries = 1
                students = {}
                with open(PATH_STUDENTS, 'r') as file:
                    students = json.load(file)
                    all_ids = [student for student in students]
                change_int = -1
                valid_change_count = False
                while not valid_change_count:
                    change_count = input('Enter the number of student(s) that you want to make changes : ')
                    try:
                        change_count = int(change_count)
                        if change_count <= 0:
                            print("Input must be a valid positive number!")
                            tries += 1
                        elif change_count > len(all_ids):
                            print('There are less student(s) than that you want to make changes!')
                            tries += 1
                        else:
                            change_int = change_count
                            valid_change_count = True
                        if tries > 3:
                            print('Too many tries!')
                            Other.exiting()
                            return
                    except ValueError:
                        print("Input must be a valid positive number!")
                count = 1
                if students:
                    print('All Student(s) 🠛')
                    for student in students:
                        subjects = students[student]['student_subjects']
                        print(
                            f'{count}-{student} {students[student]['name']} {students[student]['surname']} {students[student]['age']} | {students[student]['school']}/{students[student]['department']}')
                        if not subjects:
                            print('No subject(s) found!')
                        else:
                            count_subjects = 1
                            for subject in subjects:
                                print(f'{count_subjects} -> {subject}')
                                count_subjects += 1
                        count += 1
                    change = False
                    with open(PATH_STUDENTS, 'r') as file:
                        students = json.load(file)
                    with open(PATH_STUDENTS, 'w') as file:
                        Other.clear_screen()
                        print('---------------------------------------------------')
                        ct = 0
                        tries = 1
                        while ct < change_int:
                            id = input(
                                "Enter the id of the student you want to remove subject(s) from (exp : S1234) : ")
                            if id in all_ids:
                                all_subjects = students[id]['student_subjects']
                                if not all_subjects:
                                    print('This student has no subject(s) to remove!')
                                else:
                                    print('Current subject(s) 🠛')
                                    for i, subj in enumerate(all_subjects, start=1):
                                        print(f'{i} -> {subj}')
                                    subject_to_remove = input(
                                        'Enter the subject you want to remove : ').strip().capitalize()
                                    if subject_to_remove in all_subjects:
                                        all_subjects.remove(subject_to_remove)
                                        students[id]['student_subjects'] = all_subjects

                                        all_grades = students[id]['student_grades']
                                        if subject_to_remove in all_grades:
                                            del all_grades[subject_to_remove]
                                            students[id]['student_grades'] = all_grades

                                        change = True
                                        print(f'{subject_to_remove} removed successfully!')
                                    else:
                                        print('Subject not found for this student!')
                                ct += 1
                            else:
                                print('Student not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(students, file, indent=4)
                                    Other.exiting()
                                    return
                        json.dump(students, file, indent=4)
                        if change:
                            print("\nSubject(s) removed successfully\n")
                        else:
                            print("\nSubject(s) not removed\n")
                    print('You want to remove more subject(s) now?\n')
                    ifyesno = False
                    while not ifyesno:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.remove_subject_from_student()
                            ifyesno = True
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            ifyesno = True
                            return
                        else:
                            print('Please enter valid option!')
                else:
                    print('No student(s) found!')
                    print('Please try again!')
                    Other.exiting()
                    return
        else:
            raise NotFoundError('The STUDENT file is not exist!')

    #

    def remove_subject_from_teacher(self):
        if Other.is_teacher_file_exists() and os.path.getsize(PATH_TEACHERS) > 0:
            rand = []
            with open(PATH_TEACHERS, 'r') as file:
                teachers = json.load(file)
                rand = [teacher for teacher in teachers]
            if not rand:
                print('No teacher(s) found to make changes!')
                return
            all_ids = []
            while True:
                print('-------------------------------------------')
                print()
                tries = 1
                teachers = {}
                with open(PATH_TEACHERS, 'r') as file:
                    teachers = json.load(file)
                    all_ids = [teacher for teacher in teachers]
                change_int = -1
                valid_change_count = False
                while not valid_change_count:
                    change_count = input('Enter the number of teacher(s) that you want to make changes : ')
                    try:
                        change_count = int(change_count)
                        if change_count <= 0:
                            print("Input must be a valid positive number!")
                            tries += 1
                        elif change_count > len(all_ids):
                            print('There are less teacher(s) than that you want to make changes!')
                            tries += 1
                        else:
                            change_int = change_count
                            valid_change_count = True
                        if tries > 3:
                            print('Too many tries!')
                            Other.exiting()
                            return
                    except ValueError:
                        print("Input must be a valid positive number!")
                count = 1
                if teachers:
                    print('All Teacher(s) 🠛')
                    for teacher in teachers:
                        subjects = teachers[teacher]['teacher_subjects']
                        print(
                            f'{count}-{teacher} {teachers[teacher]['name']} {teachers[teacher]['surname']} {teachers[teacher]['age']} | {teachers[teacher]['salary']}$ - {teachers[teacher]['school']}')
                        if not subjects:
                            print('No subject(s) found!')
                        else:
                            count_subjects = 1
                            for subject in subjects:
                                print(f'{count_subjects} -> {subject}')
                                count_subjects += 1
                        count += 1
                    change = False
                    with open(PATH_TEACHERS, 'r') as file:
                        teachers = json.load(file)
                    with open(PATH_TEACHERS, 'w') as file:
                        Other.clear_screen()
                        print('---------------------------------------------------')
                        ct = 0
                        tries = 1
                        while ct < change_int:
                            id = input(
                                "Enter the id of the teacher you want to remove subject(s) from (exp : T1234) : ")
                            if id in all_ids:
                                all_subjects = teachers[id]['teacher_subjects']
                                if not all_subjects:
                                    print('This teacher has no subject(s) to remove!')
                                else:
                                    print('Current subject(s) 🠛')
                                    for i, subj in enumerate(all_subjects, start=1):
                                        print(f'{i} -> {subj}')
                                    subject_to_remove = input(
                                        'Enter the subject you want to remove : ').strip().capitalize()
                                    if subject_to_remove in all_subjects:
                                        all_subjects.remove(subject_to_remove)
                                        teachers[id]['teacher_subjects'] = all_subjects
                                        change = True
                                        print(f'{subject_to_remove} removed successfully!')
                                    else:
                                        print('Subject not found for this teacher!')
                                ct += 1
                            else:
                                print('Teacher not found!')
                                tries += 1
                                if tries > 3:
                                    print('Too many tries!')
                                    print('Please try again')
                                    json.dump(teachers, file, indent=4)
                                    Other.exiting()
                                    return
                        json.dump(teachers, file, indent=4)
                        if change:
                            print("\nSubject(s) removed successfully\n")
                        else:
                            print("\nSubject(s) not removed\n")
                    print('You want to remove more subject(s) now?\n')
                    ifyesno = False
                    while not ifyesno:
                        yesno = input('YES or NO? (Y/N) : ')
                        if yesno == 'Y' or yesno == 'y':
                            self.remove_subject_from_teacher()
                            ifyesno = True
                        elif yesno == 'N' or yesno == 'n':
                            print('\nSee you later !\n')
                            ifyesno = True
                            return
                        else:
                            print('Please enter valid option!')
                else:
                    print('No teacher(s) found!')
                    print('Please try again!')
                    Other.exiting()
                    return
        else:
            raise NotFoundError('The TEACHER file is not exist!')

    #

#_______________________________________________________________________________________#

def create_uni() -> _University:
    uni = _University()
    return uni