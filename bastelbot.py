import os

from dotenv import load_dotenv
from twitchio.ext import commands


class Bot(commands.Bot):
    load_dotenv()

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.getenv('TOKEN'), prefix='?', initial_channels=['viertelwissen'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            print(f'Nachricht vom Bot {message.content}!')
            return

        # Print the contents of our message to console...
        print(f'{message.author.display_name}: {message.content}')
        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...

        if message.content.startswith('?'):
            print("Befehl ausgelöst!")

        await self.handle_commands(message)


bot = Bot()
bot.run()
