import enum
import subprocess

_branches = {
    1: "system_test",
    2: "mechanics_test",
    3: "recognition_test",

    4: "system_dev",
    5: "mechanics_dev",
    6: "recognition_dev",

    7: "system",
    8: "mechanics",
    9: "recognition",
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
    if params[0] not in _branches.values():
        return "Нет такой ветки"

    branch = params[0]
    subprocess.run("git stash", shell=True)
    subprocess.run(f"git checkout {branch}", shell=True)
    p = subprocess.run(f"git pull --ff-only origin {branch}", shell=True)

    return p.returncode