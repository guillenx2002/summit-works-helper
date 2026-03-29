import os
import discord

class Config:
    # This line hides your secret. We will put the actual token into Railway's "Variables" tab.
    TOKEN = os.getenv("BOT_TOKEN")
    
    # Replace these numbers with your actual Discord Channel IDs
    GUILD_ID = 123456789012345678  
    WELCOME_CHANNEL_ID = 111222333444
    LEAD_LOG_CHANNEL_ID = 555666777888
    
    # Branding & Visuals
    PRIMARY_COLOR = 0x0057FF       # Summit Works Blue
    BOT_NAME = "Summit Works Helper"
    BANNER_URL = "https://your-image-link.com/banner.png" 
    FOOTER_TEXT = "Summit Works | Premium Custom Builds"