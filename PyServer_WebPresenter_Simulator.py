# FIRST VERSION
# 17/JAN/2022: Mimic Blackmagic Web Presentor ethernet output.

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

IDENTITY = {}
IDENTITY["Model"]       = "Blackmagic Web Presenter HD"
IDENTITY["Label"]       = "Blackmagic Web Presenter HD"
IDENTITY["Unique ID"]   = "00112233445566778899AABBCCDDEEFF"
MEM_IDENTITY = {}
MEM_IDENTITY["Model"]       = "Blackmagic Web Presenter HD"
MEM_IDENTITY["Label"]       = "Blackmagic Web Presenter HD"
MEM_IDENTITY["Unique ID"]   = "00112233445566778899AABBCCDDEEFF"

VERSION = {}
VERSION["Product ID"]        = "BE73"
VERSION["Hardware Version"]  = "0100"
VERSION["Software Version"]  = "48858B6F"
VERSION["Software Release"]  = "2.0"
MEM_VERSION = {}
MEM_VERSION["Product ID"]        = "BE73"
MEM_VERSION["Hardware Version"]  = "0100"
MEM_VERSION["Software Version"]  = "48858B6F"
MEM_VERSION["Software Release"]  = "2.0"

NETWORK = {}
NETWORK["Interface Count"]      = "2"
NETWORK["Default Interface"]    = "0"
NETWORK["Static DNS Servers"]   = "8.8.8.8, 8.8.4.4"
NETWORK["Current DNS Servers"]  = "192.168.1.1, 8.8.4.4"
MEM_NETWORK = {}
MEM_NETWORK["Interface Count"]      = "2"
MEM_NETWORK["Default Interface"]    = "0"
MEM_NETWORK["Static DNS Servers"]   = "8.8.8.8, 8.8.4.4"
MEM_NETWORK["Current DNS Servers"]  = "192.168.1.1, 8.8.4.4"

NETWORKINTERFACE0 = {}
NETWORKINTERFACE0["Name"]                = "Cadence GigE Ethernet MAC" 
NETWORKINTERFACE0["Priority"]            = "1"
NETWORKINTERFACE0["MAC Address"]         = "00:11:22:33:44:55"
NETWORKINTERFACE0["Dynamic IP"]          = "true"
NETWORKINTERFACE0["Current Addresses"]   = "192.168.1.10/255.255.255.0"
NETWORKINTERFACE0["Current Gateway"]     = "192.168.1.1"
NETWORKINTERFACE0["Static Addresses"]    = "10.0.0.2/255.255.255.0"
NETWORKINTERFACE0["Static Gateway"]      = "10.0.0.1"
MEM_NETWORKINTERFACE0 = {}
MEM_NETWORKINTERFACE0["Name"]                = "Cadence GigE Ethernet MAC" 
MEM_NETWORKINTERFACE0["Priority"]            = "1"
MEM_NETWORKINTERFACE0["MAC Address"]         = "00:11:22:33:44:55"
MEM_NETWORKINTERFACE0["Dynamic IP"]          = "true"
MEM_NETWORKINTERFACE0["Current Addresses"]   = "192.168.1.10/255.255.255.0"
MEM_NETWORKINTERFACE0["Current Gateway"]     = "192.168.1.1"
MEM_NETWORKINTERFACE0["Static Addresses"]    = "10.0.0.2/255.255.255.0"
MEM_NETWORKINTERFACE0["Static Gateway"]      = "10.0.0.1"

NETWORKINTERFACE1 = {}
NETWORKINTERFACE1["Name"]                = "USB Ethernet" 
NETWORKINTERFACE1["Priority"]            = ""
NETWORKINTERFACE1["MAC Address"]         = "00:00:00:00:00:00"
NETWORKINTERFACE1["Dynamic IP"]          = "true"
NETWORKINTERFACE1["Current Addresses"]   = "192.168.1.10/255.255.255.0"
NETWORKINTERFACE1["Current Gateway"]     = "192.168.1.1"
NETWORKINTERFACE1["Static Addresses"]    = "10.0.0.2/255.255.255.0"
NETWORKINTERFACE1["Static Gateway"]      = "10.0.0.1"
MEM_NETWORKINTERFACE1 = {}
MEM_NETWORKINTERFACE1["Name"]                = "USB Ethernet" 
MEM_NETWORKINTERFACE1["Priority"]            = ""
MEM_NETWORKINTERFACE1["MAC Address"]         = "00:00:00:00:00:00"
MEM_NETWORKINTERFACE1["Dynamic IP"]          = "true"
MEM_NETWORKINTERFACE1["Current Addresses"]   = "192.168.1.10/255.255.255.0"
MEM_NETWORKINTERFACE1["Current Gateway"]     = "192.168.1.1"
MEM_NETWORKINTERFACE1["Static Addresses"]    = "10.0.0.2/255.255.255.0"
MEM_NETWORKINTERFACE1["Static Gateway"]      = "10.0.0.1"

UISETTINGS = {}
UISETTINGS["Available Locales"]         = "en_US.UTF-8, zh_CN.UTF-8, ja_JP.UTF-8, ko_KR.UTF-8, es_ES.UTF-8, de_DE.UTF-8, fr_FR.UTF-8, ru_RU.UTF-8, it_IT.UTF-8, pt_BR.UTF-8,tr_TR.UTF-8" 
UISETTINGS["Current Locale"]            = "en_US.UTF-8" 
UISETTINGS["Available Audio Meters"]    = "PPM -18dB, PPM -20dB, VU -18dB, VU -20dB"
UISETTINGS["Current Audio Meter"]       = "PPM -20dB"
MEM_UISETTINGS = {}
MEM_UISETTINGS["Available Locales"]         = "en_US.UTF-8, zh_CN.UTF-8, ja_JP.UTF-8, ko_KR.UTF-8, es_ES.UTF-8, de_DE.UTF-8, fr_FR.UTF-8, ru_RU.UTF-8, it_IT.UTF-8, pt_BR.UTF-8,tr_TR.UTF-8" 
MEM_UISETTINGS["Current Locale"]            = "en_US.UTF-8" 
MEM_UISETTINGS["Available Audio Meters"]    = "PPM -18dB, PPM -20dB, VU -18dB, VU -20dB"
MEM_UISETTINGS["Current Audio Meter"]       = "PPM -20dB"

