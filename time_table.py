"""Main script time_table.py"""
from __future__ import annotations
import sys
import os
import random
import csv
from itertools import permutations

from package.inputs import input_file_name
from package.files.connection import open_file
from package.objects import Teacher, Grade, TABLE
import package.display as dp
import package.commerce as com
import package.science as sci
import package.teacher as tc
import package.general as gn
import package.convert_to_pdf as pdf
import package.class_details as cdt


# all global variables
all_teachers: list[Teacher] = []
all_classes: dict[str, Grade] = {}
physics_lab = list(TABLE)
chemistry_lab = list(TABLE)
biology_lab = list(TABLE)
comp_lab_sen = list(TABLE)
comp_lab_jun = list(TABLE)

# store teachers with extra specialisations
physics_teachers = []
chemistry_teachers = []
biology_teachers = []
entre_teachers = []
business_teachers = []
accounts_teachers = []


class LackOfTeachersError(Exception):
    """Error raised when code identifies shortage of teachers"""


class RestartRequiredError(Exception):
    """Error raised when code is required to restart"""


class GoToMainMenuError(Exception):
    """Error raised when user needs to return to main menu"""


def reset_globals():
    """Reset all global variables. Call when restarting main()."""
    global physics_lab, chemistry_lab, biology_lab, comp_lab_jun, comp_lab_sen
    physics_lab = list(TABLE)
    chemistry_lab = list(TABLE)
    biology_lab = list(TABLE)
    comp_lab_sen = list(TABLE)
    comp_lab_jun = list(TABLE)
    for teacher in all_teachers:
        teacher.reset_all()
    for clss in all_classes.values():
        clss.reset_all()


def delete_globals():
    """Delete all data stored in global variables but not variable itself"""
    global all_classes, all_teachers
    reset_globals()
    # del lst[:] deletes all data from list without deleting variable name
    del biology_teachers[:]
    del chemistry_teachers[:]
    del physics_teachers[:]
    del business_teachers[:]
    del entre_teachers[:]
    del accounts_teachers[:]
    all_classes = {}
    all_teachers = []


def change_teacher_data():
    """Update, Remove, or Add teachers to teacher.csv file"""
    print("A: Add a teacher\nR: Remove a teacher\nU: Update a teacher info")
    ch = input("Enter your choice: ").capitalize()
    while ch not in ("A", "R", "U"):  # Validate the input
        print("Invalid Input")
        ch = input("Enter: ").capitalize()

    if ch == "R":
        try:
            tc.remove()
        except ValueError:  # ValueError if user doesn't want to remove teacher
            pass
    elif ch == "A":
        tc.add()
    elif ch == "U":
        tc.update()


def classify_science():
    """Classify science teachers into 3 streams"""
    # take only science teachers of higher classes
    sci_teachers = [t for t in all_teachers
                    if t.subject == "Science"
                    and set(t.grades).issubset({9, 10, 11, 12})
                    ]
    flag = sci.verify(sci_teachers)
    p, c, b = sci.read(sci_teachers) if flag else sci.write(sci_teachers)
    physics_teachers.extend(p)
    chemistry_teachers.extend(c)
    biology_teachers.extend(b)


def classify_commerce():
    """Classify commerce teachers into 3 streams"""
    com_teachers = [t for t in all_teachers if t.subject == "Commerce"]
    flag = com.verify(com_teachers)
    a, b, e = com.read(com_teachers) if flag else com.write(com_teachers)
    accounts_teachers.extend(a)
    business_teachers.extend(b)
    entre_teachers.extend(e)


def all_labs_free(pos) -> bool:
    """Check if all three science labs are free for two given positions"""
    return (
        physics_lab[int(pos)].isdigit()
        and chemistry_lab[int(pos)].isdigit()
        and biology_lab[int(pos)].isdigit()
    )


def is_teachers_filled(sub: str, clss_grade: int) -> bool:
    """Check if teachers are filled and cannot be assigned any classes"""
    count = sum(
        teacher.max_c / len(teacher.grades)
        for teacher in all_teachers
        if clss_grade in teacher.grades and teacher.subject == sub
    )
    return count < 4


