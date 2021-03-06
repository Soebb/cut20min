import os, datetime, glob, subprocess, json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import keyboard as kb
import pygetwindow as gw

win = gw.getActiveWindow()

BOT_TOKEN = " "
API_ID = " "
API_HASH = " "

Bot = Client(
    ":memory:",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

refresh_button = [
    InlineKeyboardButton(
        text='Refresh List',
        callback_data='refresh'
    )
]

msgid = 0
chatid = 0

@Bot.on_message(filters.command(['resume']) & filters.private)
async def edame(client, message):
    win.activate()
    kb.press_and_release('enter')
    await message.reply('resumed.')

@Bot.on_message(filters.command(['stop']) & filters.private)
async def estop(client, message):
    win.activate()
    kb.press_and_release('pause')
    await message.reply('stoped. to resume send /resume')

@Bot.on_message(filters.command(['cancel']) & filters.private)
async def kansel(client, message):
    await message.reply('canceled.')
    exit(0)

@Bot.on_message(filters.text & ~filters.regex('/previous'))
async def start(bot, m):
    keyboard = []
    keyboard.append(refresh_button)
    try:
        for file in glob.glob('C:/dlmacvin/1aa/*'):
            if file.endswith(('.ts', '.mp4', '.mkv')):
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=file.rsplit('/', 1)[1].replace('1aa\\', ''),
                            callback_data=file.rsplit('/', 1)[1].replace('1aa\\', '')
                        )
                    ]
                )
    except Exception as e:
        print(e)
        return
    keyboard.append(refresh_button)
    #await bot.send_message(chat_id=id, text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))
    await m.reply_text(text="Which one?", reply_markup=InlineKeyboardMarkup(keyboard))


@Bot.on_callback_query()
async def callback(bot, update):
    global chatid, msgid
    if update.data == "refresh":
        keyboard = []
        keyboard.append(refresh_button)
        try:
            for file in glob.glob('C:/dlmacvin/1aa/*'):
                if file.endswith(('.ts', '.mp4', '.mkv')):
                    keyboard.append(
                        [
                            InlineKeyboardButton(
                                text=file.rsplit('/', 1)[1].replace('1aa\\', ''),
                                callback_data=file.rsplit('/', 1)[1].replace('1aa\\', '')
                            )
                        ]
                    )
        except Exception as e:
            print(e)
            return
        keyboard.append(refresh_button)
        try:
            await update.message.edit(text=f"Which one of these {len(keyboard)} videos?", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await update.message.reply_text("error!! Send /start")
        return
    try:
        name = update.data
        input = 'C:/dlmacvin/1aa/' + name
        process_msg = await update.message.reply_text('Processing..\nFor cancel send /cancel\nFor stop send /stop')
        ext = '.' + name.rsplit('.', 1)[1]
        out = 'C:/dlmacvin/1aa/videos/'+name
        os.system(f'''ffmpeg -ss 00:00:00 -i "{input}" -to 00:20:00 -c copy -y "{out}"''')
        await process_msg.delete()
        if chatid == 0:
            msg = await update.message.reply_text('Done! ' + out)
            msgid = msg.message_id
        elif chatid != 0:
            try:
                await bot.edit_message_text(update.message.chat.id, msgid, 'Done! ' + out)
            except:
                await bot.edit_message_text(update.message.chat.id, msgid, '????????')
        chatid = update.message.from_user.id

    except:
        pass



Bot.run()
