def display_table(t: "list[str]", scale: int = 1):
    """Print a table neatly; scale parameter controls size of table printed"""
    count = 0
    print("-"*(105*(scale) - (scale-1)*25))
    print("|", end="")
    for piece in t[1:]:
        if count == 8:
            count = 0
            print()
            print("-"*(105*(scale) - (scale-1)*25))
            print("|", end="")

        size = 10*scale
        if piece.isdigit():
            # ^10 parameter: ^ means center align, 10 ensures equal spacing
            empty = ""
            print(f" {empty:^{size}} ", end="|")
        else:
            print(f" {piece:^{size}} ", end="|")
        count += 1
    print("\n"+"-"*(92*scale - (scale-1)*22))


def home_screen() -> int:
    """Display home screen and menu and input what user wants to do"""
    print("Welcome to the Time Table Generator!")
    print("""
        1. Edit teacher details
        2. Generate time table
        3. Exit
        """)
    ch = input("Please enter your choice: ")
    valid = [str(i) for i in range(1, 4)]
    while True:
        if ch not in valid:
            print("Invalid input!")
            ch = input("Please enter your choice: ")
        else:
            ch = int(ch)
            break

    return ch


def display_teachers(data: set) -> None:
    """Displays all the information of teachers in list data"""
    lst = ["S.No.", "Name", "Subject", "Grades", "Min classes", "Max classes"]
    print(f"\n{lst[0]:>4} {lst[1]:<25} {lst[2]:<12} {lst[3]:<20} {lst[4]:^12} {lst[5]:^12}")
    for t in data:
        full_name = t.f_name + " " + t.l_name
        grades = " ".join(str(g) for g in t.grades)
        print(f"{t.i_d:>4}. {full_name:<25} {t.subject:<12} {grades:<20} {t.min_c:^12} {t.max_c:^12}")


def substitution_instruction():
    """Print instructions on output to inform user about substitutions"""
    print("""
    INSTRUCTIONS FOR SUBSTITUTION TEACHERS
    IF A TEACHER IS TO BE ABSENT,
    then the table shows the IDs of all available teachers.

    For example, if it shows
    7A: 23, 25, 21
    it means you can select any one of these free teachers,
    and assign them to class 7A at that particular period.

    The teachers are ORDERED from HIGHEST PRIORITY to LOWEST PRIORITY
    PRIORITY is given to teachers who already teach the class
    This ensures that teaching can continue even during substitutions
    """)
 

def restart_disclaimer():
    """Disclaimer for user if code hits restart at particular points"""
    print("""
    this code can sometimes raise such errors.
    if some person is able to assign classes to the department manually,
    then it is recommended that the maximum classes of
    the teachers in that department be increased
    """.upper())


def out_of_slots():
    """Print error to user if there are discrepencies in code for classes"""
    print("Error! Class has run out of free slots.")
    print("Too many subjects are being assigned.")
    print("Contact necessary faculty to edit the code and resolve the issue.")
    input("Press enter to exit: ")
    exit()


def time_table_instruction():
    """Print instruction for user on layout of time table"""
    print("INSTRUCTIONS")
    print("All time tables have 7 rows and 8 columns.")
    print("The first row is for Monday, second row for Tuesday and so on till Saturday.")
    print("The first column is for the first period, second for second period and so on till eighth period.")
    print()