def min_max(teachers: list[Teacher], clss: Grade) -> Teacher:
    """Select a teacher from sample teachers
    satisfies minimum classes first, then satisfies max. classes"""
    random.shuffle(teachers)

    # check minimum classes first
    for t in teachers:
        if t.min_c == len(t.assigned_classes):
            continue
        if (
            t.min_c > len(t.assigned_classes)
            # distribute teachers across their classes evenly
            and ("".join(t.assigned_classes)).count(str(clss.grade)) < int(t.min_c/len(t.grades))
        ):
            return t

    # check maximum classes
    for t in teachers:
        if len(t.assigned_classes) < t.max_c:
            return t

    # if both min and max fail, check if teachers are filled
    if is_teachers_filled(t.subject, clss.grade):
        print(f"ERROR! Maximum Classes for {t.subject} department exceeded!")
        print("Please update existing details or enter new teacher.")
        dp.restart_disclaimer()
        input("Press enter to continue")
        raise LackOfTeachersError
    else:
        raise RestartRequiredError


def check_class_faculty(clss: Grade):
    """Check if a given class has been assigned all required teachers"""

    # check the main subjects
    for sub in clss.main_subs:
        if sub == "Language":
            continue  # language is assigned and checked separately
        try:
            clss.faculty[sub]
        except KeyError:
            print(f"ERROR!! Lack of Teachers For {sub} For Class {clss.grade}")
            print("Please Add The Required Teacher.")
            input("Press enter to continue")
            raise LackOfTeachersError

    # check the additional subjects
    for sub in clss.add_subs:
        if sub == "Practicals":
            continue  # practicals is assigned and checked separately
        try:
            clss.faculty[sub]
        except KeyError:
            print(f"ERROR!! Lack of Teachers For {sub} For Class {clss.grade}")
            print("Please Add The Required Teacher.")
            input("Press enter to continue")
            raise LackOfTeachersError


def sync_language(clss_1: Grade, clss_2: Grade):
    """Sync language classes for clss_1 and clss_2"""
    sub1, sub2, sub3 = "Sanskrit", "Hindi", "Tamil"

    if sub1 in clss_1.faculty:
        t1 = clss_1.faculty[sub1]
    else:
        # if class does not have the specified language
        # dummy teacher is created to avoid errors
        t1 = Teacher(None, None, None, None, None, None, None)
    if sub2 in clss_1.faculty:
        t2 = clss_1.faculty[sub2]
    else:
        t2 = Teacher(None, None, None, None, None, None, None)
    if sub3 in clss_1.faculty:
        t3 = clss_1.faculty[sub3]
    else:
        t3 = Teacher(None, None, None, None, None, None, None)

    for i in range(6):
        day = clss_1.schedule[8*i+1:8*i + 9]
        random.shuffle(day)
        day = [int(p) for p in day if p.isdigit()]  # ensures clss_1 is free
        if not day:
            raise RestartRequiredError
        for pos in day:
            if clss_2.is_free(pos) and gn.teachers_free(pos, t1, t2, t3):
                clss_1.update(pos, "Language")
                clss_2.update(pos, "Language")
                for t in t1, t2, t3:
                    t.update(pos, clss_1.grade, clss_1.section)
                break
        else:
            # all positions on all days are full, restart
            raise RestartRequiredError


def assign_one_teacher(clss: Grade, teachers: dict[str, list[Teacher]]) -> None:
    """From an identified list of teachers, assign any one.
    Function must be called within assign_faculty or assign_faculty_together
    only after the correct set of teachers has been identified
    """
    for subject in teachers:
        if subject not in clss.faculty:
            if subject == "Computers":  # few classes have two computer teachers
                t1 = random.choice(teachers[subject])
                if 12 in t1.grades:  # if teacher is most senior
                    clss.faculty[subject] = t1
                    t1.new_assigned_class(clss)
                    continue
                t2 = random.choice(teachers[subject])
                while t1 == t2 or 12 in t2.grades:
                    t2 = random.choice(teachers[subject])
                clss.faculty[subject] = (t1, t2)
                t1.new_assigned_class(clss)
                t2.new_assigned_class(clss)
            else:
                t = min_max(teachers[subject], clss)
                clss.faculty[subject] = t
                t.new_assigned_class(clss)


