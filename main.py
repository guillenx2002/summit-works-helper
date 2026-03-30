import discord
import asyncio
from discord.ext import commands
from config import Config

class SummitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Required for Welcome system
        intents.message_content = True # Good practice to keep this enabled
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Load Cogs
        await self.load_extension('cogs.welcome')
        await self.load_extension('cogs.applications')
        await self.load_extension('cogs.fivem') # <--- ADDED THIS LINE
        
        # Sync Slash Commands
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        # Updated status to reflect both commands
        await self.change_presence(activity=discord.Game(name="Summit Works | /dayzapply & /fivemapply"))

bot = SummitBot()
bot.run(Config.TOKEN)