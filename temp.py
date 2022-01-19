# SECOND VERSION
# 20/JAN/2022: Mimic Blackmagic Web Presentor ethernet output.

#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9977        # default port Web Presenter

#Make ACK and NAK visible
debug = 1
if debug:
    ACK = "[ACK]"
    NAK = "[NAK]"
else:
    ACK = "\6"
    NAK = "\21"
    
LF  = "\n"
CR  = "\r"  
OUT = ": "
ACCEPT = ACK + LF + CR
DECLINE = NAK + LF + CR
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

def On_Connect():
    LINES = "PROTOCOL PREAMBLE:" +CR+LF+ "Version: 1.0" +CR+LF+ "END PRELUDE:" +CR+LF+CR+LF
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
    buffer_1 = ''
    buffer_2 = ''
    buffer_1 = conn.recv(1024)
    if not buffer_1:
        return
    buffer_1 = buffer_1.decode('utf-8')
    if Search('\r', buffer_1):
        buffer_1 = buffer_1.replace(ACK, '[ACK]')
        buffer_1 = buffer_1.replace(NAK, '[NAK]')
        buffer_1 = buffer_1.replace('\r','[CR]')
        buffer_1 = buffer_1.replace('\n','[LF]')
    else:
        buffer_2 = conn.recv(1024)
        if buffer_2:
            buffer_2 = buffer_2.decode('utf-8')
            if Search('\r', buffer_2):
                buffer_2 = buffer_2.replace(ACK, '[ACK]')
                buffer_2 = buffer_2.replace(NAK, '[NAK]')
                buffer_2 = buffer_2.replace('\r','[CR]')
                buffer_2 = buffer_2.replace('\n','[LF]')
        else:
            pass
    if debug:
        print('Received: ' + buffer_1 + buffer_2)
    return buffer_1 + buffer_2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        conn.sendall(On_Connect())
        while True:
            stringdata = Recv()

            TEMP = None
            CHANGE = False
            for k, v in CONFIGURATION.items():
                if Search(k, stringdata):
                    NAME = k
                    TEMP = v
            while (stringdata != "[CR][LF]"):
                for k, v in TEMP.items():
                    if Search(k, stringdata):
                        CHANGE = True
                        #How to find the correct location
                stringdata = Recv()
            if TEMP:
                if CHANGE:
                    Transmit(ACK)
                    Transmit(EMPTY)
                    Transmit(NAME)
                    #Print the ones that changed
                else:
                    Transmit(ACK)
                    Transmit(EMPTY)
                    Transmit(NAME)
                    for k, v in TEMP.items():
                        Transmit(k + OUT + v)
                    Transmit(EMPTY)