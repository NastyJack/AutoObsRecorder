
import time
import sys
from pyautogui import hotkey

from helpers import *
import os

isRunning=False
isRecording=False
turnOffOnce=False
toStop=True
failSafe=r'G:\Tech_Stuff\CODE\Auto_OBS_Recorder\writeFalseHereToStop.txt'
deleteOBS_safeMode = r'C:\Users\Nasty_Jack\AppData\Roaming\obs-studio\safe_mode'
obsDirectory = r'E:\Software\obs-studio\bin\64bit'

def main():
    global isRunning
    global isRecording
    global turnOffOnce
    global toStop

    #Create a file if it doesn't exist
    with open(failSafe, 'w') as File:
        File.write('True')     
    
    #Check if date matches to today's date. If not clear videos from folder
    performDateCheck()

    #Check if game is running and recording infinitely. To stop write 'False' to file as a failsafe.
    while toStop!='False' and toStop!='false':         
        with open(failSafe, 'r') as File:
            toStop = File.read() 
        print('Checking if game is running...')
        time.sleep(10)
        isRunning = checkIfGameIsRunning()
        if(isRunning and not isRecording):
            isRecording = toggleRecording('ON')
            turnOffOnce = True
        elif(not isRunning and turnOffOnce):
            isRecording = toggleRecording('OFF')
            turnOffOnce = False
        if(isRunning and isRecording):
            print('\n__currently recording game__\n')            
    
    print('EXITING SCRIPT')
    hotkey('alt','pagedown',interval=0.25)
    sys.exit()

if __name__=="__main__":
   main()


                                   


