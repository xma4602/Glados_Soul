import gspread

opened = False


def open_room():
    global opened
    opened = True


def close_room():
    global opened
    opened = False


def is_opened():
    if opened:
        return True
    else:

