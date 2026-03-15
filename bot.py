import requests
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8764715379:AAFGyL47vhCroLo4umgbVLUUY6LDl38V-JI"

tasks = {}

def generate_username(mode):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"

    if mode == "1":
        return random.choice(chars)+"_"+random.choice(chars)+"_"+random.choice(chars)

    elif mode == "2":
        return random.choice(chars)+"__"+random.choice(chars)+"_"+random.choice(chars)

    elif mode == "3":
        return random.choice(chars)+"_"+random.choice(chars)+"_"+random.choice(chars)+"_"+random.choice(chars)

    elif mode == "4":
        return "".join(random.choice(chars) for _ in range(5))

    elif mode == "5":
        return "".join(random.choice(chars) for _ in range(6))


def check_username(username):
    try:
        url = f"https://fragment.com/username/{username}"
        headers = {"User-Agent":"Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)

        if "is not available" in r.text:
            return False
        return True

    except:
        return False


async def scanner(chat_id, mode, context):

    while True:

        username = generate_username(mode)

        if check_username(username):
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"""

𝗨𝗦𝗘𝗥

➜ @{username}
"""
            )

        await asyncio.sleep(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗨𝗦𝗘𝗥

𝗖𝗵𝗼𝗼𝘀𝗲 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗧𝘆𝗽𝗲

➊ ➜ 𝗮_𝗯_𝗰
➋ ➜ 𝗮__𝗯_𝗰
➌ ➜ 𝗮_𝗯_𝗰_𝗱
➍ ➜ 𝗮𝗯𝗰𝗱𝗲
➎ ➜ 𝗮𝗯𝗰𝗱𝗲𝗳

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(text)


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mode = update.message.text
    chat_id = update.effective_chat.id

    if mode not in ["1","2","3","4","5"]:
        return

    await update.message.reply_text("𝗦𝗰𝗮𝗻𝗻𝗶𝗻𝗴 𝘀𝘁𝗮𝗿𝘁𝗲𝗱... 𝘀𝗲𝗻𝗱 /stop 𝘁𝗼 𝘀𝘁𝗼𝗽")

    task = asyncio.create_task(scanner(chat_id, mode, context))
    tasks[chat_id] = task


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id in tasks:
        tasks[chat_id].cancel()
        del tasks[chat_id]

    await update.message.reply_text("𝗦𝗰𝗮𝗻𝗻𝗶𝗻𝗴 𝘀𝘁𝗼𝗽𝗽𝗲𝗱")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(MessageHandler(filters.TEXT, choose))

print("Bot running...")

app.run_polling()