def assign_one_lab(clss: Grade) -> None:
    """Assign lab classes to 11th and 12th"""
    # take the required teachers
    physics = clss.faculty["Physics"]
    chemistry = clss.faculty["Chemistry"]
    if clss.section == "B":
        biology = clss.faculty["Biology"]
    days = [0, 1, 2, 3, 4]
    random.shuffle(days)
    # k values -> 0 & 1: assign phy and chem, 2: assign bio
    for k in range(3):
        classes_assigned = False  # check if classes for one k value are assigned
        for i in days:
            day = clss.schedule[8*i+1: 8*i+9]
            for j in range(len(day) - 1):
                pos1 = day[j]
                pos2 = day[j + 1]
                if pos1.isdigit() and pos2.isdigit():
                    if k in {0, 1}:
                        # assign phy and chem labs at same time
                        if (physics_lab[int(pos1)].isdigit()
                           and physics_lab[int(pos2)].isdigit()
                           and physics.is_free(pos1, pos2)
                           and chemistry_lab[int(pos1)].isdigit()
                           and chemistry_lab[int(pos2)].isdigit()
                           and chemistry.is_free(pos1, pos2)):
                            for pos in pos1, pos2:
                                clss.update(pos, "P/C Lab")
                                physics.update(pos, clss.grade, clss.section)
                                physics_lab[int(pos)] = str(clss.grade) + clss.section
                                chemistry.update(pos, clss.grade, clss.section)
                                chemistry_lab[int(pos)] = str(clss.grade) + clss.section
                            classes_assigned = True
                            break
                    elif k == 2 and clss.section == "A":
                        classes_assigned = True
                        break
                    elif k == 2 and clss.section == "B":
                        if (
                            biology_lab[int(pos1)].isdigit()
                            and biology_lab[int(pos2)].isdigit()
                            and biology.is_free(pos1, pos2)
                        ):
                            for pos in pos1, pos2:
                                clss.update(pos, "Bio Lab")
                                biology.update(int(pos), clss.grade, clss.section)
                                biology_lab[int(pos)] = str(clss.grade) + clss.section
                            classes_assigned = True
                            break
            if classes_assigned:
                days.remove(i)
                break
        else:
            classes_assigned = False
            break
    if not classes_assigned:
        raise RestartRequiredError


def assign_faculty(clss: Grade) -> None:
    """Assigns faculty for main subjects and additional subjects for a class"""
    # Assign faculty for main subjects
    allowed_teachers = {}  # Dictionary of all possible main subject teachers
    for teacher in all_teachers:
        # first, for 11th and 12th, assign teachers of special subjects
        # science and commerce teachers are assigned
        if clss.grade in (11, 12):
            if clss.section in ["A", "B"]:
                allowed_teachers["Physics"] = [t for t in physics_teachers
                                               if clss.grade in t.grades]
                allowed_teachers["Chemistry"] = [t for t in chemistry_teachers
                                                 if clss.grade in t.grades]
                if clss.section == "B":
                    allowed_teachers["Biology"] = [t for t in biology_teachers
                                                   if clss.grade in t.grades]

            elif clss.section in ("C", "D"):
                # unlike science groups, here no need to check for t.grades
                # since commerce is available only for 11th and 12th
                allowed_teachers["Accounts"] = accounts_teachers
                allowed_teachers["Business"] = business_teachers
                if clss.section == "D":
                    allowed_teachers["Entre"] = entre_teachers

        if teacher.subject in clss.main_subs and clss.grade in teacher.grades:
            allowed_teachers.setdefault(teacher.subject, [])
            allowed_teachers[teacher.subject].append(teacher)

    assign_one_teacher(clss, allowed_teachers)

    # Assign faculty for additional subjects
    allowed_add_teachers = {}  # Dict of possible additional subject teachers
    for teacher in all_teachers:
        if teacher.subject in clss.add_subs and clss.grade in teacher.grades:
            allowed_add_teachers.setdefault(teacher.subject, [])
            allowed_add_teachers[teacher.subject].append(teacher)

    assign_one_teacher(clss, allowed_add_teachers)
    check_class_faculty(clss)