STREAMSETTINGS = {}
STREAMSETTINGS["Available Video Modes"]         = "Auto, 1080p23.98, 1080p24, 1080p25, 1080p29.97,1080p30, 1080p50, 1080p59.94, 1080p60, 720p25, 720p30, 720p50, 720p60"
STREAMSETTINGS["Video Mode"]                    = "1080p59.94"
STREAMSETTINGS["Current Platform"]              = "YouTube"
STREAMSETTINGS["Current Server"]                = "Primary"
STREAMSETTINGS["Current Quality Level"]         = "Streaming Medium"
STREAMSETTINGS["Stream Key"]                    = "abc1-def2-ghi3-jkl4-mno5"
STREAMSETTINGS["Available Default Platforms"]   = "Facebook, Twitch, YouTube, Twitter / Periscope, Restream.IO"
STREAMSETTINGS["Available Custom Platforms"]    = "My Platform"
STREAMSETTINGS["Available Servers"]             = "Primary, Secondary"
STREAMSETTINGS["Available Quality Levels"]      = "HyperDeck High, HyperDeck Medium, HyperDeck Low, Streaming High, Streaming Medium, Streaming Low"
MEM_STREAMSETTINGS = {}
MEM_STREAMSETTINGS["Available Video Modes"]         = "Auto, 1080p23.98, 1080p24, 1080p25, 1080p29.97,1080p30, 1080p50, 1080p59.94, 1080p60, 720p25, 720p30, 720p50, 720p60"
MEM_STREAMSETTINGS["Video Mode"]                    = "1080p59.94"
MEM_STREAMSETTINGS["Current Platform"]              = "YouTube"
MEM_STREAMSETTINGS["Current Server"]                = "Primary"
MEM_STREAMSETTINGS["Current Quality Level"]         = "Streaming Medium"
MEM_STREAMSETTINGS["Stream Key"]                    = "abc1-def2-ghi3-jkl4-mno5"
MEM_STREAMSETTINGS["Available Default Platforms"]   = "Facebook, Twitch, YouTube, Twitter / Periscope, Restream.IO"
MEM_STREAMSETTINGS["Available Custom Platforms"]    = "My Platform"
MEM_STREAMSETTINGS["Available Servers"]             = "Primary, Secondary"
MEM_STREAMSETTINGS["Available Quality Levels"]      = "HyperDeck High, HyperDeck Medium, HyperDeck Low, Streaming High, Streaming Medium, Streaming Low"

STREAMSTATE = {}
STREAMSTATE["Status"]   = "Idle"
STREAMSTATE["Action"]   = "Stop"
STREAMSTATE["Duration"] = "DD:HH:MM:SS"
STREAMSTATE["Bitrate"]  = "bps"
MEM_STREAMSTATE = {}
MEM_STREAMSTATE["Status"]   = "Idle"
MEM_STREAMSTATE["Action"]   = "Stop"
MEM_STREAMSTATE["Duration"] = "DD:HH:MM:SS"
MEM_STREAMSTATE["Bitrate"]  = "bps"

SHUTDOWN = {}
SHUTDOWN["Action"]   = "Reboot"
MEM_SHUTDOWN = {}
MEM_SHUTDOWN["Action"]   = "Reboot"

def On_Connect():
    LINES = "PROTOCOL PREAMBLE:" +CR+LF+ "Version: 1.0" +CR+LF+ "END PRELUDE:" +CR+LF+CR+LF
    sent = bytes(LINES, encoding="utf-8")
    return sent

def Search(Key, Data):
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

def Recieve():
    data = conn.recv(1024)
    recv = data.decode('utf-8')
    recv = recv.replace(ACK, '[ACK]')
    recv = recv.replace(NAK, '[NAK]')
    recv = recv.replace(LF, '[LF]')
    recv = recv.replace(CR, '[CR]')
    return recv


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
            
            if Search('IDENTITY:',stringdata): #Identity block
                stringdata = Recv()
                IDENTITY_BIT = False
                while (stringdata != "[CR][LF]"):     
                    for key, value in IDENTITY.items():
                        if Search(key, stringdata):
                            IDENTITY_BIT = True
                            IDENTITY[key] = stringdata[(len(key)+2):Pos('[',stringdata)]
                    stringdata = Recv()
                if IDENTITY_BIT:
                    Transmit(ACK)
                    Transmit(EMPTY)
                    Transmit('IDENTITY:')
                    for key, value in IDENTITY.items():
                        if MEM_IDENTITY[key] != IDENTITY[key]:
                            MEM_IDENTITY[key] = IDENTITY[key]
                            Transmit(key + OUT + value)
                    Transmit(EMPTY)
                else:
                    Transmit('IDENTITY:')
                    for key, value in IDENTITY.items() :
                        Transmit(key + OUT + value)
                    Transmit(EMPTY)

            if Search('VERSION:',stringdata): #Version block
                stringdata = Recv() #'Key' or '[LF][CR]'
                if stringdata == "[CR][LF]":
                    for key, value in VERSION.items() :
                        Transmit(key + OUT + value)
                    Transmit("")

            if not stringdata:
                break
