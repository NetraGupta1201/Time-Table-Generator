from package.objects import Grade


def class_11_12_details(grade: '11 | 12', section: str) -> Grade:
    """
    Function storing details of classes 11th and 12th.
    Returns Grade object with necessary details
    """

    if section == "A":
        return Grade(
                    grade,
                    "A",
                    ("Chemistry", "Physics", "Maths", "English", "Computers"),
                    {"Pt": 2, "Practicals": 4, "Library": 1},
                )
    elif section == "B":
        return Grade(
                    grade,
                    "B",
                    ("Chemistry", "Physics", "Maths", "English", "Biology"),
                    {"Pt": 2, "Practicals": 6, "Library": 1},
                )
    elif section == "C":
        return Grade(
                    grade,
                    "C",
                    ("Accounts", "Business", "Maths", "English", "Economics"),
                    {"Pt": 2, "Library": 1},
                )
    elif section == "D":
        return Grade(
                    grade,
                    "D",
                    ("Accounts", "Business", "Entre", "English", "Economics"),
                    {"Pt": 2, "Library": 1},
                )


def class_9_10_details(grade: '9 | 10', section: str) -> Grade:
    """
    Function storing details of classes 9th and 10th
    returns Grade object with necessary details
    """
    return Grade(grade,
                 section,
                 ("Science", "Maths", "English", "Language", "Sst"),
                 {
                  "Pt": 2,
                  "Craft": 2,
                  "Computers": 2,
                  "Practicals": 2,
                  "Yoga": 1,
                  "Morals": 1,
                  "Drawing": 1,
                  "Music": 1,
                  "Library": 1,
                 })


def class_6_7_8_details(grade: '6 | 7 | 8', section: str) -> Grade:
    """
    Function storing details of classes 6th, 7th, and 8th
    returns Grade object with necessary details
    """
    return Grade(grade,
                 section,
                 ("Science", "Maths", "English", "Sst"),
                 {
                  "Hindi": 5,
                  "Tamil": 5,
                  "Pt": 2,
                  "Craft": 2,
                  "Computers": 2,
                  "Yoga": 1,
                  "Morals": 1,
                  "Drawing": 1,
                  "Music": 1,
                  "Library": 1,
                 })


def class_4_5_details(grade: '4 | 5', section: str) -> Grade:
    """
    Function storing details of classes 4th and 5th
    returns Grade object with necessary details
    """
    return Grade(grade,
                 section,
                 ("Maths", "English", "Evs"),
                 {
                  "Hindi": 3,
                  "Tamil": 3,
                  "Pt": 2,
                  "Craft": 2,
                  "Computers": 2,
                  "Yoga": 1,
                  "Morals": 1,
                  "Drawing": 1,
                  "Music": 1,
                 })
