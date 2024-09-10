import os

import ffmpeg
from pyrogram import filters

from config import LOG_GROUP_ID
from Vivek import MusicPlayer, app
from Vivek.utils.functions import S12K, MelodyError, Vivek
from Vivek.utils.queue import Queue


@app.on_message(filters.chat(LOG_GROUP_ID) & (filters.audio | filters.voice))
async def audio_play(client, message):
    mystic = await message.reply_text("processing")

    if message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name
        duration_min = message.audio.duration
    if message.voice:
        file_id = message.voice.file_id
        duration_min = message.voice.duration
        file_name = f"{message.voice.file_unique_id}.ogg"

    file_path = os.path.join("downloads", file_name)
    user_name = "🤗"
    video = False
    a = await app.download_media(file_id)

    (
        ffmpeg.input(a)
        .filter("volume", "18dB")
        .output(file_path)
        .overwrite_output()
        .run()
    )
    chat_id = S12K()
    title = "Playing Local Audio/Voice"

    if await Vivek.is_active_chat(chat_id):
        await Queue.add(
            chat_id,
            title=title,
            duration=duration_min,
            vidid=None,
            video=video,
            file_path=file_path,
            by=user_name,
        )
        count = len(await Queue.get_queues(chat_id)) - 1
        return await mystic.edit(
            f"<b>Added To Queue At {count}</b>\n<b>Title:</b> {title}\n<b>Duration</b>: {duration_min} seconds\n<b>By</b>: {user_name}",
            disable_web_page_preview=True,
        )

    try:
        await MusicPlayer.play(message.chat.id, file_path, video)
    except MelodyError as e:
        return await mystic.edit(e)
    except Exception as e:
        return await mystic.edit(e)
    await Queue.add(
        chat_id,
        title=title,
        duration=duration_min,
        vidid=None,
        video=video,
        file_path=file_path,
        by=user_name,
    )

    await Vivek.add_active_chat(message.chat.id)
    await mystic.edit("Started Playing")
    os.remove(a)


@app.on_message(filters.sudo & filters.command("playhere"))
async def audio_play(client, message):
    S12K(message.chat.id)
    await message.reply_text(
        "Now All recieved audio/voice has been playing here from since Now"
    )
