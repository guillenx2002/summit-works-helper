import discord
from discord import app_commands
from discord.ext import commands
from config import Config # Ensure this matches your config class name

class BuildSubmissionModal(discord.ui.Modal):
    def __init__(self, build_type):
        super().__init__(title=f"Submit: {build_type}")
        self.build_type = build_type

    # --- The 3 Specific Questions ---
    details = discord.ui.TextInput(
        label="Describe your build in deep details",
        style=discord.TextStyle.paragraph,
        placeholder="Provide as much detail as possible...",
        required=True
    )
    
    price = discord.ui.TextInput(
        label="What is the price? (If free, type 0)",
        placeholder="e.g. 50 or 0",
        max_length=10,
        required=True
    )
    
    platform = discord.ui.TextInput(
        label="Which platform will this be on?",
        placeholder="e.g. DayZ, FiveM, PC, etc.",
        max_length=50,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 1. Get the right channel from Config
        channel_id = Config.CHANNEL_MAP.get(self.build_type)
        channel = interaction.guild.get_channel(channel_id)
        
        # 2. Get the Master Log channel
        master_log = interaction.guild.get_channel(Config.LEAD_LOG_CHANNEL_ID)

        embed = discord.Embed(
            title=f"🛠️ New {self.build_type} Submission",
            color=Config.PRIMARY_COLOR
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Platform", value=self.platform.value, inline=True)
        embed.add_field(name="Price", value=f"${self.price.value}" if self.price.value != "0" else "Free", inline=True)
        embed.add_field(name="Details", value=self.details.value, inline=False)
        embed.set_footer(text=Config.FOOTER_TEXT)

        # Send to the specific category channel
        if channel:
            await channel.send(embed=embed)
        
        # Send a copy to the Master Log
        if master_log:
            await master_log.send(embed=embed)

        await interaction.response.send_message(f"Thanks! Your {self.build_type} has been submitted.", ephemeral=True)

class BuildSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="What kind of build would you like to be submitting today?",
        options=[
            discord.SelectOption(label="Bunker", description="Submit a custom bunker build"),
            discord.SelectOption(label="Store", description="Submit a store/shop layout"),
            discord.SelectOption(label="Custom Build", description="A unique premium project"),
            discord.SelectOption(label="Bases", description="Clan or player base designs")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Open the modal based on what they picked in the dropdown
        await interaction.response.send_modal(BuildSubmissionModal(select.values[0]))

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Start your build submission")
    async def apply(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Welcome to **Summit Works**. Please use the menu below to start.",
            view=BuildSelectionView(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Applications(bot))