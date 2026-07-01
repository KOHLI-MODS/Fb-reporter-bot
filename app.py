# app.py - Render Entry Point
import os
import sys
import json
from datetime import datetime
from bot import FacebookReportBot, DataManager, DATA_FILE

# Create bot instance
bot = FacebookReportBot()

# Run the bot (this will start polling)
if __name__ == "__main__":
    print("🚀 Starting bot on Render...")
    bot.run()
