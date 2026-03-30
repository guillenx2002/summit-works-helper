import discord
from discord import app_commands
from discord.ext import commands
from config import Config

class FiveMSubmissionModal(discord.ui.Modal):
    def __init__(self, build_type):
        super().__init__(title=f"FiveM Submission: {build_type}")
        self.build_type = build_type

    # Using the same 3 questions you requested
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
        default="FiveM", # Pre-filled for convenience
        max_length=50,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 1. Get the FiveM specific channel
        channel_id = Config.FIVEM_MAP.get(self.build_type)
        channel = interaction.guild.get_channel(channel_id)
        master_log = interaction.guild.get_channel(Config.LEAD_LOG_CHANNEL_ID)

        embed = discord.Embed(
            title=f"🏙️ New FiveM {self.build_type} Request",
            color=0xFF0044 # A different color to distinguish from DayZ
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Type", value=self.build_type, inline=True)
        embed.add_field(name="Price", value=f"${self.price.value}" if self.price.value != "0" else "Free", inline=True)
        embed.add_field(name="Details", value=self.details.value, inline=False)
        embed.set_footer(text=Config.FOOTER_TEXT)

        if channel:
            await channel.send(embed=embed)
        if master_log:
            await master_log.send(embed=embed)

        await interaction.response.send_message(f"Your FiveM {self.build_type} request has been submitted!", ephemeral=True)

class FiveMSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="What kind of FiveM build are you submitting?",
        options=[
            discord.SelectOption(label="Hood Pack", description="Custom territory/hood designs"),
            discord.SelectOption(label="Custom City", description="Full city overhauls or MLOs"),
            discord.SelectOption(label="Gun Pack", description="Custom weapon models and skins"),
            discord.SelectOption(label="Sound Pack", description="Custom engine or weapon sounds"),
            discord.SelectOption(label="Car Pack", description="Imported vehicle packs"),
            discord.SelectOption(label="Store Pack", description="Interior store/shop designs")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(FiveMSubmissionModal(select.values[0]))

class FiveMApplications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fivemapply", description="Start your FiveM build submission")
    async def fivemapply(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Welcome to **Summit Works | FiveM Division**. Select your category below:",
            view=FiveMSelectionView(),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(FiveMApplications(bot))