def assign_language_together(clss_1: Grade, clss_2: Grade) -> None:
    """Assign language classes commonly to clss_1, clss_2"""
    allowed_teachers = {}  # Dict of all possible lang teachers
    for teacher in all_teachers:
        if (teacher.subject in ("Hindi", "Tamil", "Sanskrit")
           and clss_1.grade in teacher.grades):
            allowed_teachers.setdefault("Language", [])
            allowed_teachers["Language"].append(teacher)

    # identify and separate all language teachers
    for teachers in allowed_teachers.values():
        sanskrit, tamil, hindi = [], [], []
        for t in teachers:
            if t.subject == "Hindi":
                hindi.append(t)
            elif t.subject == "Sanskrit":
                sanskrit.append(t)
            elif t.subject == "Tamil":
                tamil.append(t)

        if clss_1.section not in "CD":  # sanskrit is available only for A and B sections
            if not sanskrit:
                print(f"ERROR!! Lack of Teachers For Sanskrit For Class {clss_1.grade}")
                print("Please Add The Required Teacher.")
                input("Press enter to continue")
                raise LackOfTeachersError

            t1 = random.choice(sanskrit)
            clss_1.faculty["Sanskrit"] = t1
            clss_2.faculty["Sanskrit"] = t1
            t1.new_assigned_class(clss_1)
            t1.new_assigned_class(clss_2)

        if not tamil:
            print(f"ERROR!! Lack of Teachers For Tamil For Class {clss_1.grade}")
            print("Please Add The Required Teacher.")
            input("Press enter to continue")
            raise LackOfTeachersError

        t2 = random.choice(tamil)
        clss_1.faculty["Tamil"] = t2
        clss_2.faculty["Tamil"] = t2
        t2.new_assigned_class(clss_1)
        t2.new_assigned_class(clss_2)

        if not hindi:
            print(f"ERROR!! Lack of Teachers For Hindi For Class {clss_1.grade}")
            print("Please Add The Required Teacher.")
            input("Press enter to continue")
            raise LackOfTeachersError

        t3 = random.choice(hindi)
        clss_1.faculty["Hindi"] = t3
        clss_2.faculty["Hindi"] = t3
        t3.new_assigned_class(clss_1)
        t3.new_assigned_class(clss_2)


def assign_faculty_together(clss_1: Grade, clss_2: Grade) -> None:
    """Assign certain faculty common for two classes"""
    allowed_teachers = {}  # Dict of all possible main subject teachers
    # assign language first
    assign_language_together(clss_1, clss_2)
    for clss in clss_1, clss_2:
        allowed_teachers = {}
        for t in all_teachers:
            if (
                # language teachers have been assigned separately
                t.subject not in ("Hindi", "Tamil", "Sanskrit")
                and t.subject in clss.main_subs
                and clss.grade in t.grades
            ):
                allowed_teachers.setdefault(t.subject, [])
                allowed_teachers[t.subject].append(t)
        assign_one_teacher(clss, allowed_teachers)
    allowed_add_teachers = {}  # Dictionary of all possible add. sub. teachers
    for t in all_teachers:
        if (
            t.subject in clss_1.add_subs
            and clss_1.grade in t.grades
        ):
            allowed_add_teachers.setdefault(t.subject, [])
            allowed_add_teachers[t.subject].append(t)

    assign_one_teacher(clss_1, allowed_add_teachers)
    assign_one_teacher(clss_2, allowed_add_teachers)
    check_class_faculty(clss_1)
    check_class_faculty(clss_2)


def schedule_full_week(clss: Grade, subs: list[str]) -> None:
    """Schedule one class of each subject in list subs on each day for entire week"""
    DAYS = 5 if clss.grade in (1, 2, 3, 4, 5) else 6
    for i in range(DAYS):
        day = clss.schedule[8*i + 1: 8*i + 9]
        day = [p for p in day if p.isdigit()]  # take only free positions
        possible_slots = list(permutations(day, len(subs)))  # take all possibilities
        random.shuffle(possible_slots)
        for slots in possible_slots:
            for j, slot in enumerate(slots):
                # check if the slot is free for teacher as well
                teacher = clss.faculty[subs[j]]
                if not gn.positions_valid((clss, teacher, slot)):
                    flag = False
                    break
            else:
                flag = True
            if flag:
                break
        else:
            raise RestartRequiredError

        # once free slot is identified, assign the classes
        for j, pos in enumerate(slots):
            sub = subs[j]
            teacher = clss.faculty[sub]
            clss.update(pos, sub)
            teacher.update(int(pos), clss.grade, clss.section)


def schedule_add_sub(clss: Grade, slots: list[str], sub: str) -> None:
    """Schedule an additional subject sub to the class clss"""
    t = clss.faculty[sub]
    freq = clss.add_subs[sub]
    slots: list[tuple[str]] = [i for i in permutations(slots, freq) if gn.all_different(i)]
    if not slots:
        dp.out_of_slots()
    random.shuffle(slots)
    for slot in slots:
        for pos in slot:
            if not (gn.teachers_free(pos, t) and clss.is_free(pos)):
                break
        else:
            for pos in slot:
                t.update(pos, clss.grade, clss.section)
                clss.update(pos, sub)
            break
    else:
        raise RestartRequiredError


