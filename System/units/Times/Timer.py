from datetime import datetime
from System.units.Times.TimeEvent import TimeEvent

# 12:23:45
time = input("Введите время в формате чч:мм:сс : ")
uncorrect = "Некорректные данные!!!"


class Timer(TimeEvent):



    def check_Time(time):

        if len(time) == 0 or time[2] != ":" or time[5] != ":" or len(time) != 8:
            raise BaseException()

        arr = time.split(':')

        for i in range(len(arr)):

            if len(arr[i]) != 2 or not (arr[i].isdigit()):
                raise BaseException()

        if int(arr[0]) < 0 or int(arr[0]) >= 24:
            raise BaseException()

        if int(arr[1]) < 0 or int(arr[1]) >= 60:
            raise BaseException()

        if int(arr[2]) < 0 or int(arr[2]) >= 60:
            raise BaseException()


try:

    Timer.check_Time(time)
    system_time = datetime.now()



except BaseException:
    print(uncorrect)
