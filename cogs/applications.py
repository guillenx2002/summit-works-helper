import discord
from discord import app_commands
from discord.ext import commands
from config import Config 

# --- The view that shows the "Add Image" button ---
class ImageUploadView(discord.ui.View):
    def __init__(self, thread_url):
        super().__init__(timeout=None)
        # Create a link button that goes straight to the private thread
        self.add_item(discord.ui.Button(label="📸 Click Here to Add Images", url=thread_url))

class BuildSubmissionModal(discord.ui.Modal):
    def __init__(self, build_type):
        super().__init__(title=f"Submit: {build_type}")
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
        placeholder="e.g. DayZ, FiveM, PC, etc.",
        max_length=50,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 1. Get channels from config
        channel_id = Config.CHANNEL_MAP.get(self.build_type)
        channel = interaction.guild.get_channel(channel_id)
        master_log = interaction.guild.get_channel(Config.LEAD_LOG_CHANNEL_ID)
        discussion_root = interaction.guild.get_channel(Config.DISCUSSION_CHANNEL_ID)

        # 2. Create the Summary Embed
        embed = discord.Embed(
            title=f"🛠️ New {self.build_type} Submission",
            color=Config.PRIMARY_COLOR
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="Platform", value=self.platform.value, inline=True)
        embed.add_field(name="Price", value=f"${self.price.value}" if self.price.value != "0" else "Free", inline=True)
        embed.add_field(name="Details", value=self.details.value, inline=False)
        embed.set_footer(text=Config.FOOTER_TEXT)

        # 3. Create Private Thread for images/discussion
        # We use a private thread so only staff and the user can see it
        thread = await discussion_root.create_thread(
            name=f"Project: {interaction.user.display_name} - {self.build_type}",
            type=discord.ChannelType.private_thread
        )
        await thread.add_user(interaction.user)
        
        # Send initial info into the private thread
        await thread.send(content=f"**Official Project Details for {interaction.user.mention}:**", embed=embed)
        await thread.send("Please **upload your images, blueprints, or screenshots** directly below in this chat.")

        # 4. Send the Logs to your staff channels
        log_msg = f"✅ **Thread Created:** {thread.jump_url}"
        if channel: await channel.send(content=log_msg, embed=embed)
        if master_log: await master_log.send(content=log_msg, embed=embed)

        # 5. Show the user the "Add Image" button bar (Ephemeral = only they see it)
        view = ImageUploadView(thread.jump_url)
        await interaction.response.send_message(
            "### ✅ Application Received!\nTo finish, click the button below to upload your reference images.",
            view=view,
            ephemeral=True
        )

class BuildSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="What kind of build would you like to be submitting today?",
        options=[
            discord.SelectOption(label="Bunker", description="Submit a custom DayZ bunker build"),
            discord.SelectOption(label="Store", description="Submit a store/shop layout"),
            discord.SelectOption(label="Custom Build", description="A unique premium project"),
            discord.SelectOption(label="Bases", description="Clan or player base designs")
        ]
    )
    async