def schedule_computer(clss: Grade, slots: list[str]) -> None:
    """Schedule computer labs for a particular class."""
    freq = clss.add_subs["Computers"]
    slots: list[tuple[str]] = [i for i in permutations(slots, freq) if gn.all_different(i)]
    random.shuffle(slots)

    # check if class has two computer teachers
    if isinstance(clss.faculty["Computers"], tuple):  # if class has two computer teachers
        t1, t2 = clss.faculty["Computers"]
        for slot in slots:
            for pos in slot:
                # check if teachers and lab are free
                if not (gn.teachers_free(pos, t1, t2) and comp_lab_jun[int(pos)].isdigit()):
                    break
            else:
                for pos in slot:
                    t1.update(pos, clss.grade, clss.section)
                    t2.update(pos, clss.grade, clss.section)
                    clss.update(pos, "Computers")
                    comp_lab_jun[int(pos)] = str(clss.grade) + clss.section
                break
        else:
            # if not able to assign classes, restart
            raise RestartRequiredError
    else:  # executes if class has only one computer teacher
        # a single computer teacher would be assigned the senior lab
        t = clss.faculty["Computers"]
        for slot in slots:
            for pos in slot:
                if not (gn.teachers_free(pos, t) and comp_lab_sen[int(pos)].isdigit()):
                    break
            else:
                for pos in slot:
                    t.update(pos, clss.grade, clss.section)
                    clss.update(pos, "Computers")
                    comp_lab_sen[int(pos)] = str(clss.grade) + clss.section
                break
        else:
            raise RestartRequiredError


def sync_common_subs(clss_1: Grade, clss_2: Grade, common_subs: list[str]) -> None:
    """Sync subs in common_subs for both clss_1 and clss_2"""
    while True:
        for sub in common_subs:
            if sub in clss_1.main_subs:
                if sub == "Language":
                    sync_language(clss_1, clss_2)
            elif sub in clss_1.add_subs:
                if sub == "Practicals":
                    # if sub is practicals, assign labs and teachers
                    physics = random.choice(physics_teachers)
                    chemistry = random.choice(chemistry_teachers)
                    biology = random.choice(biology_teachers)
                    classes_assigned = False
                    days_num = [0, 1, 2, 3, 4]  # only weekdays should have practicals
                    random.shuffle(days_num)
                    for i in days_num:
                        # check each weekday if class can be assigned
                        day = clss_1.schedule[8*i+1:8*i + 9]
                        for j in range(len(day) - 1):
                            pos1 = day[j]
                            pos2 = day[j+1]
                            if pos1.isdigit() and pos2.isdigit():
                                # check if second class, teachers, and labs are free
                                if (
                                    clss_2.is_free(pos1, pos2)
                                    and all_labs_free(pos1)
                                    and all_labs_free(pos2)
                                    and gn.teachers_free(pos1, physics, chemistry, biology)
                                    and gn.teachers_free(pos2, physics, chemistry, biology)
                                ):
                                    for pos in pos1, pos2:
                                        for clss in clss_1, clss_2:
                                            clss.update(pos, sub)
                                            for lab in (physics_lab, biology_lab, chemistry_lab):
                                                if (
                                                    pos == pos1 and clss == clss_1
                                                    or pos == pos2 and clss == clss_2
                                                ):
                                                    lab[int(pos)] = str(clss.grade) + clss.section
                                                    for t in (physics, chemistry, biology):
                                                        t.update(int(pos), clss.grade, clss.section)

                                    classes_assigned = True
                                    break
                        break

                    if not classes_assigned:
                        # if classes not assigned, reset the schedules and try again
                        for clss in clss_1, clss_2:
                            remove_class_from_labs(clss.grade, clss.section)
                            clss.reset_schedule()
                        break
        else:
            break


def sync_bio_entre(clss_1: Grade, clss_2: Grade) -> None:
    """syncs biology and entrepreneurship classes
    clss_1 has to be the biology class and clss_2 has to be the entrepreneurship class
    """
    while True:
        generate(clss_1)  # generate entire time table for biology class
        t2 = clss_2.faculty["Entre"]
        for i, pos in enumerate(clss_1.schedule):
            if pos in ["Bio Lab", "Biology"]:
                # for positions where clss_1 has biology,
                # try assigning entre to clss_2 at same position
                if not gn.teachers_free(i, t2):
                    remove_class_from_labs(clss_1.grade, clss_1.section)
                    clss_1.reset_schedule()
                    clss_2.reset_schedule()
                    break
                else:
                    clss_2.update(i, "Entre")
                    t2.update(i, clss_2.grade, clss_2.section)
        else:
            break
        continue


