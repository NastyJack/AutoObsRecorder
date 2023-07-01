
import datetime
import os
import glob
import psutil
import shutil
from config import gameList
from playsound import playsound
from pyautogui import press, typewrite, hotkey


dateFile = 'G:\Tech_Stuff\CODE\Auto_OBS_Recorder\Date.txt'
videoFilePath = 'G:\Tech_Stuff\Highlights\REC\*'
stableDiffusionOutputFilePath = 'G:\Tech_Stuff\stableDiffusion\stable-diffusion-webui\outputs\\'
bakkesMod = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BakkesMod.lnk'
bakkesModProcess = 'BakkesMod.exe'
BakkesModIsRunning = False
todaysDate = datetime.date.today().strftime("%d")


def performDateCheck():
    try:
        with open(dateFile, 'r') as File:
            oldDate = File.read()
            File.close()
        with open(dateFile, 'w') as File:
            # if(oldDate != todaysDate):
            print('Deleting stable diffusion output')
            deleteStableDiffusionOutput()
            if (int(todaysDate) - int(oldDate) > 2):
                print('Deleting old videos')
                deleteOldVideos()
            else:
                print('Condition not met for deletion.')
            File.write(todaysDate)
            File.close()
    except Exception as e:
        print('Encountered Error. Writing null to file.', e)
        with open(dateFile, 'w') as File:
            File.write('null')
            File.close()


def deleteOldVideos():
    try:
        folder = glob.glob(videoFilePath)
        for files in folder:
            os.remove(files)
        print('Deleted all videos!')
    except Exception as e:
        print('Not deleted videos', e)


def deleteStableDiffusionOutput():
    try:
        # delete all files and folders in directory
        # folder = glob.glob(stableDiffusionOutputFilePath)
        shutil.rmtree(stableDiffusionOutputFilePath)
        print('Deleted all stable diffusion files!')
    except Exception as e:
        print('Not deleted stable diffusion files', e)

    #     folder = glob.glob(stableDiffusionOutputFilePath)
    #     for files in folder:
    #         os.remove(files)
    #     print('Deleted all stable diffusion files!')
    # except Exception as e:
    #     print('Not deleted stable diffusion files',e)


def checkIfGameIsRunning():
    global BakkesModIsRunning
    procName = None
    running = False
    try:
        for proc in psutil.process_iter():
            # if proc.name() == "RocketLeague.exe" or proc.name() == "r5apex.exe" :
            if proc.name() in gameList:
                procName = proc.name()
                running = True
        if (running):
            print("Game is RUNNING ")
        else:
            print("Game is NOT Running")

        if (procName == "RocketLeague.exe" and not BakkesModIsRunning):
            toggleBakkesMod('ON')
            BakkesModIsRunning = True
        return running
    except Exception as e:
        print('Encountered Error. Returning false.', e)
        return False


def toggleRecording(ONorOFF):
    global BakkesModIsRunning
    if (ONorOFF == 'ON'):
        hotkey('alt', 'pageup', interval=0.25)
        playsound('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\ON.mp3')
        print('\nRecording ON\n')
        return True
    else:
        hotkey('alt', 'pagedown', interval=0.25)
        if (BakkesModIsRunning == True):
            toggleBakkesMod('OFF')
            BakkesModIsRunning = False
        BakkesModIsRunning = False
        playsound('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\OFF.mp3')
        print('\nRecording OFF\n')
        return False


def toggleBakkesMod(ONorOFF):
    if (ONorOFF == 'ON'):
        os.startfile(bakkesMod)
        print('BakkesMod ON\n')
        return True
    else:
        os.system("taskkill /im BakkesMod.exe /f")
        print('BakkesMod OFF\n')
        return False
