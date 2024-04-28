
from pyautogui import hotkey
from config import gameList
from pywinauto import Application
from pydub import AudioSegment
from pydub.playback import play

import pyautogui
import datetime
import os
import glob
import psutil
import shutil
import subprocess
import time
import keyboard


dateFile = 'G:\Tech_Stuff\CODE\Auto_OBS_Recorder\Date.txt'
videoFilePath = 'G:\Tech_Stuff\Highlights\REC\\'
stableDiffusionOutputFilePath = 'G:\Tech_Stuff\stableDiffusion\stable-diffusion-webui\outputs\\'
bakkesMod = 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BakkesMod.lnk'
bakkesModProcess = 'BakkesMod.exe'
BakkesModIsRunning = False
todaysDate = datetime.date.today().strftime("%d")
daysToKeep = 1
current_playlist_index = 0

spotifyPath = 'C:/Users/Nasty_Jack/AppData/Roaming/Spotify/Spotify.exe'
osVolume = 8
spotifyVolume = 80
playlist_uris = [
    '00GARohVljsECuUcNSfvSz',  # Evil EDM
    '7e4Bnf7RxQYGsR9kqV7yjs',  # Pop Wihtout The Corn
    '3Xj7R4u8O3QPgvu3Ja9Jud',  # Offbeat EDM
    '5A7t00DC3dP7htDmFsjF2I'  # Rocket League x Monstercat
]


def performDateCheck():
    try:
        # get difference between today's date and date in the oldest file at path videoFilePath
        delete_files_older_than(videoFilePath, daysToKeep)
        print('Deleting stable diffusion output')
        deleteStableDiffusionOutput()

    except Exception as e:
        print('Encountered Error. Writing null to file.', e)
        with open(dateFile, 'w') as File:
            File.write('null')
            File.close()


def delete_files_older_than(videoFilePath, days):

    # Delete video files older than a given number of days.
    today = datetime.datetime.now()

    for root, _, files in os.walk(videoFilePath):
        for file in files:

            if file.endswith(".mp4") or file.endswith(".mkv"):
                file_path = os.path.join(root, file)
                creation_date = get_creation_date(file_path)
                delta = today - creation_date
                if delta.days > days:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")


def get_creation_date(file_path):
    """Get the creation date of a file."""
    timestamp = os.path.getctime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

# ================================================ SPOTIFY BEGIN ==============================================================


def start_spotify_with_playlist(current_playlist_uri):
    try:
        # Check if Spotify is already running
        running_spotify_process = any("spotify.exe" in p.name()
                                      for p in psutil.process_iter())

        if not running_spotify_process:
            # Start Spotify process with random mode flag
            subprocess.Popen([spotifyPath, "--shuffle"])

            # Wait for Spotify to open
            time.sleep(5)
        # Connect to the running Spotify application
        app = Application().connect(title="Spotify Free")

        # Set OS volume
        # print(" @@@@@@@@@@@@ before test this!!!", current_playlist_index)
        subprocess.Popen(['nircmdc.exe', "setsysvolume", str(osVolume)])

        # Set Spotify volume
        subprocess.Popen(['nircmdc.exe', "mixervolume",
                         "Spotify.exe", str(spotifyVolume)])

        # Get the Spotify main window handle
        main_window = app.window(title="Spotify Free")

        # Maximize the Spotify window (optional)
        main_window.minimize()

        # Play the playlist
        # Assumes playlist order is 1-indexed
        # main_window.type_keys(f"%{current_playlist_uri+1 }")

        main_window.type_keys("^k")
        time.sleep(1)
        main_window.type_keys(f"spotify:playlist:{current_playlist_uri}")
        time.sleep(1)
        main_window.type_keys("{ENTER}")
        time.sleep(5)
        main_window.type_keys("{SPACE}")
        time.sleep(1)
        main_window.type_keys("{TAB}")
        time.sleep(1)
        main_window.type_keys("{TAB}")
        time.sleep(1)
        main_window.type_keys("{TAB}")
        time.sleep(1)
        main_window.type_keys("{TAB}")
        time.sleep(1)
        main_window.type_keys("{TAB}")
        time.sleep(1)

        # Play the playlist
        # pyautogui.typewrite(['enter'])
    except Exception as e:
        print('Encountered error at start_spotify_with_playlists', e)


def cycle_playlists():

    # Get the current playlist URI from the list
    current_playlist_uri = playlist_uris[current_playlist_index]

    # Start Spotify with the current playlist
    start_spotify_with_playlist(current_playlist_uri)

    # Increase the index to cycle to the next playlist
    current_playlist_index = (current_playlist_index + 1) % len(playlist_uris)


# ================================================ SPOTIFY END ==============================================================


def deleteStableDiffusionOutput():
    try:
        shutil.rmtree(stableDiffusionOutputFilePath)
        print('Deleted all stable diffusion files!')
    except Exception as e:
        print('Not deleted stable diffusion files', e)


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

            # start_spotify_with_playlist(playlist_uris[0])
            # keyboard.on_press_key("num -", cycle_playlists())

        return running
    except Exception as e:
        print('Encountered Error. Returning false.', e)
        return False


def toggleRecording(ONorOFF):
    global BakkesModIsRunning
    if (ONorOFF == 'ON'):
        hotkey('alt', 'pageup', interval=0.25)
        play_mp3('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\ON.mp3')
        # playsound('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\ON.mp3')
        print('\nRecording ON\n')
        return True
    else:
        hotkey('alt', 'pagedown', interval=0.25)
        if (BakkesModIsRunning == True):
            toggleBakkesMod('OFF')
            BakkesModIsRunning = False
        BakkesModIsRunning = False
        play_mp3('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\OFF.mp3')
        # playsound('G:\Tech_Stuff\CODE\Auto_OBS_Recorder\mp3\OFF.mp3')
        print('\nRecording OFF\n')
        return False


def play_mp3(file_path):
    audio = AudioSegment.from_file(file_path, format="mp3")
    play(audio)


def toggleBakkesMod(ONorOFF):
    if (ONorOFF == 'ON'):
        os.startfile(bakkesMod)
        print('BakkesMod ON\n')
        return True
    else:
        os.system("taskkill /im BakkesMod.exe /f")
        print('BakkesMod OFF\n')
        return False
