# Definitions of functions responsible for socket connection and xml parsing


import socket
import xml.etree.ElementTree as ET
import sys
import re

def ConnectToServer(host = 'codearena.pl', port = 7654):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    xml_msg = ET.Element('connect')
    xml_msg.set('hashid','a7c129489fc70e66e1aa01aec799d910')
    xml_msg.set('userid','129')
    txt_msg = ET.tostring(xml_msg)
    SendMsg(s, txt_msg)
    root = ReceiveAndParse(s)
    return (s,root)

def SendMsg(s, msg):
    s.sendall(msg)

def ReceiveAndParse(s, num = 1024):
    data = s.recv(num)
    data_tab = re.split('<\?xml version=.*\?>',data)
    resp_list = []
    for d in data_tab:
        if d != '':
            resp_list.append(ET.fromstring(d))
    return resp_list

