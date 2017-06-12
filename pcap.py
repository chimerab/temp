#!/usr/bin/python
# -*- coding: UTF-8 -*-


import re
import zlib


from scapy.all import *

a = rdpcap("/root/workspace/test2.pcap")

sessions = a.sessions()

for session in sessions:
    for packet in sessions[session]:
        print packet[TCP].dport