import httpx
from colorama import Fore, Back, Style
import _thread
import time
import urllib.parse
import json
import pyperclip

web = "http://175.155.65.14:10376/luogu/"


def loading(lock):
    chars = ["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"]
    i = 0
    print("")
    while lock[0]:
        i = (i + 1) % len(chars)
        print("\033[A%s %s" % (chars[i], lock[1] or "" if len(lock) >= 2 else ""))
        time.sleep(0.25)


Y = Fore.YELLOW
B = Fore.BLUE
R = Fore.RED
G = Fore.GREEN
RST = Fore.RESET

lock = [False, ""]


# Accept = 1
# Wrong_Answer = 2
# Time_Limit_Exceed = 3
# Memory_Limit_Exceed = 4
# Runtime_Error = 5
# Special_Error = 6
# Compile_Error = 7

colorList = [None, G, R, Fore.BLACK, Fore.BLACK, Fore.MAGENTA, Fore.WHITE, Y]

statusList = [
    None,
    "Accept",
    "Wrong Answer",
    "Time Limit Exceed",
    "Memory Limit Exceed",
    "Runtime Error",
    "Special Error",
    "Compile Error",
]


def scoreColor(task):
    scoreC = G
    if task["score"] == 0:
        scoreC = R
    elif task["status"] != 1:
        scoreC = Y
    return scoreC


def visualize(json):
    # print(json)
    if json["status"] == 7:
        print(f"{Y}compile error: {RST}\n{json['extraInfo']}")
        return
    totalscoreC = scoreColor(json)
    print(
        f"{colorList[json['status']]}{statusList[json['status']]}{RST} {totalscoreC}{str(json['score'])}pts{RST}"
        + f" {str(json['time'])}ms, {str(json['memory'])}KB"
    )
    subtasks = json["subtasks"]
    for task in subtasks:
        subscoreC = scoreColor(task)
        print(
            f"Subtask {Fore.CYAN}#{task['subtaskId']}{RST}: {subscoreC}{str(task['score'])}pts{RST}"
        )
        num = 0
        for case in task["testcases"]:
            num += 1
            scoreC = scoreColor(case)
            if case["status"] == 3:
                case["extraInfo"] = "memory limit exceed"
            if case["status"] == 4:
                case["extraInfo"] = "time limit exceed"
            if case["status"] == 5:
                case["extraInfo"] = "runtime error"
            if case["status"] == 6:
                case["extraInfo"] = "special error"
            print(
                f"\tCase {Fore.CYAN}#{str(num)}{RST}: {scoreC}{str(case['score'])}pts{RST}, "
                + f"{str(case['memory'])}KB, {str(case['time'])}ms, "
                + f"{colorList[case['status']]}{case['extraInfo']}{RST}"
            )


def submitCode(code, Lang, problemId):
    try:
        res = httpx.post(
            web + "submit",
            data={"language": Lang, "problemId": problemId, "code": code},
        )
        return res.text
    except Exception as e:
        print(e)


def getRecord(recordId, submitter):
    try:
        res = httpx.get(
            web + "record", params={"rid": recordId, "submitter": submitter}
        )
        return res.text
    except Exception as e:
        print(e)


def submit(Command):
    Lang = 28
    codePath = Command[1].replace("'", "").replace("&", "").lstrip()
    codeFile = open(codePath, encoding="utf-8")
    rawCode = codeFile.read()
    codeFile.close()
    rawCode = urllib.parse.quote(rawCode)
    problemId = Command[2]
    res = submitCode(rawCode, Lang, problemId)
    return json.loads(res)


def record(rawCommand):
    pyperclip.copy(f'{rawCommand["submitter"]} {rawCommand["rid"]}')
    submitter = rawCommand["submitter"]
    recordId = rawCommand["rid"]
    recordRes = getRecord(recordId, submitter)
    # print(recordRes)
    return json.loads(recordRes)


def Submit(rawCommand):
    if len(rawCommand) != 3:
        print(f"{Y}C:{RST}{R}命令应输入三个参数{RST}")
        return "None"
    Res = submit(rawCommand)
    if Res == None:
        return "OK"
    print(
        f"{Y}C:{RST}代码已提交！\n提交记录ID为:{Fore.MAGENTA}{str(Res['rid'])}{Fore.RESET}, 提交账号ID为:{Fore.MAGENTA}{str(Res['submitter'])}{Fore.RESET}"
    )
    lock[0] = True
    try:
        _thread.start_new_thread(loading, (lock,))
    except Exception as e:
        print(e)
    lock[1] = "Judging..."
    recordRes = record(Res)
    lock[0] = False
    # print(recordRes)
    visualize(recordRes)


def Record(rawCommand):
    if len(rawCommand) != 3:
        print(f"{Y}C:{RST}{R}命令应输入三个参数{RST}")
        return None
    recordCommand = {"rid": rawCommand[2], "submitter": rawCommand[1]}
    Res = record(recordCommand)
    # if Res[]
    visualize(Res)
