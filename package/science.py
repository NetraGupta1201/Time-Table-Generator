"""Contains all operations related to modifying data in science_streams.csv"""
from __future__ import annotations
from package.files.connection import open_file
import csv

FILE_NAME = "science_streams.csv"


def verify(teachers: list):
    """Verify whether all teachers in parameter are already present in file"""
    with open_file(FILE_NAME, "r") as f:
        data = list(csv.reader(f))
    row_count = sum(1 for row in data if row)  # count no. of rows in file
    tot_sci_t = len(teachers)                  # count no. of science teachers
    return row_count == tot_sci_t              # return True if both equal


def read(teachers: list) -> tuple[list, list, list]:
    """
    Read the data stored in file into main program
    Data in file contains information about the teacher's streams
    Function must be called only if verify() returns True
    """
    physics = []
    chemistry = []
    biology = []
    with open_file(FILE_NAME, "r") as f:
        data = list(csv.reader(f))
    data = [row for row in data if row]  # remove any empty rows
    for row in data:
        idt, stream = row                # idt is id of teacher from data in file
        for t in teachers:
            if t.i_d == int(idt):        # if teacher id is present in file,
                if stream == "P":        # classify Teacher object to respective stream
                    physics.append(t)
                elif stream == "C":
                    chemistry.append(t)
                elif stream == "B":
                    biology.append(t)

    return physics, chemistry, biology


def write(teachers: list) -> tuple[list, list, list]:
    """
    Write the science teachers data into the file and update in main program
    teachers parameter must be a list of Teacher objects
    returns tuple of lists of Teacher objects
    function must be called only if verify() returns False
    """
    f = open_file(FILE_NAME, "w")
    writer = csv.writer(f)
    # initialize lists for the three streams
    physics = []
    chemistry = []
    biology = []
    for t in teachers:
        print("Key:\nC: Chemistry, B: Biology, P: Physics")
        print(f"ID {t.i_d}. {t.f_name} {t.l_name} is a Science Teacher")
        stream = input("Enter the stream. P, C or B: ").upper()
        while True:  # while loop for input validation
            if stream in ("P", "C", "B"):
                break
            print("Please enter a valid choice")
            stream = input("Enter the stream. P, C, B: ").upper()

        writer.writerow((t.i_d, stream))
        # append the teachers to their respective lists
        if stream == "P":
            physics.append(t)
        elif stream == "C":
            chemistry.append(t)
        elif stream == "B":
            biology.append(t)
    f.close()
    return physics, chemistry, biology
