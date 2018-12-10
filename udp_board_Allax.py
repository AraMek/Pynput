#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import os
import pickle
import sys
import crc16
sys.path.append('EduBot/EduBotLibrary')
import edubot

#IP = '127.0.0.1'
IP = str(os.popen('hostname -I | cut -d\' \' -f1').readline().replace('\n','')) #получаем IP, удаляем \n
PORT = 8000
TIMEOUT = 60

def SetSpeed(leftSpeed, rightSpeed):
    robot.leftMotor.SetSpeed(leftSpeed)
    robot.rightMotor.SetSpeed(rightSpeed)

robot = edubot.EduBot(1)
assert robot.Check(), 'EduBot not found!!!'
robot.Start() #обязательная процедура, запуск потока отправляющего на контроллер EduBot онлайн сообщений
print ('EduBot started!!!')

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #создаем UDP server
server.bind((IP, PORT)) #запускаем сервер
server.settimeout(TIMEOUT)
print("Listening %s on port %d..." % (IP, PORT))

countPacket = 0
userIP = ''

while True:
    try:
        packet = server.recvfrom(1024) # получаем UDP пакет
    except socket.timeout:
        print('Time is out...')
        break

    countPacket += 1
    if userIP == '':
        userIP = packet[1][0]
        print('Робот зохвачен: %s. xXx_XD_LOL_xXx' % userIP)
    else:
        if packet[1][0] == userIP:
        
            data = packet[0] #полученный массив байт
    
            crcBytes = data[-2:] #берем последние 2 байта из пакета данных
            crc = int.from_bytes(crcBytes, byteorder='big', signed = False)

            stateMoveBytes = data[:-2] #берем байты пакета
            newCrc = crc16.crc16xmodem(stateMoveBytes) #вычисляем CRC16

            if crc == newCrc:
                speed, stateMove = pickle.loads(stateMoveBytes)
                leftSpeed = int(stateMove[1]*speed + stateMove[0]*speed//2)
                rightSpeed = int(stateMove[1]*speed - stateMove[0]*speed//2)
    
                SetSpeed(leftSpeed, rightSpeed)
            else:
                print('%d Error CRC packet' % countPacket)
        else:
            print('Левый пакет от %s' % packet[1][0])

        
server.close()

SetSpeed(0, 0)

#останавливаем поток отправки онлайн сообщений в контроллер EduBot
robot.Release()
print('End program')
