def show(info=[]):
    if type(info) is dict:
            showDict(info)
    elif type(info) in [list, tuple, set]:
        for item in info:
            show(item)
    else:
        print(info)

def showDict(info):
    for k, v in info.items():
        print(f'{k}: {v}')

