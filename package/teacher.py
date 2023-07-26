"""Functions that perform file operations related to teacher_info.csv"""
from package.files.connection import open_file
from package import inputs as ip
import csv


def read(data: "list[list[str]]"):
    """Print all the teacher data from list data neatly"""
    lst = ["ID", "Name", "Subject", "Grades", "Min classes", "Max classes"]
    print(f"\n{lst[0]:>4} {lst[1]:<25} {lst[2]:<12} {lst[3]:<20} {lst[4]:^12} {lst[5]:^12}")
    for row in data:
        name = row[1] + " " + row[2]
        print(f"{row[0]:>4}. {name:<25} {row[3]:<12} {row[4]:<20} {row[5]:^12} {row[6]:^12}")


def remove():
    """
    Remove a teacher from the file teacher_info.csv
    If user wants to exit without removing a teacher, ValueError is raised
    """
    f = open_file("teacher_info.csv", "r+")
    data = csv.reader(f)
    data = list(data)
    data = [row for row in data if row]
    read(data)
    num = ip.input_to_delete(data)
    if num is False:
        raise ValueError
    for row in data:
        if int(row[0]) == num:
            break
    
    print("The following data is going to be deleted.")
    read([row])
    ch = input("Do you wish to continue? y/n: ").lower()
    while ch not in ("y", "n"):
        ch = input("Invalid input! Enter again: ").lower()
    if ch == "n":
        raise ValueError
    
    data.remove(row)
    f.close()
    f = open_file("teacher_info.csv", "w")
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
    f.close()
    input("Data deleted successfully. Hit enter to continue")


def add():
    """Add a teacher to the file teacher_info.csv"""
    f = open_file("teacher_info.csv", "r+")
    i = 1
    while True:
        print(f"Enter details of teacher {i}")
        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")
        data = list(csv.reader(f))
        i_d = ip.input_id(data)
        subject = ip.input_subject()
        grades = ip.input_grades()
        grades = " ".join(str(grade) for grade in grades)
        min_classes, max_classes = ip.input_min_max_classes()
        row = (i_d, f_name, l_name, subject, grades, min_classes, max_classes)
        f.write("\n")
        writer = csv.writer(f)
        writer.writerow(row)
        choice = ip.yes_or_no("Any more teacher details to enter?")
        if choice == "Y":
            i += 1
        else:
            f.close()
            break


def update():
    """Update the details of an existing teacher in teacher_info.csv"""
    f = open_file("teacher_info.csv", "r")
    data = list(csv.reader(f))
    data = [i for i in data if i]  # remove empty rows
    read(data)
    while True:
        num = ip.input_to_update(data)
        for row in data:
            if int(row[0]) == num:
                print(f"You are editing data for ID {row[0]}: {row[1]} {row[2]}")
                grades = ip.input_grades()
                min, max = ip.input_min_max_classes()
                grades = " ".join(str(g) for g in grades)
                row[4], row[5], row[6] = grades, min, max
                break
        else:
            print("Invalid input. The ID you entered is not present in the file. Try again.")
            continue
        break
    f.close()
    f = open_file("teacher_info.csv", "w")
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()
    input("Data updated successfully. Hit enter to continue")
