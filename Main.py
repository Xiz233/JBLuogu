import colorama
import os
import time

import command


def main():
    # 特判愚人节
    Time = time.localtime()
    if Time.tm_mon == 4 and Time.tm_mday == 1:
        print(f"Wel{colorama.Style.BRIGHT}cum{colorama.Style.NORMAL} to {colorama.Fore.YELLOW}JBLuogu{colorama.Fore.RESET}!")
    else:
        print(f"Welcome to {colorama.Fore.YELLOW}JBLuogu{colorama.Fore.RESET}!")
    while 1:
        result=command.readCommand()
        if result=='FK':
            break
    print("Thanks for using.")


main()

# RawCode=input("请输入所提交的源码：")
