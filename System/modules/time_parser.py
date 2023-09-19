import re
from datetime import timedelta, datetime


def parse_time(time: str):
    t = re.search(r'(\d+)\s*сек\.*', time)
    if t is not None:
        match = t[0]
        delta = timedelta(seconds=float(t.group(1)))
    else:
        t = re.search(r'(\d+)\s*мин[а-я]*\s*', time)
        if t is not None:
            match = t[0]
            delta = timedelta(minutes=float(t.group(1)))
        else:
            t = re.search(r'(\d+)\s*час[а-я]*\s*', time)
            if t is not None:
                match = t[0]
                delta = timedelta(hours=float(t.group(1)))
            else:
                t = re.search(r'(\d+)\s*дн[а-я]*\s*', time)
                if t is not None:
                    match = t[0]
                    delta = timedelta(days=float(t.group(1)))
                else:
                    t = re.search(r'(\d+)[ :;.,]*(\d+)?', time)
                    if t is not None:
                        match = t[0]
                        h = float(t.group(1))
                        m = t.group(2)
                        m = 0 if m is None else float(m)
                        delta = timedelta(hours=h, minutes=m)
                    else:
                        raise ValueError("Неверный формат времени")
    return time.replace(match, ''), delta


def parse_date(time):
    t = re.search(r'сегодня\s*', time)
    date = datetime.now()
    if t is not None:
        match = t[0]
    else:
        t = re.search(r'завтра\s*', time)
        if t is not None:
            match = t[0]
            date = date.replace(day=date.day + 1)
        else:
            t = re.search(r'послезавтра\s*', time)
            if t is not None:
                match = t[0]
                date = date.replace(day=date.day + 2)
            else:
                t = re.search(r'(\d{1,2})[ -_/\\.,:;](\d{1,2})([ -_/\\.,:;](\d{2,4}))?', time)
                if t is not None:
                    match = t[0]
                    d = int(t.group(1))
                    m = int(t.group(2))
                    y = t.group(4)
                    y = datetime.now().year if y is None else int(y)
                    date = date.replace(day=d, month=m, year=y)
                else:
                    raise ValueError("Неверный формат времени")
    return time.replace(match, ''), date
