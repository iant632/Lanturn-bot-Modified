#These are the comments provided by olliz0r. These may be useful if you need to calibrate for other languages
#Commands:
#make sure to append \r\n to the end of the command string or the switch args parser might not work
#responses end with a \n (only poke has a response atm)

#click A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#press A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#release A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE

#peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
#poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>

#setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF


import socket
import time
import binascii
import struct
import sys
import os.path
from binascii import unhexlify
from PK8 import *
from NumpadInterpreter import *


#Get yuor switch IP from the system settings under the internet tab
#Should be listed under "Connection Status" as 'IP Address'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("172.30.1.54", 6000))
code = ""

def sendCommand(s, content):
    content += '\r\n' #important for the parser on the switch side
    s.sendall(content.encode())

#New interpreter for new packet structure
def bytesToInt(bytedata, length):
        data = list()
        j = 0
        i = 0
        while j < length:
            if bytedata[j] == 0x0A:
                break
            digit = str(chr(bytedata[i])) + str(chr(bytedata[i+1]))
            data.append(int(digit, 16))
            j += 1
            i += 2

        return data

#New interpreter for new packet structure
def convertToString(arr):
    size = len(arr)
    i = 0
    strings = list()
    accumulator = ""
    while i < size:
        if arr[i] == 0x0A:
            strings.append(accumulator)
            accumulator = ""
        if arr[i] != 0x0D or arr[i] != 0x0A:
            accumulator = accumulator + str(chr(arr[i]))
        i += 1

    return accumulator

#New interpreter for new packet structure
def convertToBytes(arr):
    size = len(arr)
    i = 0
    accumulator = ""
    while i < size:
        if arr[i] == 0xA:
            break
        accumulator = accumulator + str(chr(arr[i]))
        i += 1

    return accumulator

#For the new sys-botbase
#Allows for faster and more reliable inputs
def sendCmdHelper(s, cmd):
    sendCommand(s, cmd)
    time.sleep(0.5)
    echo = s.recv(689)
    strng = convertToString(echo[0:-2])
    #If response not received, try again
    #If received, go to the next button
    while not cmd in strng:
        #sendCommand(s, cmd)
        print("Error!")
        echo = s.recv(689)
        strng = convertToString(echo[0:-2])
    print(str(cmd))

def sendKeypadHelper(s, cmd):
    sendCommand(s, cmd)
    time.sleep(0.3)
    echo = s.recv(689)
    echo = convertToString(echo[0:-2])
    print(str(echo))
    #If response not received, try again
    #If received, go to the next button
    while echo != cmd:
        #sendCommand(s, cmd)
        echo = s.recv(689)
        echo = convertToString(echo[0:-2])

#Cleans out the file relied for communication
def cleanEnvironment():
    fileOut = open("com.bin", "r+b")
    fileOut.seek(8)
    fileOut.write(bytes([0]))
    fileOut.seek(9)
    fileOut.write(bytes([0]))
    fileOut.seek(10)
    fileOut.write(bytes([0]))
    fileOut.seek(11)
    fileOut.write(bytes([0]))
    fileOut.seek(12)
    fileOut.write(bytes([0]))
    fileOut.seek(13)
    fileOut.write(bytes([0]))
    fileOut.seek(14)
    fileOut.write(bytes([0]))
    fileOut.close()

#Writes timeout flag to file
def timedOut():
    fileOut = open("com.bin", "r+b")
    fileOut.seek(8)
    fileOut.write(bytes([0]))
    fileOut.seek(10)
    fileOut.write(bytes([1]))
    fileOut.close()

def writeTrade():
    fileOut = open("com.bin", "r+b")
    fileOut.seek(8)
    fileOut.write(bytes([1]))
    fileOut.close()

#Interprets sequence of strings in arraylist
def interpretStringList(arr):
    length = len(arr)
    i = 0
    while i < length:
        sendCmdHelper(s, arr[i])
        i+=1

#Calibrated for games set to english
#Will exit the trade once the timeout period is reached
def timeOutTradeSearch():

    sendCmdHelper(s, "click Y")
    time.sleep(0.6)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)

    sendCmdHelper(s, "click B")
    time.sleep(0.2)
    sendCmdHelper(s, "click B")
    time.sleep(0.2)

#Exits trade if a disconnection occured
#or if the player refused to input a pokemon
def exitTrade():
    sendCmdHelper(s, "click B")
    sendCmdHelper(s, "click A")
    time.sleep(0.2)

