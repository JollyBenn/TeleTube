# TeleTube
<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/JollyBenn/TeleTube"> [![license](https://img.shields.io/github/license/JollyBenn/teletube.svg?style=flat-square&maxAge=2592000&label=License)](https://raw.githubusercontent.com/JollyBenn/teletube/master/LICENSE)

**TeleTube** Is simple telegram bot for downloading high quality videos from youtube

## 📦 Installing
#### 1. Install latest version of Python
- Go to the [official Python website](https://www.python.org/downloads/)
- Press on `Download Python`
- Install it

#### 2. Open Command Prompt
- If you are working in Window, then this can be done with the keyboard shortcut `Win` + `R`.
- Next, you need to install the necessary libraries, to do this, run the following commands.

```console
pip install requests
```

```code
pip install pyTelegramBotAPI
```
#### 3. Bot installation
- Downloading the bot file `bot.py`
*That's all for installation, let's move on 😄*

## 🔨 Setup
*Now let's get down to setting up the bot itself.*
> Open file bot.py we see the main settings of the bot
```python
token = 'TOKEN' # telegram bot api, read more: https://core.telegram.org/api
download_delay = 10 # delay for download video
timeout = 5 # timeout for load page
localstore = {} # data store
lang = 'eng' # set lang, default: uk - Ukrainian, eng - English
locales = {} # langs
```
Let's go through each item

`TOKEN` in order for the bot to start you need to get your token, how to get it you can find out [here](https://core.telegram.org/api)

`download_delay` why not payload the bot, and not check every second whether the video loaded or not, there was add delay

`timeout` Normal delay for page load

`lang` the parameter is responsible for the language pack, English and Ukrainian are set by default, but no one bothers to add your own

`locales` place where language packs are stored

## Bot launch
- Open Command Prompt
- Go to the folder where the file is found `bot.py`
```console
cd PATH_TO_FOLDER
```
- After that just run the file
```console
python bot.py
```

## Donate
<a href="https://www.buymeacoffee.com/jollybenn" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
