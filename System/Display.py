def show(info=[]):
    for item in info:
        if type(item) is str:
            showString(item)
        elif type(item) is dict:
            showDict(info)


def showString(info):
    print(info)


def showDict(info):
    for k, v in info.items():
        print(f'{k}: {v}')
