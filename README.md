<h1 align="center">Welcome to AutoObsRecorder 👋</h1>

![auto-obs-recorder-icon](https://github.com/NastyJack/AutoObsRecorder/assets/44137857/da0eb4c4-4b1a-4058-bdaa-edea40b7796c)

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
</p>



> A python script to automatically record gameplays using OBS. The script will also auto-delete recorded gameplays older than 3 days, so the disk space doesn't get overwhelmed.

## Usage

* Open OBS, head over to settings and set the hotkey for "Start Recording" to Alt+Page Up.

* Then, set the hotkey for "Stop Recording" to Alt+Page Down.

* Set OBS to always start at windows startup.

* Set the directories for the following in helpers.py : dateFile, videoFilePath, bakkesMod.

* Open config.py and add the .exe filename for the game you would like to enable recording for.

* Finally, set this python command to execute at startup using a .bat file or Windows Task SCheduler.


```sh
python Auto_OBS_Recorder.py
```

## Author

👤 **nasty_jack**

* Github: [@NastyJack](https://github.com/NastyJack)

## Show your support

Give a ⭐️ if this project helped you!

***
