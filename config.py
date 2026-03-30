import os

class Config:
    # Token loaded from Railway Environment Variables
    TOKEN = os.getenv("BOT_TOKEN")
    
    # --- Main Server & Welcome IDs ---
    GUILD_ID = 123456789012345678  # Replace with your Server ID
    WELCOME_CHANNEL_ID = 1487864190969577516
    
    # --- Master Lead Log (For all applications) ---
    LEAD_LOG_CHANNEL_ID = 1487892567151476807
    
    # --- DayZ Categorized Lead Channels ---
    BUNKER_LOG_ID = 1488201109511077888
    STORE_LOG_ID = 1488201109511077888
    CUSTOM_BUILD_LOG_ID = 1487890299899482245
    BASES_LOG_ID = 0 # Update this when ready

    CHANNEL_MAP = {
        "Bunker": BUNKER_LOG_ID,
        "Store": STORE_LOG_ID,
        "Custom Build": CUSTOM_BUILD_LOG_ID,
        "Bases": BASES_LOG_ID
    }

    # --- FiveM Categorized Lead Channels ---
    # Replace these 0s with your FiveM Channel IDs
    HOOD_PACK_ID = 0
    CUSTOM_CITY_ID = 0
    GUN_PACK_ID = 0
    SOUND_PACK_ID = 0
    CAR_PACK_ID = 0
    STORE_PACK_ID = 0

    FIVEM_MAP = {
        "Hood Pack": HOOD_PACK_ID,
        "Custom City": CUSTOM_CITY_ID,
        "Gun Pack": GUN_PACK_ID,
        "Sound Pack": SOUND_PACK_ID,
        "Car Pack": CAR_PACK_ID,
        "Store Pack": STORE_PACK_ID
    }
    
    # Branding & Visuals
    PRIMARY_COLOR = 0x0057FF       # Summit Works Blue
    BOT_NAME = "Summit Works Helper"
    BANNER_URL = "https://your-image-link.com/banner.png" 
    FOOTER_TEXT = "Summit Works | Premium Custom Builds"