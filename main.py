import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp as ytdlp
import os
import uuid
import re

# Assign provided values
bot_token = '6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU'
api_id = '10471716'
api_hash = 'f8a1b21a13af154596e2ff5bed164860'


# Initialize the Pyrogram client
app = Client("yt_dlp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Handler for /start command
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Welcome to the YouTube Video Downloader Bot! Send me a YouTube link and I'll download the video for you.")

# Handler for messages containing YouTube links
@app.on_message(filters.regex(r"(http(s)?://)?(www\.)?(youtube\.com|youtu\.be)/.+"))
def download_video(client, message: Message):
    try:
        video_url = message.text
        with ytdlp.YoutubeDL() as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', None)
            if title:
                message.reply_text(f"Downloading: {title}")
                unique_id = uuid.uuid4().hex
                # Remove special characters from title
                filename = "video.mp4"
                ydl.download([video_url])
                print(f"Video downloaded ⚠   file path= {filename}")

                if os.path.exists(filename):
                    message.reply_video(video=filename, caption=title)
                    os.remove(filename)
                    print("video sent")
            else:
                message.reply_text("Error: Unable to fetch video information.")
    except Exception as e:
        error_message = f"Error: Failed to download the video. Details: {str(e)}\n\n{traceback.format_exc()}"
        message.reply_text(error_message)

# Error handler
@app.on_message(filters.private)
def error_handler(client, message):
    message.reply_text("Sorry, I can only process YouTube links.")

# Run the bot
app.run()
