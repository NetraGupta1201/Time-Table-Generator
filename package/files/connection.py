"""Open a file containing data"""
import os


def open_file(name, m, new="", fil=__file__):
    """Open a file in folder 'files' from any directory on command line.
    File name and mode to open file are parameters.
    fil parameter can be passed in if file to open is in some other directory.
    Returns file object."""

    loc = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(fil)))
    file_path = os.path.join(loc, name)
    return open(file_path, m, encoding="utf-8", newline=new)
