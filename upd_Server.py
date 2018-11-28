#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pickle
import os 

IP = '192.168.8.172' #айпи сервера
PORT = 8000 #порт сервера
TIMEOUT = 60 #время ожидания ответа сервера [сек]

BASE_SPEED = 100

def SetSpeed(leftSpeed, rightSpeed):
    print(leftSpeed, rightSpeed)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #создаем udp сервер
server.bind((IP, PORT)) #запускаем udp сервер
print("Listening on port %d..." % PORT) #выводим сообщение о запуске сервера
server.settimeout(TIMEOUT) #указываем серверу время ожидания

while True: #создаем бесконечный цикл    
    try:
        data = server.recvfrom(1024) #попытка получить 1024 байта
    except socket.timeout:
        print("Time is out...")
        break
    parseData = pickle.loads(data[0])

    leftSpeed = parseData[1]*BASE_SPEED + parseData[0]*BASE_SPEED//2
    rightSpeed = parseData[1]*BASE_SPEED - parseData[0]*BASE_SPEED//2

    SetSpeed(leftSpeed, rightSpeed)


    #msg = 'Ok'
    #server.sendto(msg.encode('utf-8'), adrs)
server.close()
