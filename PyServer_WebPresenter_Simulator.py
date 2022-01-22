# SECOND VERSION
# 22/JAN/2022: Mimic Blackmagic Web Presentor ethernet output.

#!/usr/bin/env python3

import socket
import copy

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9977        # default port Web Presenter

ACK = "\6"
NAK = "\21"  
LF  = "\n"
CR  = "\r"  
OUT = ": "
EMPTY = ""

CONFIGURATION = {
    "IDENTITY:" : {
        "Model"     : "Blackmagic Web Presenter HD",
        "Label"     : "Blackmagic Web Presenter HD",
        "Unique ID" : "00112233445566778899AABBCCDDEEFF"
        },
    "VERSION:" : {
        "Product ID"        : "BE73",
        "Hardware Version"  : "0100",
        "Software Version"  : "48858B6F",
        "Software Release"  : "2.0"
        },
    "NETWORK:" : {
        "Interface Count"       : "2",
        "Default Interface"     : "0",
        "Static DNS Servers"    : "8.8.8.8, 8.8.4.4",
        "Current DNS Servers"   : "192.168.1.1, 8.8.4.4"
        },
    "NETWORK INTERFACE 0:" : {
        "Name"                : "Cadence GigE Ethernet MAC", 
        "Priority"            : "1",
        "MAC Address"         : "00:11:22:33:44:55",
        "Dynamic IP"          : "true",
        "Current Addresses"   : "192.168.1.10/255.255.255.0",
        "Current Gateway"     : "192.168.1.1",
        "Static Addresses"    : "10.0.0.2/255.255.255.0",
        "Static Gateway"      : "10.0.0.1"
        },
    "NETWORK INTERFACE 1:" : {
        "Name"                : "USB Ethernet", 
        "Priority"            : "",
        "MAC Address"         : "00:00:00:00:00:00",
        "Dynamic IP"          : "true",
        "Current Addresses"   : "192.168.1.10/255.255.255.0",
        "Current Gateway"     : "192.168.1.1",
        "Static Addresses"    : "10.0.0.2/255.255.255.0",
        "Static Gateway"      : "10.0.0.1"
        },
    "UI SETTINGS:" : {
        "Available Locales"         : "en_US.UTF-8, zh_CN.UTF-8, ja_JP.UTF-8, ko_KR.UTF-8, es_ES.UTF-8, de_DE.UTF-8, fr_FR.UTF-8, ru_RU.UTF-8, it_IT.UTF-8, pt_BR.UTF-8,tr_TR.UTF-8", 
        "Current Locale"            : "en_US.UTF-8", 
        "Available Audio Meters"    : "PPM -18dB, PPM -20dB, VU -18dB, VU -20dB",
        "Current Audio Meter"       : "PPM -20dB"
        },
    "STREAM SETTINGS:" : {
        "Available Video Modes"         : "Auto, 1080p23.98, 1080p24, 1080p25, 1080p29.97,1080p30, 1080p50, 1080p59.94, 1080p60, 720p25, 720p30, 720p50, 720p60",
        "Video Mode"                    : "1080p59.94",
        "Current Platform"              : "YouTube",
        "Current Server"                : "Primary",
        "Current Quality Level"         : "Streaming Medium",
        "Stream Key"                    : "abc1-def2-ghi3-jkl4-mno5",
        "Available Default Platforms"   : "Facebook, Twitch, YouTube, Twitter / Periscope, Restream.IO",
        "Available Custom Platforms"    : "My Platform",
        "Available Servers"             : "Primary, Secondary",
        "Available Quality Levels"      : "HyperDeck High, HyperDeck Medium, HyperDeck Low, Streaming High, Streaming Medium, Streaming Low"
        },
    "STREAM STATE:" : {
        "Status"   : "Idle",
        "Action"   : "Stop",
        "Duration" : "DD:HH:MM:SS",
        "Bitrate"  : "bps"
        },
    "SHUTDOWN:" : {
        "Action"   : "Reboot"
        }
    }

M_CONFIGURATION = {}

def On_Connect():
    LINES = "PROTOCOL PREAMBLE:"+"\r\n"+"Version: 1.0"+"\r\n"+"END PRELUDE:"+"\r\n"+"\r\n"
    sent = bytes(LINES, encoding="utf-8")
    return sent

def Search(Key, Data):
    if Data is None:
        Data = ""
    if int(Data.find(Key)) > -1:
        result = True
    else:
        result = False
    return result

def Pos(Key, Data):
    return int(Data.find(Key))

def Transmit(Input):
    sent = bytes(Input+CR+LF, encoding="utf-8")
    conn.sendall(sent)

def Recv():
    byte_in = ''
    str_out = ''
    while not(Search('\n', str_out)):
        byte_in = conn.recv(1024)
        if byte_in:
            str_out = str_out + byte_in.decode('utf-8')
    return str_out

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        conn.sendall(On_Connect())
        while True:
            stringdata = Recv()

            TEMP = None
            COPY = None
            CHANGE = False
            for k1, v1 in CONFIGURATION.items():
                if Search(k1, stringdata):
                    NAME = k1
                    TEMP = v1
                    COPY = copy.deepcopy(v1)
            while (stringdata != "\r\n" and TEMP):
                for k2, v2 in TEMP.items():
                    if Search(k2, stringdata):
                        CHANGE = True
                        TEMP[k2] = stringdata[(len(k2)+2):Pos('[',stringdata)]
                stringdata = Recv()
            if TEMP:
                if CHANGE:
                    Transmit(ACK)
                    Transmit(EMPTY)
                    Transmit(NAME)
                    for k3, v3 in TEMP.items():
                        if COPY[k3] != TEMP[k3]:
                            Transmit(k3 + OUT + v3)
                    Transmit(EMPTY)
                else:
                    Transmit(ACK)
                    Transmit(EMPTY)
                    Transmit(NAME)
                    for k4, v4 in TEMP.items():
                        Transmit(k4 + OUT + v4)
                    Transmit(EMPTY)
