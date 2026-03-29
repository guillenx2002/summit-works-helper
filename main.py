import discord
import asyncio
from discord.ext import commands
from config import Config

class SummitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Required for Welcome system
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Load Cogs
        await self.load_extension('cogs.welcome')
        await self.load_extension('cogs.applications')
        # Sync Slash Commands
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name="/apply | Summit Works"))

bot = SummitBot()
bot.run(Config.TOKEN)