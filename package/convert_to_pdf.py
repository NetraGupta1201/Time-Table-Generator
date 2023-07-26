import os
from package.files.connection import open_file
try:
    from fpdf import FPDF
except ModuleNotFoundError:
    # if user does not have the module installed
    # run the required command and install it
    print("You do not have the fpdf module installed.")
    print("This module is required to provide output in pdf format.")
    input("Hit enter to start installation")
    while True:
        try:
            os.system("py -m pip install fpdf")  # run command on command line
            from fpdf import FPDF
            print("Module successfully installed.")
            input("Press enter to continue")
            break
        except ModuleNotFoundError:
            print("ERROR!!!")
            print("Some Error has occurred.")
            print("Are you connected to the internet?")
            print("Please check your internet connection.")
            input("Hit enter to try again")
 

def create_pdf(filename, mode="P", font="Courier", siz=8.5, f=__file__):
    """Convert a text file into pdf format"""
    loc = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(f)))
    OUTPUT_PATH = os.path.join(loc, f"{filename}.pdf")
    pdf = FPDF()
    pdf.add_page(mode)  # add a page

    # set style and size of font for pdf
    pdf.set_font(font, size=siz)
    
    f = open_file(f"{filename}.txt", "r", fil=f)
    text = f.readlines()

    count = 0  # counter to check how many schedules are written on one page 
    for i, line in enumerate(text, start=1):
        if line.startswith("SUBSTITUTION FOR TEACHER"):  # given string denotes a new schedule
            if count == 0:  # for the first schedule, take a fresh page
                pdf.add_page(mode)  # count will never become 0 again
            count += 1  # increase counter for every schedule written
        if count > 4:  # do not write more than 4 schedules on one page
            pdf.add_page(mode)  # add a new page and write the next one
            count = 1  # reset the counter

        # create a cell
        pdf.cell(2000, 2.5, txt = line, ln = i, align = 'L')

    pdf.output(OUTPUT_PATH)  # save the pdf
