import discord
from discord import app_commands
from discord.ext import commands
from config import Config 

# --- The view that shows the "Add Image" button ---
class ImageUploadView(discord.ui.View):
    def __init__(self, thread_url):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="📸 Click Here to Add Images", url=thread_url))

class FiveMSubmissionModal(discord.ui.Modal):
    def __init__(self, build_type):
        super().__init__(title=f"FiveM Submission: {build_type}")
        self.build_type = build_type

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
        default="FiveM",
        max_length=50,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 1. Get channels from config
        channel_id = Config.FIVEM_MAP.get(self.build_type)
        channel = interaction.guild.get_channel(channel_id)
        master_log = interaction.guild.get_channel(Config.LEAD_LOG_CHANNEL_ID)
        discussion_root = interaction.guild.get_channel(Config.DISCUSSION_CHANNEL_ID)

        # 2. Create the Summary Embed
        embed = discord.Embed(
            title=f"🏙️ New FiveM {self.build_type} Request",
            color=0xFF0044 
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Type", value=self.build_type, inline=True)
        embed.add_field(name="Price", value=f"${self.price.value}" if self.price.value != "0" else "Free", inline=True)
        embed.add_field(name="Details", value=self.details.value, inline=False)
        embed.set_footer(text=Config.FOOTER_TEXT)

        # 3. Create PUBLIC Thread
        thread = await discussion_root.create_thread(
            name=f"FiveM: {interaction.user.display_name} - {self.build_type}",
            type=discord.ChannelType.public_thread 
        )
        await thread.add_user(interaction.user)
        
        await thread.send(content=f"**Official FiveM Request Details for {interaction.user.mention}:**", embed=embed)
        await thread.send("Please **upload your reference images, pack files, or screenshots** here for everyone to see!")

        # 4. Send the Logs
        log_msg = f"✅ **FiveM Public Thread Created:** {thread.jump_url}"
        if channel: 
            await channel.send(content=log_msg, embed=embed)
        if master_log: 
            await master_log.send(content=log_msg, embed=embed)

        # 5. Response to user
        view = ImageUploadView(thread.jump_url)
        await interaction.response.send_message(
            "### ✅ FiveM Application Sent!\nYour public project thread has been created. Click below to add images.",
            view=view,
            ephemeral=True
        )

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