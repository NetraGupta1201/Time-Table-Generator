"""Contains the objects used in the program"""
from __future__ import annotations
from package.display import display_table


# TABLE: Base layout for all tables
# Contains 1 to 47 positions from monday to saturday
# First slot is empty so that positions and indexing are same
TABLE = [""] + [str(i) for i in range(1, 48)]


class Teacher:
    """
    Represents a teacher.
    Attributes:
        i_d: int
            teacher ID, must be unique
        f_name: str
            teacher's first name
        l_name: str
            teacher's last name
        subject: str
            subject taught by the teacher
        grades: tuple(int)
            classes taught by the teacher (eg. 6th, 7th)
        min_c: int
            minimum classes to be taken by the teacher
        max_c: int
            maximum classes to be taken by the teacher
        assigned_classes: dict
            classes that have been assigned to the teacher
        schedule: list
            teacher's time table

    """
    def __init__(self, i_d: int, f_name: str, l_name: str, subject: str, grades: tuple[int], min_c: int, max_c: int):
        self.i_d = i_d
        self.f_name = f_name
        self.l_name = l_name
        self.subject = subject
        self.grades = grades
        self.assigned_classes = {}
        self.schedule = list(TABLE)
        self.min_c = min_c
        self.max_c = max_c

    def new_assigned_class(self, clss: Grade):
        """Update details when teacher is assigned a class
        Parameters
            clss: the class that has been assigned (Grade object)
        """
        self.assigned_classes[str(clss.grade) + clss.section] = clss

    def update(self, pos: str | int, grade: int, section: str):
        """Update a position in schedule"""
        self.schedule[int(pos)] = str(grade) + section

    def print_schedule(self):
        """Print the teacher schedule/time table"""
        s = []
        for pos in self.schedule:
            # Show numbers as empty spaces
            if pos.isdigit():
                s.append("")
            else:
                s.append(pos)

        print(self.f_name, self.l_name)
        if self.schedule != TABLE:  # Print schedule only if not empty
            display_table(s)
        else:
            print("Schedule is empty.")

    def is_free(self, *args: str) -> bool:
        """Check if teacher is free for all positions in args"""
        return all(self.schedule[int(pos)].isdigit() for pos in args)

    def reset_schedule(self):
        self.schedule = list(TABLE)

    def reset_all(self):
        self.schedule = list(TABLE)
        self.assigned_classes = {}


# Class object handles all class details
class Grade:
    """
    Represents a class.
    Attributes:
        grade: int
            grade of the class
        section: str
            section of the class
        main_subs: tuple(str)
            the main subjects of the class
        add_subs: dict(str: int)
            keys: additional subjects of the class, values: frequency per week
        grades: tuple(int)
            classes taught by the teacher (eg. 6th, 7th)
        faculty: dict(str: Teacher)
            all the class's faculty stored in dictionary
        schedule: list
            class's time table
    """
    def __init__(self, grade: int, section: str, main_subs: tuple[str], add_subs: dict[str, int]):
        self.grade = grade
        self.main_subs = list(main_subs)
        self.add_subs = add_subs
        self.section = section
        self.faculty: dict[str, Teacher | tuple[Teacher]] = {}
        self.schedule = list(TABLE)
        if self.grade <= 5:            # if it is lower classes
            del self.schedule[41:]     # do not work on saturday
            self.schedule[17] = "CCA"  # CCA on wed. for primary classes
        else:
            self.schedule[33] = "CCA"  # CCA on Fri. for higher classes
            if self.grade in {11, 12}:
                self.schedule[46] = "WE"
                self.schedule[47] = "WE"

    def display_schedule(self):
        """Print the schedule of the class"""
        print(f"{self.grade}{self.section} Time Table")
        display_table(self.schedule)

    def print_faculty(self):
        """Print the faculty of the class"""
        print(self.grade, self.section)
        for s in self.faculty:
            if isinstance(self.faculty[s], tuple):
                for t in self.faculty[s]:
                    print(f"{s}: {t.f_name} {t.l_name}")
            else:
                t = self.faculty[s]
                print(f"{s}: {t.f_name} {t.l_name}")

    def is_free(self, *args: str) -> bool:
        """Check if class is free for all positions in args"""
        return all(self.schedule[int(pos)].isdigit() for pos in args)

    def update(self, pos: str, sub: str):
        self.schedule[int(pos)] = sub

    def display_all_details(self):
        self.print_faculty()
        self.display_schedule()

    def reset_schedule(self):
        """Resets the schedule of the class.
        If class has been assigned to any teacher in the faculty,
        then remove the class from that teacher's schedule."""
        clss = str(self.grade) + self.section
        for t in self.faculty.values():
            if isinstance(t, tuple):  # computer sub has multiple teachers
                for k in t:
                    for ind, pos in enumerate(k.schedule):
                        if pos == clss:
                            k.schedule[ind] = str(ind)
            else:
                for ind, pos in enumerate(t.schedule):
                    if pos == clss:
                        t.schedule[ind] = str(ind)

        self.schedule = list(TABLE)
        if self.grade <= 5:
            del self.schedule[41:]
            self.schedule[17] = "CCA"
        else:
            self.schedule[33] = "CCA"

    def reset_all(self):
        self.schedule = list(TABLE)
        self.faculty = {}
        if self.grade <= 5:            # if it is lower classes
            del self.schedule[41:]     # do not work on saturday
            self.schedule[17] = "CCA"  # CCA on Wed. for primary classes
        else:
            self.schedule[33] = "CCA"  # CCA on Fri. for higher classes
            if self.grade in {11, 12}:
                self.schedule[46] = "WE"
                self.schedule[47] = "WE"