def generate(clss: Grade) -> None:
    """Generate time table for one class independently"""
    if "Practicals" in clss.add_subs and clss.grade in (11, 12):
        assign_one_lab(clss)

    if clss.grade not in (11, 12) or clss.section not in "D":
        schedule_full_week(clss, clss.main_subs)
    else:
        # 11D and 12D are scheduled using sync_bio_entre
        # so Entre subject must not be scheduled again
        schedule_full_week(clss, [s for s in clss.main_subs if s != "Entre"])
    for sub in clss.add_subs:
        slots = [p for p in clss.schedule if p.isdigit()]
        if sub == "Computers":
            schedule_computer(clss, slots)
        elif sub != "Practicals":
            if clss.add_subs[sub] >= 2:
                # if there are many multiple subs to assign
                # then do not use permutations
                # as it will take a long time
                t = clss.faculty[sub]
                count = 0
                while True:
                    pos = random.choice(slots)
                    if gn.teachers_free(pos, t):
                        clss.update(pos, sub)
                        t.update(int(pos), clss.grade, clss.section)
                        count = 0
                        slots.remove(pos)
                    freq = clss.add_subs[sub]
                    if clss.schedule.count(sub) == freq:
                        break
                    elif not slots:  # check if slots is empty
                        dp.out_of_slots()  # call the error msg

                    count += 1
                    if count == 1000:
                        raise RestartRequiredError
            else:
                # assign classes using permutation method
                schedule_add_sub(clss, slots, sub)

    # fill up remaining empty slots
    leave_free = 2 if clss.grade in (4, 5) else 0
    free_slots(clss, leave_free)


def generate_together(clss_1: Grade, clss_2: Grade, common_subs: list[str]) -> None:
    """sync certain subjects together for two classes"""
    # schedule main and additional subs for both classes
    for clss in clss_1, clss_2:
        main_subs_to_assign = [s for s in clss.main_subs if s not in common_subs]
        schedule_full_week(clss, main_subs_to_assign)
        for sub in clss.add_subs:
            all_available_slots = [p for p in clss.schedule if p.isdigit()]
            if sub in common_subs:
                pass
            elif sub == "Computers":
                schedule_computer(clss, all_available_slots)
            else:
                schedule_add_sub(clss, all_available_slots, sub)
        free_slots(clss)


def free_slots(clss: Grade, leave_free: int = 0) -> None:
    """Fill up leftover slots on time table"""
    sub_freq = {sub: 0 for sub in clss.main_subs}
    positions_free = {}
    for pos in clss.schedule:
        if pos.isdigit():
            available_teachers = []
            for s in list(clss.faculty):
                t = clss.faculty[s]
                if (
                    not isinstance(t, tuple)  # tuple in case of computer sub.
                    and s in clss.main_subs
                    and gn.teachers_free(pos, t)
                    and s != "Entre"  # Assigned separately in sync_bio_entre
                ):
                    available_teachers.append(t)
            if not available_teachers:
                # no teachers available for position pos
                raise RestartRequiredError
            random.shuffle(available_teachers)
            positions_free[pos] = available_teachers

    positions_free = gn.sort_dict(positions_free)
    positions_free = gn.remove_values(positions_free, leave_free)

    for pos in positions_free:
        if len(positions_free[pos]) == 1:
            t = positions_free[pos][0]
            sub = gn.get_key(clss, t)
            t.update(int(pos), clss.grade, clss.section)
            clss.update(pos, sub)
            sub_freq[sub] += 1
        else:
            for t in positions_free[pos]:
                sub = gn.get_key(clss, t)
                if sub_freq[sub] == min(sub_freq.values()):
                    t.update(int(pos), clss.grade, clss.section)
                    clss.update(pos, sub)
                    sub_freq[sub] += 1
                    break
            else:
                t = random.choice(positions_free[pos])
                t.update(int(pos), clss.grade, clss.section)
                clss.update(pos, sub)
                sub_freq[sub] += 1


