import enum
import subprocess

_branches = {
    "s_t": "system_test",
    "m_t": "mechanics_test",
    "r_t": "recognition_test",

    "s_d": "system_dev",
    "m_d": "mechanics_dev",
    "r_d": "recognition_dev",

    "s_": "system",
    "m_": "mechanics",
    "r_": "recognition",
}


class Branches(enum.Enum):
    MECHANICS = "mechanics_test"
    RECOGNITION = "recognition_test"
    SYSTEM = "system_test"


def help():
    return ['update [branch]', 'where [branch] is:', _branches]

def update(params):
    if len(params) == 0:
        return ["Укажите какую ветку обновить", _branches]
    elif params[0] in _branches.values():
        branch = params[0]
    elif params[0] in _branches.keys():
        branch = _branches.get(params[0])
    else:
        return "Нет такой ветки"

    subprocess.run("git stash", shell=True)
    subprocess.run(f"git checkout {branch}", shell=True)
    p = subprocess.run(f"git pull --ff-only origin {branch}", shell=True)

    if p.returncode < 0:
        return "Ошибка обновления"
    else:
        return "Обновление прошло успешно"