import sys
if sys.platform != "win32":
    import uvloop
    uvloop.install()

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Ego(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="EgoMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        # Resolve LOG_GROUP_ID if it's a username
        log_chat_id = config.LOG_GROUP_ID
        if isinstance(config.LOG_GROUP_ID, str) and config.LOG_GROUP_ID.startswith('@'):
            try:
                chat = await self.get_chat(config.LOG_GROUP_ID)
                log_chat_id = chat.id
                LOGGER(__name__).info(f"Resolved log group username {config.LOG_GROUP_ID} to ID: {log_chat_id}")
            except Exception as ex:
                LOGGER(__name__).error(f"Failed to resolve log group username {config.LOG_GROUP_ID}: {ex}")
                exit()

        try:
            await self.send_message(
                chat_id=log_chat_id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(log_chat_id, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        
        # Store the resolved chat ID for other parts of the application
        config.LOG_GROUP_ID = log_chat_id
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
