"""Functions that do various tasks used inside of main script"""

TABLE = [""] + [str(i) for i in range(1, 48)]


def positions_valid(*args: str):
    """Check if given slot is free for both teacher and classroom"""
    return not any(
        not c.is_free(pos)
        or not t.schedule[int(pos)].isdigit()
        for c, t, pos in args
    )


def teachers_free(pos: str, *args):
    """Check if teacher(s) is(are) free for a given position"""
    return all(t.schedule[int(pos)].isdigit() for t in args)


def sort_dict(d: dict) -> dict:
    """Sort dictionary by values"""
    keys = list(d.keys())
    values = list(d.values())
    number = [len(t) for t in d.values()]                        # count number of teachers per slot
    for i in range(len(number)):                                 # initialize bubble sort
        for j in range(len(number) - i - 1):
            if number[j] > number[j+1]:                          # if more teachers, push slot to end of list
                keys[j], keys[j+1] = keys[j+1], keys[j]          # swap keys
                values[j], values[j+1] = values[j+1], values[j]  # swap values

    d = dict(zip(keys, values))
    return d


def get_key(clss, t):
    """Access a key from dictionary using value"""
    key_list = list(clss.faculty.keys())
    val_list = list(clss.faculty.values())
    return key_list[val_list.index(t)]


def all_different(slot):
    """Check if all positions in slot are on different days"""
    slot = set(slot)
    for i in range(6):
        day = set(TABLE[8*i+1: 8*i+9])
        if len(slot.intersection(day)) > 1:
            return False
    return True


def remove_values(d: dict, n: int) -> dict:
    """Removes the first n values from the dictionary d"""
    return dict(tuple(d.items())[n:])
