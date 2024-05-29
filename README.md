# YouTube Downloader Bot

This is a professional YouTube downloader bot written in Python. It uses the `telebot` library to interact with users
via Telegram and the `pytube` library to download YouTube videos and audio.

## Features

- Download YouTube videos in various formats and resolutions.
- Extract audio from YouTube videos.
- Easy-to-use Telegram interface.
- Premium and free versions.
- Fast in performance
- And many more...

## Prerequisites

- Python 3.10+
- A Telegram bot token from BotFather
- Required Python main libraries:
    - `pyTelegramBotAPI` (telebot)
    - `pytube`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DiarTor/DiTube.git
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot:
    - Talk to [BotFather](https://core.telegram.org/bots#botfather) to create a new bot and get your bot token.
    - Replace `YOUR_BOT_TOKEN` in the script with your actual bot token.
    - To replace the bot token you should create this path `config/token.py` and inside this file you should create a
      variable called `bot_token` and place your token there as a string

## Usage

1. Run the bot:
   ```bash
   python main.py
   ```

2. Start a conversation with your bot on Telegram.

3. Use the following commands and instructions to interact with the bot:
    - `/start`: Welcome message and instructions.
    - `/ahelp`: List of available admin commands.
    - You Can use the Bot buttons for more use
    

## Example

Here's an example of how to use the bot:

1. Send `/start` to the bot:
2. Send the link of Youtube video you want to download
3. Choose a method via InlineButtons
4. Done.

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have feature requests.


## Acknowledgments

- [Telebot (pyTelegramBotAPI)](https://github.com/eternnoir/pyTelegramBotAPI)
- [Pytube](https://github.com/nficano/pytube)
- [YouTube](https://www.youtube.com)

---

*Warning: Downloading videos from YouTube might violate their terms of service. Please ensure that you have the right to
download the content before using this bot.*

*Note: There is no gateway connected to the bot so basiclly the premium version can not be baught automaticlly but manuly*
