import os

import ffmpeg
from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import MusicPlayer, app
from Vivek.utils.functions import S12K, Vivek
from Vivek.utils.queue import Queue



@app.on_message(filters.sudo & filters.command("end"))
async def audio_play(client, message):
    chat_id = message.chat.id
    await MusicPlayer.leave_call(chat_id)
    await Queue.clear(chat_id)
    await Vivek.remove_active_chat(chat_id)