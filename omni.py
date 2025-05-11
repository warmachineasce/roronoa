import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Telegram API credentials
api_id = 21124978
api_hash = '63f41b60df295e52b2a967e5f9c02977'
bot_username = '@roronoa_zoro_robot'  # Replace with actual bot username

# Your saved string session
string_session = '1BVtsOGwBuxQ5In8ERyQqJIBo83wNkXeJESEFclUwu6cUCb8EPs1eXwiTqNBtVOH-0XUBkonv3bKlIJTQrDi-ogohGBhmCexMMOhr2p0600Lgykw9j2fbUqcl9Vw_4r8HF5asfI_BqR8PkT5Gud1n8dFpXgtocox2BZwOBRH8UPz8IWiuZz_rHpFTLfEet82nGG5INS4bQigHID1OMARf01jJxvFzJJ98DjL8ikFde-DNM24BlS9wjbIbpYppzZ4uKz3Yd5xoTZmygzqXW40LPRwXDaMs7soYMgpYRdfrss33PW8qjJwFR13rpI_SuVHN6kZwdW71ardII6F8_cOFZV_S_vVx8t0='

class AutoFisher:
    def __init__(self):
        self.client = TelegramClient(StringSession(string_session), api_id, api_hash)
        self.fishing_event = asyncio.Event()

    async def start(self):
        await self.client.start()
        self.client.add_event_handler(self.handle_bot_message, events.NewMessage(from_users=bot_username))
        print("Started AutoFisher. Beginning fishing cycles...")

        while True:
            for i in range(12):
                print(f"[{i+1}/12] Sending /fish")
                await self.client.send_message(bot_username, "/fish")
                await asyncio.sleep(5)

                try:
                    await asyncio.wait_for(self.fishing_event.wait(), timeout=30)
                    self.fishing_event.clear()
                except asyncio.TimeoutError:
                    print("Timeout waiting for 'Are you ready?'")

                await asyncio.sleep(5)

            print("12 cycles complete. Waiting 26 minutes...")
            await asyncio.sleep(26 * 60)

    async def handle_bot_message(self, event):
        text = event.raw_text.lower()

        if "are you ready?" in text and event.buttons:
            print("Detected 'Are you ready?' — clicking Start Fishing.")
            await asyncio.sleep(2)
            await event.click(0)
            self.fishing_event.set()

        elif "already fishing" in text:
            print("Detected 'Already fishing' — retrying /fish in 5 seconds.")
            await asyncio.sleep(5)
            await self.client.send_message(bot_username, "/fish")


if __name__ == '__main__':
    auto_fisher = AutoFisher()
    asyncio.run(auto_fisher.start())
