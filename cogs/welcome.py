import discord
from discord.ext import commands
from config import Config

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(Config.WELCOME_CHANNEL_ID)
        if not channel: return

        embed = discord.Embed(
            title=f"Welcome to Summit Works, {member.display_name}!",
            description=f"Great to have you here, {member.mention}.\n\nLooking for a custom build? Use `/apply` to get started with our team.",
            color=Config.PRIMARY_COLOR
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=Config.BANNER_URL)
        embed.set_footer(text=Config.FOOTER_TEXT)

        await channel.send(content=member.mention, embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))