#Calibrated for games set to english
#Starts up trade and inputs code
def initiateTrade():
    global code

    datalist, code = getButtons(None)
    fcode = open("code2.txt", "w")
    fcode.write(code)
    fcode.close()
        
    fileOut = open("com.bin", "r+b")
    fileOut.seek(8)
    fileOut.write(bytes([1]))
    fileOut.seek(9)
    fileOut.write(bytes([1]))
    fileOut.seek(10)
    fileOut.write(bytes([0]))
    fileOut.seek(11)
    fileOut.write(bytes([0]))
    fileOut.seek(12)
    fileOut.write(bytes([0]))
    fileOut.seek(13)
    fileOut.write(bytes([0]))
    fileOut.close()

    #Gets to the code input menu
    sendCmdHelper(s, "click Y")
    time.sleep(0.6)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click DDOWN")
    
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)

    #uncomment if you are using in Japanese
    sendCmdHelper(s, "click A")
    time.sleep(0.8)


    #Get passcode button sequence and input them
    #Pass None if you want your code randomly generated
    #Pass in a 4 digit number not containing any zeros for a fixed code
    interpretStringList(datalist)

    #Confirm passcode and exit the menu
    sendCmdHelper(s, "click PLUS")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)
    sendCmdHelper(s, "click A")
    time.sleep(0.2)

    #Just to be safe since this is a very important part
    sendCommand(s, f"poke 0x2F7240A0 0x00000000")
    time.sleep(0.5)
    s.recv(689)
    sendCommand(s, f"poke 0x2F7240A0 0x00000000")
    time.sleep(0.5)
    s.recv(689)
    sendCommand(s, f"poke 0x2F724084 0x00000000")
    time.sleep(0.5)
    s.recv(689)
    sendCommand(s, f"poke 0x2F724084 0x00000000")
    time.sleep(0.5)
    s.recv(689)

#Start up program and clean up necessary files
print("Cleaning environment...")
cleanEnvironment()
print("Environment cleaned!")

#Has the bot echo last command
sendCommand(s, "configure echoCommands 1")
time.sleep(1.0)
s.recv(689)

print("Awaiting inputs...")



while True:
    fileIn = open("com.bin", "rb")
    fileIn.seek(8)
    tradeState = int(fileIn.read()[0])
    fileIn.close()

    if tradeState == 1:
        print("Bot initialized!")
        print("Button Sequence:")
        initiateTrade()

        canTrade = True

        start = time.time()
        fileOut = open("com.bin", "r+b")
        fileOut.seek(11)
        fileOut.write(bytes([1]))
        fileOut.close()
        while True:
            sendCommand(s, "peek 0x2F724084 4")
            time.sleep(0.5)

            proceed = False

            while not proceed:
                try:
                    tradeCheck = s.recv(689)
                    tradeCheck = int(convertToBytes(tradeCheck), 16)
                    proceed = True
                except:
                    print("Error getting data, trying again.")
                    sendCommand(s, "peek 0x2F724084 4")
                    time.sleep(0.5)

            end = time.time()
            if tradeCheck != 0:
                print("Trade Started!")
                canTrade = True
                fileOut = open("com.bin", "r+b")
                fileOut.seek(13)
                fileOut.write(bytes([1]))
                fileOut.close()
                break
            if (end - start) >= 62:
                timeOutTradeSearch()
                timedOut()
                canTrade = False
                break

        if canTrade:
            start = time.time()
            writeTrade()

            while True:
                sendCommand(s, "peek 0x2F7240A0 4")
                time.sleep(0.5)

                proceed = False

                while not proceed:
                    try:
                        memCheck = s.recv(689)
                        memCheck = int(convertToBytes(memCheck), 16)
                        proceed = True
                    except:
                        sendCommand(s, "peek 0x2F7240A0 4")
                        time.sleep(0.5)

                #print(memCheck)
                end = time.time()
                if memCheck != 0:
                    canTrade = True
                    break
                if (end - start) >= 30:
                    exitTrade()
                    timedOut()
                    canTrade = False
                    break
            
            if canTrade:
                exitTrade()
                sendCommand(s, "peek 0x2F72408A 328")
                time.sleep(0.5)

                ek8 = s.recv(689)

                #ek8 = binascii.unhexlify(ek8[0:-1])
                ##print("Received data: " + str(ek8))
                data = bytesToInt(ek8, 0x148)
                ##print("Encrypted Data: " + str(data))
                decryptor = PK8(data)
                decryptor.decrypt()
                pk8 = decryptor.getData()
                pk = decryptor.getPK()
                if pk < 891 and pk > 0:
                    OT = decryptor.getOT()
                    year, day, month = decryptor.getDate()

                    ec = decryptor.getEncryptionConstant()
                    pid = decryptor.getPID()
                    print("Encryption Constant: " + str(hex(ec)))
                    print("pid: " + str(hex(pid)))
                    print("OT: " + OT)
                    print("date: " + str(year)+str(day)+str(month))
                    print("PK: " + str(pk))

                else:
                    print("Error!")

                pk8Out = open("out2.pk8", "wb")
                pk8Out.write(bytes(pk8))
                pk8Out.close()

                fileOut = open("com.bin", "r+b")
                fileOut.seek(8)
                fileOut.write(bytes([0]))
                fileOut.seek(9)
                fileOut.write(bytes([0]))
                fileOut.seek(10)
                fileOut.write(bytes([0]))
                fileOut.seek(11)
                fileOut.write(bytes([0]))
                fileOut.seek(12)
                fileOut.write(bytes([0]))
                fileOut.seek(13)
                fileOut.write(bytes([0]))
                fileOut.close()

                attempts = 0
                while not os.path.isfile("out2.pk8") and attempts < 10:
                    pk8Out = open("out2.pk8", "wb")
                    pk8Out.write(bytes(pk8))
                    pk8Out.close()
                    attempts += 1

        print("Awaiting inputs...")
    time.sleep(1.8)