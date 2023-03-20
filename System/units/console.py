""" Файл, отвечающий за вывод на консоль """

def send(obj):
    pass

def show(info=()):
    #рекурсивная функция, выводящая все типы, кроме словаря и списочных типов
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
    #Вывод словаря
    for k, v in info.items():
        print(f'{k}: {v}')


def showList(info):
    # Вывод list, tuple или set
    print(" ".join([str(x) for x in list(info)]))
