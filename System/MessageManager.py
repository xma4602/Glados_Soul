def show(info=()):
    if type(info) is dict:
        showDict(info)
    elif type(info) in [list, tuple, set]:
        for item in info:
            if type(item) in [list, tuple, set]:
                showList(item)
            else:
                show(item)
    else:
        print(info)


def showDict(info):
    for k, v in info.items():
        print(f'{k}: {v}')


def showList(info):
    # элементы списка засовывает в строку
    print(" ".join([str(x) for x in list(info)]))
