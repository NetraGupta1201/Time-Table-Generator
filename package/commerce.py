"""Contains all functions that perform all file operations
related to commerce_streams.csv"""
from package.files.connection import open_file
from package.inputs import yes_or_no
import csv


FILE_NAME = "commerce_streams.csv"


def verify(teachers: list) -> bool:
    """Verifies if all teachers present in parameter teachers
    is present in the file"""
    with open_file(FILE_NAME, "r") as f:
        data = list(csv.reader(f))
    row_count = sum(1 for row in data if row)
    tot_com_t = len(teachers)
    return row_count == tot_com_t


def read(teachers: list) -> tuple:
    """
    Read the data stored in file into main program
    Data in file contains information about the teacher's streams
    Function must be called only if verify() returns True
    """
    entre = []
    business = []
    accounts = []
    with open_file(FILE_NAME, "r") as f:
        data = list(csv.reader(f))
    data = [row for row in data if row]
    for row in data:
        idt, streams = row
        streams = streams.split()
        for t in teachers:
            if t.i_d == int(idt):
                for stream in streams:
                    if stream == "E":
                        entre.append(t)
                    elif stream == "B":
                        business.append(t)
                    elif stream == "A":
                        accounts.append(t)

    return accounts, business, entre


def write(teachers: list) -> tuple:
    """
    Write the science teachers data into the file and update in main program
    teachers parameter must be a list of Teacher objects
    returns tuple of lists of Teacher objects
    function must be called only if verify() returns False
    """
    f = open_file(FILE_NAME, "w")
    writer = csv.writer(f)
    entre = []
    business = []
    accounts = []
    for t in teachers:
        streams = []
        print(f"ID {t.i_d}. {t.f_name} {t.l_name} is a Commerce Teacher")
        for stream in ["Accounts", "Business Studies", "Entrepreneurship"]:
            ch = yes_or_no(f"Does {t.f_name} {t.l_name} teach {stream}?")
            if ch == "Y":
                streams.append(stream[0])  # first letter is sufficient
        writer.writerow((t.i_d, " ".join(streams)))
        for stream in streams:
            if stream == "E":
                entre.append(t)
            elif stream == "B":
                business.append(t)
            elif stream == "A":
                accounts.append(t)
    f.close()
    return accounts, business, entre
