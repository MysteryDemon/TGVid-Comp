import datetime
from helper.database import db


async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You R Banned!.. Contact @Snowball_Official 😝", quote=True)
            return
    await cmd.continue_propagation()
