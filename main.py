from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp as ytdlp
import os

# Initialize the Pyrogram client
api_id = "10471716"
api_hash = "f8a1b21a13af154596e2ff5bed164860"
bot_token = "6999401413:AAHgF1ZpUsCT5MgWX1Wky7GbegyeHvzi2AU"

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
                filename = f"{title}.mp4"
                ydl.download([video_url])
                if os.path.exists(filename):
                    message.reply_video(filename)
                    os.remove(filename)
                else:
                    message.reply_text("Error: Failed to download the video.")
            else:
                message.reply_text("Error: Unable to fetch video information.")
    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")

# Error handler
@app.on_message(filters.private)
def error_handler(client, message):
    message.reply_text("Sorry, I can only process YouTube links.")

# Run the bot
app.run()
