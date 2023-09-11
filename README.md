# MiTube - YouTube Downloader Telegram Bot 🎥🤖

MiTube is a Telegram bot that allows users to easily download YouTube videos by sending the bot a YouTube link. Users can select their preferred language (Farsi or English), choose the video quality 📹🎧, and enjoy the convenience of downloading YouTube videos.

## Installation 🚀

To get started with MiTube, follow these simple installation steps:

1. Clone the repository :

   ```bash
   git clone https://github.com/DiarTor/MiTube.git

2. Install the project dependencies using requirements.txt:
    ```bash
    pip install -r requirements.txt

- Configure the database by editing the database.py file with your own database settings (i used mongodb(pymongo)).

- Replace the TOKEN in config.py with your own bot token.

Usage 📋

Using MiTube is a breeze :

 - Start the bot on Telegram 🚀.

 - Select your preferred language (Farsi or English) 🗣️.

 - Send a YouTube link to the bot 📨.

 - Choose the desired video quality 📹🎧.

The bot will process your request and provide you with a downloadable link to the video.
Dependencies 📦

Bot Commands 🤖

    /lang: Use this command to change the bot's language preferences.
    /help: Get a guide on how to use the bot.
    /donate: See the donation links for supporting the development of MiTube.
    /start: Start a new session.

Please remember to add these commands in BotFather for better usability.

Notes 📝

  - MiTube is designed for educational and personal use only. Please respect copyright and intellectual property rights when using this bot.

   - While MiTube strives to provide high-quality video downloads, the availability of video quality options may vary depending on YouTube's policies and the video itself.

   - MiTube is an open-source project developed by the community. Feel free to contribute to its development or report any issues you encounter.

   - To see administrator commands, please write /adminhelp.

   - Note: Please change the donation links located in the lang/persian and lang/english files to update the donation information as needed.

MiTube relies on the following Python libraries:

- python-telegram-bot : Python wrapper for the Telegram Bot API.
- pymongo : Python driver for MongoDB, used for database operations.
- pytube : A lightweight, dependency-free Python library for downloading YouTube videos.

Contact 📞

If you have any questions or need assistance with MiTube, you can reach out to the developer:

- Telegram: https://t.me/diartor 💬
- Instagram: https://instagram.com/diartor 📷

Feel free to report any issues or suggest improvements. Thank you for using MiTube! 😊👍
