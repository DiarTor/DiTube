from urllib.error import HTTPError, URLError

import telebot
from bot.download_videos.get_video_information import get_video_options, get_only_filesize
from config.database import users_collection
from languages import persian
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class YouTubeVideoHandler:
    def handle_exceptions(self, response, msg_id=None):
        """
        Handle exceptions by sending an error response to the user.

        :param response: The error response message.
        :param msg_id: The message ID to which the response should be sent.
        """
        self.bot.send_message(self.chat_id, response, reply_to_message_id=msg_id)

    def get_video_options_sorted(self, yt):
        """
        Get and sort video options while handling exceptions.

        :param yt: The YouTube video object.

        :returns: A sorted list (by resolution) of video options.
        """
        try:
            video_options = get_video_options(yt)
            return sorted(video_options, key=lambda x: int(x.split()[0].split('p')[0]), reverse=True)
        except (AgeRestrictedError, HTTPError, URLError):
            if AgeRestrictedError:
                error_response = persian.age_restricted_exception
            else:
                error_response = persian.server_error
            self.handle_exceptions(error_response, msg_id=self.msg.message_id)
            return []

    def create_keyboard(self, video_options):
        """
        Create an inline keyboard for video options and audio download.

        :param video_options: List of video options.

        :returns: InlineKeyboardMarkup for video options and audio download.
        """
        kb = []
        for item in video_options:
            parts = item.split()
            if len(parts) == 2:
                quality, size = parts
                kb.append([InlineKeyboardButton(f"{quality} {size}",
                                                callback_data=f"{self.yt.video_id} {quality} {self.chat_id}")])

        audio_file_size = get_only_filesize(self.user_message_text)
        formatted_size = "{:.1f}".format(audio_file_size)

        if self.user_lang == "en":
            kb.append([InlineKeyboardButton(f"Download Audio ({formatted_size} MB)",
                                            callback_data=f"{self.yt.video_id} vc {self.chat_id}")])
        else:
            kb.append([InlineKeyboardButton(f"دانلود صدا ({formatted_size} MB)",
                                            callback_data=f"{self.yt.video_id} vc {self.chat_id}")])

        return InlineKeyboardMarkup(kb)

    def process_video(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """
        Process the YouTube video, send information message, and create an inline keyboard for user options.

        This function handles the entire process of processing a YouTube video message.
        """
        self.msg = msg
        self.bot = bot
        self.user = msg.from_user
        self.user_message_text = msg.text
        self.chat_id = msg.chat.id
        self.user_lang = users_collection.find_one({"user_id": self.user.id})["settings"]["language"]
        message_info = bot.send_message(self.chat_id, persian.getting_media_link_information,
                                        reply_to_message_id=msg.message_id)

        self.yt = YouTube(self.user_message_text)
        video_options = self.get_video_options_sorted(self.yt)
        if not video_options:
            return

        reply_markup = self.create_keyboard(video_options)
        bot.edit_message_text(text=persian.select_download_option, chat_id=self.chat_id, message_id=message_info.id,
                              reply_markup=reply_markup)
