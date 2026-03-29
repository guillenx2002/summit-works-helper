import discord
from discord import app_commands
from discord.ext import commands
from config import Config

class AppModal(discord.ui.Modal):
    def __init__(self, category):
        super().__init__(title=f"{category} Build Request")
        self.category = category
        
        self.desc = discord.ui.TextInput(label="Build Description", style=discord.TextStyle.paragraph, placeholder="Tell us exactly what you need...")
        self.budget = discord.ui.TextInput(label="Budget Range", placeholder="e.g. $200 - $500", max_length=50)
        self.timeline = discord.ui.TextInput(label="Desired Timeline", placeholder="e.g. 2 weeks", max_length=50)
        
        self.add_item(self.desc)
        self.add_item(self.budget)
        self.add_item(self.timeline)

    async def on_submit(self, interaction: discord.Interaction):
        # Create the Lead Embed
        embed = discord.Embed(title="🚀 New Lead Received", color=Config.PRIMARY_COLOR)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Service", value=self.category, inline=True)
        embed.add_field(name="Budget", value=self.budget.value, inline=True)
        embed.add_field(name="Timeline", value=self.timeline.value, inline=True)
        embed.add_field(name="Details", value=self.desc.value, inline=False)
        embed.set_footer(text=f"User ID: {interaction.user.id}")

        log_channel = interaction.guild.get_channel(Config.LEAD_LOG_CHANNEL_ID)
        await log_channel.send(embed=embed)
        await interaction.response.send_message("Application sent! Our team will contact you soon.", ephemeral=True)

class AppButtons(discord.ui.View):
    @discord.ui.button(label="DayZ Build", style=discord.ButtonStyle.primary)
    async def dayz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AppModal("DayZ"))

    @discord.ui.button(label="FiveM Build", style=discord.ButtonStyle.primary)
    async def fivem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AppModal("FiveM"))

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Start a custom build request")
    async def apply(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Summit Works | Build Application",
            description="Select the platform you need a custom build for to begin.",
            color=Config.PRIMARY_COLOR
        )
        await interaction.response.send_message(embed=embed, view=AppButtons(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Applications(bot))