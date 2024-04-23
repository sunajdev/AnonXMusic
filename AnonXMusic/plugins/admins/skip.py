from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from AnonXMusic import YouTube, app
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import db
from AnonXMusic.utils.database import get_loop
from AnonXMusic.utils.decorators import AdminRightsCheck
from AnonXMusic.utils.inline import close_markup, stream_markup
from AnonXMusic.utils.stream.autoclear import auto_clean
from AnonXMusic.utils.thumbnails import get_thumb
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(
    filters.command(["skip", "cskip", "next", "cnext"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    if not len(message.command) < 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            mystic = await message.reply_text(_["admin_8"])
            await delete_message(chat_id, mystic.id)
            return
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                mystic = await message.reply_text(_["admin_12"])
                                await delete_message(chat_id, mystic.id)
                                return 
                            if popped:
                                await auto_clean(popped)
                            if not check:
                                try:
                                    mystic = await message.reply_text(
                                        text=_["admin_6"].format(
                                            message.from_user.mention,
                                            message.chat.title,
                                        ),
                                        reply_markup=close_markup(_),
                                    )
                                    await delete_message(chat_id, mystic.id)
                                    await Anony.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        mystic = await message.reply_text(_["admin_11"].format(count))
                        await delete_message(chat_id, mystic.id)
                        return 
                else:
                    mystic = await message.reply_text(_["admin_10"])
                    await delete_message(chat_id, mystic.id)
                    return 
            else:
                mystic = await message.reply_text(_["queue_2"])
                await delete_message(chat_id, mystic.id)
                return 
        else:
            mystic = await message.reply_text(_["admin_9"])
            await delete_message(chat_id, mystic.id)
            return 
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                mystic = await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                await delete_message(chat_id, mystic.id)
                try:
                    return await Anony.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                mystic = await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                await delete_message(chat_id, mystic.id)
                return await Anony.stop_stream(chat_id)
            except:
                return
    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    status = True if str(streamtype) == "video" else None
    db[chat_id][0]["played"] = 0
    exis = (check[0]).get("old_dur")
    if exis:
        db[chat_id][0]["dur"] = exis
        db[chat_id][0]["seconds"] = check[0]["old_second"]
        db[chat_id][0]["speed_path"] = None
        db[chat_id][0]["speed"] = 1.0
    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            mystic = await message.reply_text(_["admin_7"].format(title))
            await delete_message(chat_id, mystic.id)
            return 
        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None
        try:
            await Anony.skip_stream(chat_id, link, video=status, image=image)
        except:
            mystic = await message.reply_text(_["call_6"])
            await delete_message(chat_id, mystic.id)
            return 
        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                f"https://t.me/{app.username}?start=info_{videoid}",
                title[:23],
                check[0]["dur"],
                user,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    elif "vid_" in queued:
        mystic = await message.reply_text(_["call_7"], disable_web_page_preview=True)
        try:
            file_path, direct = await YouTube.download(
                videoid,
                mystic,
                videoid=True,
                video=status,
            )
        except:
            await mystic.edit_text(_["call_6"])
            await delete_message(chat_id, mystic.id)
            return 
        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None
        try:
            await Anony.skip_stream(chat_id, file_path, video=status, image=image)
        except:
            await mystic.edit_text(_["call_6"])
            await delete_message(chat_id, mystic.id)
            return 

        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid)
        run = await message.reply_photo(
            photo=img,
            caption=_["stream_1"].format(
                f"https://t.me/{app.username}?start=info_{videoid}",
                title[:23],
                check[0]["dur"],
                user,
            ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()
    elif "index_" in queued:
        try:
            await Anony.skip_stream(chat_id, videoid, video=status)
        except:
            mystic = await message.reply_text(_["call_6"])
            await delete_message(chat_id, mystic.id)
            return 
        button = stream_markup(_, chat_id)
        run = await message.reply_photo(
            photo=config.STREAM_IMG_URL,
            caption=_["stream_2"].format(user),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
    else:
        if videoid == "telegram":
            image = None
        elif videoid == "soundcloud":
            image = None
        else:
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
        try:
            await Anony.skip_stream(chat_id, queued, video=status, image=image)
        except:
            mystic = await message.reply_text(_["call_6"])
            await delete_message(chat_id, mystic.id)
            return 
        if videoid == "telegram":
            button = stream_markup(_, chat_id)
            run = await message.reply_photo(
                photo=config.TELEGRAM_AUDIO_URL
                if str(streamtype) == "audio"
                else config.TELEGRAM_VIDEO_URL,
                caption=_["stream_1"].format(
                    config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif videoid == "soundcloud":
            button = stream_markup(_, chat_id)
            run = await message.reply_photo(
                photo=config.SOUNCLOUD_IMG_URL
                if str(streamtype) == "audio"
                else config.TELEGRAM_VIDEO_URL,
                caption=_["stream_1"].format(
                    config.SUPPORT_CHAT, title[:23], check[0]["dur"], user
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            button = stream_markup(_, chat_id)
            img = await get_thumb(videoid)
            run = await message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
