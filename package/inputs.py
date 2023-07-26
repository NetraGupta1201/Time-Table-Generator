"""Input functions used in various tasks; input validation"""
from __future__ import annotations
ALL_SUBJECTS = (  # all subjects taught at the school
    "Maths",
    "English",
    "Hindi",
    "Tamil",
    "Sanskrit",
    "Evs",
    "Science",
    "Sst",
    "Computers",
    "Craft",
    "Morals",
    "Library",
    "Pt",
    "Drawing",
    "Yoga",
    "Music",
    "Economics",
    "Commerce",
)


def input_to_delete(data: list[list[str]]) -> int:
    """Input the ID of the teacher to be deleted from file"""
    all_ids = [row[0] for row in data]
    print("Now you will be deleting a teacher.")
    num = input("Enter ID of the teacher or Q to exit: ").capitalize()
    while True:
        if num.isdigit() and num in all_ids:
            break
        elif num == "Q":
            return False
        print("Invalid Input!")
        num = input("Enter: ").capitalize()
    return int(num)


def input_to_update(data: list[list[str]]) -> int:
    """Input the ID of the teacher to be updated in file"""
    all_ids = [row[0] for row in data]
    print("Now you will be updating a teacher.")
    num = input("Enter ID of the teacher: ").capitalize()
    while True:
        if num.isdigit() and num in all_ids:
            break
        print("Invalid Input!")
        num = input("Enter: ").capitalize()
    return int(num)


def input_subject() -> str:
    """Input the subject taken by new teacher to be added"""
    print("""
    Next, you will be entering the subject of the teacher.
    Please enter any of the following options.
    """)
    for sub in ALL_SUBJECTS:
        print(f"\t{sub}")
    print()
    subject = input("Enter subject: ").capitalize()
    while subject not in ALL_SUBJECTS:
        print("Invalid Input!")
        subject = input("Enter subject: ").capitalize()

    return subject


def input_id(data: list[list[str]]) -> int:
    data = [row for row in data if row]
    i_d = input("Enter ID of your new teacher: ")
    while True:
        if i_d.isdigit():
            for row in data:
                if int(row[0]) == int(i_d):
                    print(f"ID already exists and in use by {row[1]} {row[2]}")
                    i_d = input("Enter again: ")
                    break
            else:
                break
        else:
            print("ID can only be a number.")
            i_d = input("Enter again: ")

    return int(i_d)


def input_grades() -> list[int]:
    """Input the grades/classes taken by the new teacher to be added"""
    grades = []
    while True:
        grade = input("Enter grade or \"Q\" to exit: ").capitalize()
        if grade.isdigit() and int(grade) not in range(1, 13):
            print("Please enter a grade between 1 and 12!!")
            continue
        if not grade.isdigit() and grade != "Q":
            print("Invalid Input")
            continue
        if grade.isdigit() and int(grade) in grades:
            print("Grade already entered")
            continue
        if grade.isdigit():
            grades.append(int(grade))
        if grade == "Q" and grades:
            break
    return grades


def input_min_max_classes() -> tuple[int, int]:
    """Input min and max classes to be taken by new teacher to be added"""
    while True:
        min_c = input("Enter minimum classes taken by the teacher: ")
        while min_c.isdigit() is False:
            print("Please enter only numbers!!")
            min_c = input("Enter minimum classes taken by the teacher: ")

        max_c = input("Enter maximum classes the teacher can take: ")
        while max_c.isdigit() is False:
            print("Please enter only numbers!!")
            max_c = input("Enter maximum classes to be taken by the teacher: ")

        if int(max_c) >= int(min_c):
            break
        print("Max value must be greater than min value!!!!")
    return min_c, max_c


def yes_or_no(msg: str = "") -> str:
    """Take a yes or no input from the user and validate input"""
    choice = input(f"{msg} Y/N: ").upper()
    while choice not in ("Y", "N"):
        print("Invalid Input!")
        choice = input("Please enter Y/N: ").upper()
    return choice


def input_file_name() -> str:
    """asks user to input only a valid file name; check for illegal chars"""
    name = input("Please enter the file name of your output file: ")
    illegal = ("\\", "*", "/", "?", "|", "<", ">", "\"", ":")
    while True:
        for char in name:
            if char in illegal:
                print(f"You entered an illegal character {char}")
                name = input("Please enter a valid file name: ")
                break
        else:
            break

    return name