def substitutions() -> None:
    """Assign substitution teachers in case a teacher is absent"""
    dp.substitution_instruction()  # display instruction for user
    dp.display_teachers(all_teachers)  # show all teachers with ID
    for t in all_teachers:
        assign_substitution_teachers(t)


def assign_substitution_teachers(teacher_to_be_subbed: Teacher) -> None:
    """
    Main function for ordering substitution teachers
    Teachers are first separated into primary and secondary classes
    (we cannot assign a primary teacher as substitute for secondary class)
    Teachers are ordered by a priority criteria
    Those who already teach the class are considered first

    By default only four teachers are suggested
    but this number can be increased in MAX_TO_SHOW variable
    SIZE_OF_TABLE, which controls the output table size
    may need to be adjusted according to number of teachers displayed
    table size for SIZE_OF_TABLE > 2 will not fit in pdf output
    """
    MAX_TO_SHOW = 4
    SIZE_OF_TABLE = 2
    secondary = [t for t in all_teachers if min(t.grades) > 2]
    primary = [t for t in all_teachers if t not in secondary]
    print(f"\nSUBSTITUTION FOR TEACHER {teacher_to_be_subbed.f_name} {teacher_to_be_subbed.l_name}")
    substitution_table = list(TABLE)
    for ind, pos in enumerate(teacher_to_be_subbed.schedule):
        if pos.isdigit() is False and pos:
            try:
                clss = teacher_to_be_subbed.assigned_classes[pos]
                # create lists to order teachers by priority
                priority_list = []
                first_priority = []
                second_priority = []
                class_faculty = list(clss.faculty.values())
                random.shuffle(class_faculty)
                for t in class_faculty:
                    if isinstance(t, tuple):
                        for k in t:
                            if k.is_free(ind):
                                second_priority.append(k)
                    elif t.subject in clss.main_subs:
                        # teachers who teach main subjects get highest priority
                        if t.is_free(ind):
                            first_priority.append(t)
                    elif t.is_free(ind):
                        # all other teachers receive second priority
                        second_priority.append(t)

                priority_list.extend(first_priority)
                priority_list.extend(second_priority)
                del first_priority, second_priority
                if clss.grade < 3:
                    for t in primary:
                        if (
                            t not in priority_list
                            and t.is_free(ind)
                        ):
                            priority_list.append(t)
                else:
                    for t in secondary:
                        if (
                            t not in priority_list
                            and t.is_free(ind)
                        ):
                            priority_list.append(t)
            except KeyError:
                pass  # Practicals subject gives KeyError

            else:
                details = f"{clss.grade}{clss.section}: " + ", ".join(
                    str(t.i_d) for t in priority_list[:MAX_TO_SHOW]
                )

                substitution_table[ind] = details

    dp.display_table(substitution_table, SIZE_OF_TABLE)


def load_teacher_data() -> None:
    """Load all data from teacher_info.csv into main program"""
    f = open_file("teacher_info.csv", "r")
    data = list(csv.reader(f))
    f.close()
    for row in data:
        if row:
            i_d, f_n, l_n, sub, grades, min_c, max_c = row
            i_d, min_c, max_c = int(i_d), int(min_c), int(max_c)  # convert str to int
            grades = tuple(int(g) for g in grades.split())  # convert grades from str to tuple
            all_teachers.append(Teacher(i_d, f_n, l_n, sub, grades, min_c, max_c))


def remove_class_from_labs(clss_grade: int, clss_section: str) -> None:
    """Remove a particular class from all the labs"""
    clss_value = str(clss_grade) + clss_section
    for lab in physics_lab, chemistry_lab, biology_lab:
        for index, pos in enumerate(lab):
            if pos == clss_value:
                lab[index] = str(index)


def initialize() -> None:
    """Load all data from files and create all objects"""
    load_teacher_data()
    classify_science()
    classify_commerce()
    # Making the classes with default subjects and frequency of extra subjects
    for clss in 6, 7, 8:
        for sec in "ABCD":
            all_classes[f"{clss}{sec}"] = cdt.class_6_7_8_details(clss, sec)
    for clss in 9, 10:
        for sec in "ABCD":
            all_classes[f"{clss}{sec}"] = cdt.class_9_10_details(clss, sec)
    for clss in 11, 12:
        for sec in "ABCD":
            all_classes[f"{clss}{sec}"] = cdt.class_11_12_details(clss, sec)


