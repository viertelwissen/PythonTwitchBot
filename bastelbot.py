import asyncio
import os

from dotenv import load_dotenv
from twitchAPI.chat import ChatMessage, Chat, ChatCommand
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


async def bla_command(cmd: ChatCommand):
    print("Command ausgelöst!")
    await cmd.send("YES MOIN! -> " + cmd.parameter)


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, USER_SCOPE)
    await helper.bind()
    # do things

    # create chat instance
    chat = await Chat(twitch, initial_channel=["viertelwissen", "dreiviertelwissen"])

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    # chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)

    # listen to channel subscriptions
    # chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation

    # you can directly register commands and their handlers, this will register the !reply command
    chat.register_command('bla', bla_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()

# lets run our setup
asyncio.run(run())
