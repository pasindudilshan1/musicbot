import telebot
import yt_dlp
import os
import threading

# Replace with your bot token
bot = telebot.TeleBot('7720525698:AAGW_QEIOjIQM4BkJQwTl5bUrWkeIMnXFaQ')

DOWNLOAD_DIR = 'downloads'  # Directory to save downloaded files
cancel_flag = False  # Flag to track cancellation requests

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


# Function to download audio or video from YouTube
def download_youtube_media(url, media_type):
    global cancel_flag
    cancel_flag = False  # Reset cancel flag for each download

    options = {
        'format': 'bestaudio' if media_type == 'mp3' else 'bestvideo+bestaudio',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if media_type == 'mp3' else []
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        # Hook to check for cancellation
        def progress_hook(d):
            if cancel_flag:
                raise Exception("Download canceled by user.")

        ydl.add_progress_hook(progress_hook)

        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if media_type == 'mp3':
            filename = filename.replace('.webm', '.mp3')  # Adjust for the MP3 extension

        return filename


# Command to cancel the ongoing process
@bot.message_handler(commands=['cancel'])
def cancel_process(message):
    global cancel_flag
    cancel_flag = True  # Set the flag to True to indicate cancellation
    bot.reply_to(message, "Download process has been canceled.")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Welcome! Send me a YouTube link and type /mp3, /mp4, or /instrument for your desired format. Type /cancel to cancel the current process.")


@bot.message_handler(func=lambda message: message.text.startswith('http'))
def handle_link(message):
    url = message.text
    bot.send_message(message.chat.id,
                     "Link received! Now type /mp3 for MP3, /mp4 for MP4 format, or /instrument for instrumental audio.")
    # Store the URL temporarily in user's chat
    bot.user_data = {'url': url}


@bot.message_handler(commands=['mp3', 'mp4', 'instrument'])
def handle_download_request(message):
    media_type = message.text[1:]  # 'mp3', 'mp4', or 'instrument'
    url = bot.user_data.get('url')  # Retrieve the stored URL

    if not url:
        bot.reply_to(message, "Please send a YouTube link first.")
        return

    def download_and_send():
        global cancel_flag
        try:
            # Download the media file
            file_path = download_youtube_media(url, media_type)
            if cancel_flag:
                return  # If canceled, do not send the file

            # Send the downloaded file back to the user
            if media_type == 'mp3':
                with open(file_path, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio)
            elif media_type == 'mp4':
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video)

            # Cleanup the downloaded file
            os.remove(file_path)
            cancel_flag = False  # Reset the flag after successful download

        except Exception as e:
            bot.reply_to(message, f"Failed to process the YouTube link: {e}")
            cancel_flag = False  # Reset the flag if there was an error

    # Start the download in a separate thread
    threading.Thread(target=download_and_send).start()


try:
    bot.infinity_polling()
except KeyboardInterrupt:
    print("Bot stopped.")
