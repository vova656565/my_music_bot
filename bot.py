import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

API_ID = 22065063
API_HASH = "572cf32195764334161ada616ef74ea0"
BOT_TOKEN = "7918443528:AAGeuD5vBAHza2G5k8iqGgK4_0Q0aX9SQZ0"

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Путь к ffmpeg
FFMPEG_PATH = r"C:\Users\Cassian Comp\Downloads\ffmpeg-7.1.1-essentials_build (2)\ffmpeg-7.1.1-essentials_build\bin"

@app.on_message(filters.text & ~filters.command("start"))
async def music_downloader(client, message):
    query = message.text.strip()
    msg = await message.reply("🔍 Ищу и скачиваю музыку...")

    filename = f"{query}.mp3"
    webm_file = None

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': f'{query}.%(ext)s',
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch:{query}"])

        # Проверим наличие mp3
        if os.path.exists(filename):
            await message.reply_audio(audio=filename, title=query)
            os.remove(filename)  # Удаляем mp3

        # Ищем и удаляем webm
        for file in os.listdir():
            if file.endswith(".webm") and query.lower() in file.lower():
                webm_file = file
                os.remove(webm_file)

        await msg.delete()
    except Exception as e:
        await msg.edit(f"⚠️ Ошибка: {str(e)}")

app.run()

