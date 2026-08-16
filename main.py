from University import *
from Other import exiting

def main_menu():
    uni = create_uni()
    while True:
        print('====================================================')
        print('Welcome to the SIMS (Student Information Management System)')
        print('====================================================')
        print('1  -> Add Student')
        print('2  -> Show Students')
        print('3  -> Change Student')
        print('4  -> Delete Student')
        print('5  -> Add Subject(s) to Student')
        print('6  -> Remove Subject from Student')
        print('7  -> Add Grade(s) to Student')
        print('8  -> Add Teacher')
        print('9  -> Show Teachers')
        print('10 -> Change Teacher')
        print('11 -> Delete Teacher')
        print('12 -> Add Subject(s) to Teacher')
        print('13 -> Remove Subject from Teacher')
        print('0  -> Exit')
        print('----------------------------------------------------')

        choice = input('Choose an option : ').strip()

        try:
            if choice == '1':
                uni.add_student()
            elif choice == '2':
                uni.show_student()
            elif choice == '3':
                uni.change_student()
            elif choice == '4':
                uni.delete_student()
            elif choice == '5':
                uni.add_subjects_to_student()
            elif choice == '6':
                uni.remove_subject_from_student()
            elif choice == '7':
                uni.add_grades_to_student()
            elif choice == '8':
                uni.add_teacher()
            elif choice == '9':
                uni.show_teacher()
            elif choice == '10':
                uni.change_teacher()
            elif choice == '11':
                uni.delete_teacher()
            elif choice == '12':
                uni.add_subjects_to_teachers()
            elif choice == '13':
                uni.remove_subject_from_teacher()
            elif choice == '0':
                print('\nSee you later !\n')
                Other.exiting()
                return 0
            else:
                print('Please enter a valid option!')
        except NotFoundError as e:
            print(f'\nError: {e}\n')

        input('\nPress ENTER to continue...')
        Other.clear_screen()

if __name__ == "__main__":
    main_menu()