# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 13:14:48 2023

@author: ANNIAC (Hamudrel)
"""

import socket
import re
import keyboard

# file path for where you want the data to output
data_file_path = r"OUTPUT FILE PATH HERE"
data_file = open(data_file_path, "a")

# regex for the prompt
regex = r'{"prompt":[\s]*".*",[\s]*"completion":[\s]*".*"}'

# connection info, get the token from https://twitchapps.com/tmi/ 
server = 'irc.chat.twitch.tv'
port = 6667
nickname = ''
token = ''
channel = '#CHANNEL_NAME'

# create socket and connect
sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

while True:
    # receive messages from Twitch
    resp = sock.recv(2048).decode('utf-8')
    
    #remove irrelevant data
    r = ' '.join(resp.split()[3:])[1:]
    
    # prevent Twitch's Ping-Pong request from going unanswered. Little fella just needs a friend.
    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    
    # if the message is a valid prompt, save it to the output file
    elif re.search(regex,resp):
        data_file = open(data_file_path, "a")
        data_file.write(resp)
        data_file.close()
        
    # not the best way to break the loop, but it works
    elif keyboard.is_pressed('q'):
        break

sock.close()