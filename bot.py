from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot, os, uuid
from dotenv import load_dotenv

# Load token
load_dotenv("token.env.txt")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("veronicaabot")  # ganti dengan username bot kamu

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN tidak ditemukan!")

bot = telebot.TeleBot(BOT_TOKEN)

# Simpan data unik
media_data = {}

# Handler upload foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    unique_code = str(uuid.uuid4())[:8]
    bot_link = f"https://t.me/{BOT_USERNAME}?start={unique_code}"

    media_data[unique_code] = {
        "type": "photo",
        "file_id": file_id,
        "file_url": file_url,
        "bot_link": bot_link
    }

    caption = f"📸 Foto yang kamu kirim.\n\n👉 Klik link berikut untuk melanjutkan:\n{bot_link}"
    bot.send_message(message.chat.id, caption)

# Handler upload video
@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    unique_code = str(uuid.uuid4())[:8]
    bot_link = f"https://t.me/{BOT_USERNAME}?start={unique_code}"

    media_data[unique_code] = {
        "type": "video",
        "file_id": file_id,
        "file_url": file_url,
        "bot_link": bot_link
    }

    caption = f"🎥 Video yang kamu kirim.\n\n👉 Klik link berikut untuk melanjutkan:\n{bot_link}"
    bot.send_message(message.chat.id, caption)

# Handler link unik (/start kode)
@bot.message_handler(commands=['start'])
def start_handler(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        kode = parts[1]

        if kode in media_data:
            data = media_data[kode]
            bot_link = data["bot_link"]

            # Buat tombol
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton("🔗 Join Dulu", url="https://t.me/livestreamingbolaaaaa"),
                InlineKeyboardButton("▶️ Coba Lagi", url=bot_link)
            )

            # --- MODE FLEXIBEL ---
            mode = "caption"  # ubah ke "media" kalau mau media + tombol

            if mode == "media":
                if data["type"] == "photo":
                    bot.send_photo(
                        message.chat.id, data["file_url"],
                        caption="📸 Foto lagi.. klik tombol di bawah 👇",
                        reply_markup=markup
                    )
                elif data["type"] == "video":
                    bot.send_video(
                        message.chat.id, data["file_url"],
                        caption="🎥 Video lagi.. klik tombol di bawah 👇",
                        reply_markup=markup
                    )
            else:  # hanya caption + tombol
                bot.send_message(
                    message.chat.id,
                    text=f"👉 Klik link berikut untuk melanjutkan:\n{bot_link}",
                    reply_markup=markup
                )

        else:
            bot.send_message(message.chat.id, "❌ Link sudah tidak berlaku.")
    else:
        bot.send_message(message.chat.id, "👋 Halo! Selamat datang di bot 🙂")

print("🤖 Bot sedang berjalan nich...")
bot.infinity_polling()
