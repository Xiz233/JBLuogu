import os
import _thread
import time

from colorama import Fore, Style

import backend

HELP_TEXT = f"""JBLuogu指令Help:  账号登录
submit {Fore.BLUE}[codePath] [problemID]{Fore.RESET} \t代码提交
submit {Fore.BLUE}[submitterID] [problemID]{Fore.RESET} \t查看记录
help \t\t\t\t命令帮助
"""


def readCommand():
    RawCommand = input(Fore.YELLOW + "JBLuogu >> " + Fore.RESET).lstrip().rstrip()
    Command = RawCommand.split(" ")
    if Command[0] == "submit":
        backend.Submit(Command)
    elif Command[0] == "record":
        backend.Record(Command)
    elif (Command[0] == "exit"):
        return "FK"
    elif Command[0] == "help":
        print(HELP_TEXT)
        return "OK"
    else:
        print(f"{Fore.YELLOW}C:{Fore.RED}无效的命令{Fore.RESET}")
        return "OK"


def statusProcess(statusID):
    if statusID == "OK":
        return
