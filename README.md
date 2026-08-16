# SIMS - Student Information Management System

A simple command-line system I built in Python to manage students and teachers for a university (schools, departments, subjects, grades, salaries - all of it).

No database, no external dependencies - everything is stored in plain JSON files.

## What it does

**Students**
- Add students (with name, surname, age, school, department)
- Show all students
- Change student info
- Delete students
- Add/remove subjects for a student
- Add grades for a student's subjects

**Teachers**
- Add teachers (with name, surname, age, school, salary)
- Show all teachers
- Change teacher info
- Delete teachers
- Add/remove subjects a teacher teaches

## Project structure

```
.
├── main.py          # entry point, runs the menu
├── University.py     # all the actual logic (add/show/change/delete students & teachers)
├── Other.py           # helper functions (validation, ID generation, School/Department enums)
├── Exceptions.py      # custom exceptions (NotFoundError etc.)
└── SAVES/
    ├── students.json  # student data
    └── teachers.json  # teacher data
```

The `SAVES/` folder and the JSON files get created automatically the first time you run it, so you don't need to make them yourself.

## How to run it

```bash
python main.py
```

You'll see a menu, just type the number of what you want to do:

```
1  -> Add Student
2  -> Show Students
3  -> Change Student
4  -> Delete Student
5  -> Add Subject(s) to Student
6  -> Remove Subject from Student
7  -> Add Grade(s) to Student
8  -> Add Teacher
9  -> Show Teachers
10 -> Change Teacher
11 -> Delete Teacher
12 -> Add Subject(s) to Teacher
13 -> Remove Subject from Teacher
0  -> Exit
```

## Notes

- IDs are auto-generated: `S0001`, `S0002`... for students, `T0001`, `T0002`... for teachers
- Schools and departments are picked from a fixed list (no typos possible, you just pick a number)
- Grades are 0-100 and can only be added for a subject the student already has
- Everything gets validated before it's saved (name/surname format, age range, positive numbers etc.)

## Requirements

Just Python 3.10+ (uses f-string nested quotes, so older versions might not work).