def main(choice: 0 | 1 | 2) -> bool:
    """The main function to be executed"""
    os.system("cls")
    if choice == 0:
        os.system("cls")
        choice = dp.home_screen()

    if choice == 1:
        change_teacher_data()
        delete_globals()
        initialize()
        raise GoToMainMenuError

    elif choice == 2:
        # assigning faculty for classes 11, 12
        for clss, obj in all_classes.items():
            if int(clss[:-1]) in (11, 12):
                assign_faculty(obj)

        # assigning faculty for classes 9, 10
        assign_faculty_together(all_classes["9A"], all_classes["9B"])
        assign_faculty_together(all_classes["9C"], all_classes["9D"])
        assign_faculty_together(all_classes["10A"], all_classes["10B"])
        assign_faculty_together(all_classes["10C"], all_classes["10D"])

        # assigning faculty for classes 6, 7, 8
        for clss, obj in all_classes.items():
            if int(clss[:-1]) in (6, 7, 8):
                assign_faculty(obj)

        # Generating Timetable for classes 6, 7, 8
        for i in (6, 7, 8):
            for sec in ("A", "B", "C", "D"):
                clss = all_classes[f"{i}{sec}"]
                generate(clss)

        # generating timetable for classes 9, 10
        sync_common_subs(all_classes["9A"], all_classes["9B"], ["Language", "Practicals"])
        sync_common_subs(all_classes["9C"], all_classes["9D"], ["Language", "Practicals"])
        sync_common_subs(all_classes["10A"], all_classes["10B"], ["Language", "Practicals"])
        sync_common_subs(all_classes["10C"], all_classes["10D"], ["Language", "Practicals"])
        generate_together(all_classes["9A"], all_classes["9B"], ["Language", "Practicals"])
        generate_together(all_classes["9C"], all_classes["9D"], ["Language", "Practicals"])
        generate_together(all_classes["10A"], all_classes["10B"], ["Language", "Practicals"])
        generate_together(all_classes["10C"], all_classes["10D"], ["Language", "Practicals"])

        # generating timetables for 11, 12 BD sections
        sync_bio_entre(all_classes["11B"], all_classes["11D"])
        sync_bio_entre(all_classes["12B"], all_classes["12D"])

        # generating timetables for 11, 12 AC sections
        for i in (11, 12):
            for sec in ("A", "C"):
                clss = all_classes[f"{i}{sec}"]
                generate(clss)

        # generating timetables for 11, 12 D section
        # this is done separately due to working of sync_bio_entre function
        for clss in "11D", "12D":
            generate(all_classes[clss])

        # input file name to write final output
        print("CAUTION!!!\nEntering a file name that already exists will result in overwriting of data in file")
        filename = input_file_name()

        stdout_origin = sys.stdout  # save terminal stdout in stdout_origin
        sys.stdout = open_file(f"{filename}.txt", "w", fil=__file__)
        # Displaying the time table for classes
        dp.time_table_instruction()
        for clss in all_classes.values():
            clss.print_faculty()
            clss.display_schedule()
            print()

        # Displaying timetable for labs
        print("Physics Lab")
        dp.display_table(physics_lab)
        print("Chemistry Lab")
        dp.display_table(chemistry_lab)
        print("Biology Lab")
        dp.display_table(biology_lab)
        print("Computer Lab Junior")
        dp.display_table(comp_lab_jun)
        print("Computer Lab Senior")
        dp.display_table(comp_lab_sen)
        for teacher in all_teachers:
            print()
            teacher.print_schedule()
        sys.stdout.close()

        sys.stdout = open_file(f"{filename}_substitutions.txt", "w", fil=__file__)
        substitutions()
        sys.stdout.close()
        sys.stdout = stdout_origin

        # create pdf format using text files created
        pdf.create_pdf(filename, f=__file__)
        pdf.create_pdf(f"{filename}_substitutions", "L", siz=7, f=__file__)

        print('Time table successfully generated and saved.')
        print(f"Files saved in txt and pdf formats to location {os.path.dirname(__file__)}")
        input("Press enter to exit")
        return True
    elif choice == 3:
        return True


if __name__ == "__main__":
    mode = 0
    initialize()
    while True:
        try:
            flag = main(mode)
            if flag:
                break
        except GoToMainMenuError:
            mode = 0
        except LackOfTeachersError:
            mode = 1
        except RestartRequiredError:
            mode = 2

        print("Loading...")
        reset_globals()
