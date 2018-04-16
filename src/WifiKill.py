#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import sleep
from scan import scanning, spoofing
import subprocess
from socket import inet_ntoa
from struct import pack
from netifaces import interfaces
from os import getenv

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END ,WARNING= '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m',\
                                                        '\033[1;32m', '\033[0m', '\033[93m'


def display(buffer, color):
    """Display text with style"""

    sys.stdout.write(color)
    for i in buffer:
        sys.stdout.write(i)
        sys.stdout.flush()
        sleep(0.003)
    sys.stdout.write(WHITE)


def heading():
    """Display the header at the beginning"""

    sys.stdout.write(RED + """



██╗    ██╗██╗███████╗██╗██╗  ██╗██╗██╗     ██╗       
██║    ██║██║██╔════╝██║██║ ██╔╝██║██║     ██║     
██║ █╗ ██║██║█████╗  ██║█████╔╝ ██║██║     ██║     
██║███╗██║██║██╔══╝  ██║██╔═██╗ ██║██║     ██║     
╚███╔███╔╝██║██║     ██║██║  ██╗██║███████╗███████╗
 ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝



""")


def menu():
    """Display the menu in order to use the script"""

    if getenv("SUDO_USER") is None:
        print ('This script need root privilege')
        exit(0)
    display("1) Kick one device\n", GREEN)
    sleep(0.05)
    display("2) Kick some devices\n", WARNING)
    sleep(0.05)
    display("3) Kick all devices (not supported now)\n", RED)

    while True:
        try:
            display("What do you want to do ? ", WHITE)
            choice = input("")
            choice = int(choice)
            return choice

        except Exception as Err:
            display("[!] pls Enter a number\n", WHITE)


def ip_to_netmask(ip):
    """Change the ip range to network netmask"""

    network, cidr = ip.split('/')
    host_bits = 32 - int(cidr)
    netmask = inet_ntoa(pack('!I', (1 << 32) - (1 << host_bits)))
    return network, netmask, cidr


def RangeOfIps(iface):
    """Return the range of the network"""

    # Only support linux for now
    try:
        cmd = "ip addr | grep 'inet ' | grep " + iface + \
              " | grep -oE [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[1-9]{2}"
        # Command on linux host
        ip = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        network, netmask, cidr = ip_to_netmask(ip)
        network = network.split('.')  # 4 elements
        netmask = netmask.split('.')  # 4 elements
        subnet = []
        for i in range(4):
            subnet.append(str(int(network[i]) & int(netmask[i])))
        ips = '.'.join(subnet) + '/%s' % cidr
        print (ips)
        return ips

    except Exception as Err:
        print (Err)


def main():

    heading()
    attackmode = menu()
    try:
        # Useful to list networks interfaces
        for i in interfaces():
            display(i+'\n', WHITE)
        display("[*] Enter desired interface : ", WHITE)
        iface = raw_input("")

        display("[*] Enter down time for ip(s) : ",WHITE)
        downtime = raw_input("")

    except KeyboardInterrupt:
        display("\n[*] User request shutdown", WHITE )
        display("\n[*] Quitting ... \n", WHITE)
        sys.exit(1)
    ips = RangeOfIps(iface)
    scanning(iface, ips)
    spoofing(attackmode, downtime)


if __name__ == '__main__':
        main()
