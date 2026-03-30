import discord
from discord import app_commands
from discord.ext import commands
import config

class BuildModal(discord.ui.Modal, title="Submit Your Build Details"):
    description = discord.ui.TextInput(label="Project Description", style=discord.TextStyle.paragraph, placeholder="Tell us about your vision...")
    budget = discord.ui.TextInput(label="Budget", placeholder="e.g. $50 - $100", max_length=50)
    timeline = discord.ui.TextInput(label="Timeline", placeholder="How soon do you need it?", max_length=50)

    def __init__(self, build_type):
        super().__init__()
        self.build_type = build_type

    async def on_submit(self, interaction: discord.Interaction):
        # Find the right channel from our config map
        channel_id = config.CHANNEL_MAP.get(self.build_type)
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message(f"Error: Channel for {self.build_type} not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🆕 New {self.build_type} Request",
            color=discord.Color.green()
        )
        embed.add_field(name="Client", value=interaction.user.mention, inline=True)
        embed.add_field(name="Build Type", value=self.build_type, inline=True)
        embed.add_field(name="Budget", value=self.budget.value, inline=False)
        embed.add_field(name="Timeline", value=self.timeline.value, inline=False)
        embed.add_field(name="Description", value=self.description.value, inline=False)
        embed.set_footer(text="Summit Works | Premium Custom Builds")

        await channel.send(embed=embed)
        await interaction.response.send_message(f"Your {self.build_type} application has been sent to our team!", ephemeral=True)

class BuildButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Bunker", style=discord.ButtonStyle.primary)
    async def bunker(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuildModal("Bunker"))

    @discord.ui.button(label="Store", style=discord.ButtonStyle.primary)
    async def store(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuildModal("Store"))

    @discord.ui.button(label="Custom Build", style=discord.ButtonStyle.primary)
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuildModal("Custom Build"))

    @discord.ui.button(label="Bases", style=discord.ButtonStyle.primary)
    async def bases(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BuildModal("Bases"))

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Start a new build request")
    async def apply(self, interaction: discord.Interaction):
        view = BuildButtons()
        await interaction.response.send_message("What type of build are you looking for?", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Applications(bot))