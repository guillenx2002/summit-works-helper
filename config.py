import os

class Config:
    # Token loaded from Railway Environment Variables
    TOKEN = os.getenv("BOT_TOKEN")
    
    # --- Main Server & Welcome IDs ---
    GUILD_ID = 123456789012345678  # Replace with your Server ID
    WELCOME_CHANNEL_ID = 1487864190969577516
    
    # --- Master Lead Log (For all applications) ---
    LEAD_LOG_CHANNEL_ID = 1487892567151476807
    
    # --- Categorized Lead Channels ---
    # Replace these 0s with the actual Channel IDs for each category
    BUNKER_LOG_ID = 0
    STORE_LOG_ID = 0
    CUSTOM_BUILD_LOG_ID = 0
    BASES_LOG_ID = 0

    # This dictionary maps the button label to the specific channel ID
    CHANNEL_MAP = {
        "Bunker": BUNKER_LOG_ID,
        "Store": STORE_LOG_ID,
        "Custom Build": CUSTOM_BUILD_LOG_ID,
        "Bases": BASES_LOG_ID
    }
    
    # Branding & Visuals
    PRIMARY_COLOR = 0x0057FF       # Summit Works Blue
    BOT_NAME = "Summit Works Helper"
    BANNER_URL = "https://your-image-link.com/banner.png" 
    FOOTER_TEXT = "Summit Works | Premium Custom Builds"