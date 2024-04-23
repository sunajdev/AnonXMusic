from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def autodelete_markup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🕒 3s",
                    callback_data=f"AutoDelete {chat_id}|3",
                ),
                InlineKeyboardButton(
                    text="🕓 5s",
                    callback_data=f"AutoDelete {chat_id}|5",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["P_B_4"],
                    callback_data=f"AutoDelete {chat_id}|1",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🕤 10s",
                    callback_data=f"AutoDelete {chat_id}|10",
                ),
                InlineKeyboardButton(
                    text="🕛 15s",
                    callback_data=f"AutoDelete {chat_id}|15",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl
