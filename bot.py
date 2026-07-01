# ============================================================
# 🚀 FB REPORT BOT - RENDER DEPLOYMENT READY
# 📱 Modern UI with Animations & Flask Server
# 👑 Created by @PRIKSHIT_THE
# ⚡ Version: 3.1 - Render Optimized
# ============================================================

import os
import sys
import time
import random
import threading
import json
import logging
import asyncio
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import wraps
import re

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    Chat, ChatMember, ChatInviteLink, User
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler,
    JobQueue
)
from telegram.constants import ParseMode
from telegram.error import TelegramError

# ============================================================
# 📋 CONFIGURATION - ENVIRONMENT VARIABLES
# ============================================================

# Bot Configuration - AB YEH ENVIRONMENT VARIABLES SE LEGA
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8633276750:AAHTy0D5ScVS_9ouZrPaJyON0--CMuif7YQ")
ADMIN_IDS = [int(id.strip()) for id in os.environ.get("ADMIN_IDS", "8122122768").split(",")]

# Force Join Channels
REQUIRED_CHANNELS = [
    {
        "id": os.environ.get("CHANNEL_1", "-1004464814137"),
        "name": "📢 Main Channel",
        "link": os.environ.get("CHANNEL_1_LINK", "https://t.me/PRIKSHITXSTORE"),
        "emoji": "🔥"
    },
    {
        "id": os.environ.get("CHANNEL_2", "-1002707310819"),
        "name": "📢 Updates Channel",
        "link": os.environ.get("CHANNEL_2_LINK", "https://t.me/+s9d7InMMAu05ZDM1"),
        "emoji": "⚡"
    },
    {
        "id": os.environ.get("CHANNEL_3", "-1002414151665"),
        "name": "👥 Support Group",
        "link": os.environ.get("CHANNEL_3_LINK", "https://t.me/prikshitthe"),
        "type": "group",
        "emoji": "💬"
    }
]

# File Paths
DATA_FILE = "user_data.json"
KEYS_FILE = "premium_keys.json"
BROADCAST_FILE = "broadcast_data.json"
SETTINGS_FILE = "settings.json"
REPORTS_FILE = "reports_log.json"

# Premium Plans
PLANS = {
    "basic": {
        "name": "🌟 Basic Plan",
        "price": 99,
        "reports": 50,
        "duration": 1,
        "features": ["📊 50 Reports", "⏰ 1 Day Access", "📱 Basic Support"],
        "color": "#4CAF50",
        "emoji": "🌟"
    },
    "premium": {
        "name": "💎 Premium Plan",
        "price": 249,
        "reports": 200,
        "duration": 7,
        "features": ["📊 200 Reports", "⏰ 7 Days Access", "⚡ Priority Support", "🎯 Bulk Reporting"],
        "color": "#2196F3",
        "emoji": "💎"
    },
    "ultimate": {
        "name": "👑 Ultimate Plan",
        "price": 499,
        "reports": 500,
        "duration": 30,
        "features": ["📊 500 Reports", "⏰ 30 Days Access", "🌟 24/7 Support", "💫 VIP Status", "🚀 Unlimited Features"],
        "color": "#FF6B00",
        "emoji": "👑"
    }
}

# Report Reasons
REPORT_REASONS = {
    "fake": {"label": "🎭 Fake Profile", "color": "danger", "emoji": "🎭"},
    "harassment": {"label": "⚠️ Harassment/Bullying", "color": "danger", "emoji": "⚠️"},
    "nudity": {"label": "🔞 Nudity/Violence", "color": "danger", "emoji": "🔞"},
    "spam": {"label": "📧 Spam/Scam", "color": "primary", "emoji": "📧"},
    "hate": {"label": "💢 Hate Speech", "color": "danger", "emoji": "💢"},
    "impersonation": {"label": "👤 Impersonation", "color": "primary", "emoji": "👤"},
    "other": {"label": "📝 Other", "color": "primary", "emoji": "📝"}
}

# ============================================================
# 📊 LOGGING
# ============================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# 🎨 ANIMATION HELPERS
# ============================================================

class Animations:
    @staticmethod
    def loading_bar(progress: float, width: int = 20) -> str:
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f"`[{bar}]` {int(progress * 100)}%"
    
    @staticmethod
    def spinner(frame: int) -> str:
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        return frames[frame % len(frames)]

class ModernUI:
    @staticmethod
    def header(title: str, subtitle: str = "") -> str:
        border = "━━━━━━━━━━━━━━━━━━━━━"
        return f"""
🎯 *{title}*
{'-' * len(title)}
{subtitle if subtitle else ''}
{'-' * len(title)}
        """
    
    @staticmethod
    def success_box(text: str) -> str:
        return f"""
✅ *SUCCESS*
━━━━━━━━━━━━━━━━━━━━━
{text}
━━━━━━━━━━━━━━━━━━━━━
        """
    
    @staticmethod
    def error_box(text: str) -> str:
        return f"""
❌ *ERROR*
━━━━━━━━━━━━━━━━━━━━━
{text}
━━━━━━━━━━━━━━━━━━━━━
        """
    
    @staticmethod
    def info_box(text: str) -> str:
        return f"""
ℹ️ *INFO*
━━━━━━━━━━━━━━━━━━━━━
{text}
━━━━━━━━━━━━━━━━━━━━━
        """
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 25) -> str:
        progress = current / total if total > 0 else 0
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f"`[{bar}]` {int(progress * 100)}% ({current}/{total})"

class ButtonStyles:
    @staticmethod
    def get_colored_keyboard(buttons: List[List[tuple]]) -> InlineKeyboardMarkup:
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button in row:
                if len(button) == 3:
                    text, callback, color = button
                    keyboard_row.append(InlineKeyboardButton(text, callback_data=callback))
                else:
                    text, callback = button
                    keyboard_row.append(InlineKeyboardButton(text, callback_data=callback))
            keyboard.append(keyboard_row)
        return InlineKeyboardMarkup(keyboard)

# ============================================================
# 📁 DATA MANAGER
# ============================================================

class DataManager:
    @staticmethod
    def load_json(filename: str) -> dict:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {filename}")
            return {}
    
    @staticmethod
    def save_json(filename: str, data: dict) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving JSON to {filename}: {e}")
            return False
    
    @staticmethod
    def get_user(user_id: int) -> dict:
        data = DataManager.load_json(DATA_FILE)
        return data.get(str(user_id), {})
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> bool:
        data = DataManager.load_json(DATA_FILE)
        data[str(user_id)] = user_data
        return DataManager.save_json(DATA_FILE, data)
    
    @staticmethod
    def get_all_users() -> dict:
        return DataManager.load_json(DATA_FILE)
    
    @staticmethod
    def get_premium_keys() -> dict:
        return DataManager.load_json(KEYS_FILE)
    
    @staticmethod
    def save_premium_keys(keys: dict) -> bool:
        return DataManager.save_json(KEYS_FILE, keys)
    
    @staticmethod
    def log_report(user_id: int, target: str, reason: str, count: int) -> bool:
        data = DataManager.load_json(REPORTS_FILE)
        if str(user_id) not in data:
            data[str(user_id)] = []
        
        data[str(user_id)].append({
            "target": target,
            "reason": reason,
            "count": count,
            "timestamp": datetime.now().isoformat()
        })
        return DataManager.save_json(REPORTS_FILE, data)
    
    @staticmethod
    def get_settings() -> dict:
        return DataManager.load_json(SETTINGS_FILE)
    
    @staticmethod
    def save_settings(settings: dict) -> bool:
        return DataManager.save_json(SETTINGS_FILE, settings)

# ============================================================
# 🔑 KEY GENERATOR
# ============================================================

class KeyGenerator:
    @staticmethod
    def generate_key(plan_type: str, duration_days: int) -> str:
        random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        plan_code = plan_type[:3].upper()
        expiry = (datetime.now() + timedelta(days=duration_days)).strftime("%Y%m%d")
        
        key = f"{plan_code}-{random_part}-{expiry}"
        
        keys = DataManager.get_premium_keys()
        keys[key] = {
            "plan_type": plan_type,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=duration_days)).isoformat(),
            "used_by": None,
            "is_used": False
        }
        DataManager.save_premium_keys(keys)
        
        return key
    
    @staticmethod
    def validate_key(key: str) -> Tuple[bool, dict]:
        keys = DataManager.get_premium_keys()
        
        if key not in keys:
            return False, {"message": "❌ Invalid key! Please check and try again."}
        
        key_data = keys[key]
        
        if key_data["is_used"]:
            return False, {"message": "❌ This key has already been used!"}
        
        expiry_date = datetime.fromisoformat(key_data["expires_at"])
        if datetime.now() > expiry_date:
            return False, {"message": "❌ This key has expired!"}
        
        return True, key_data

# ============================================================
# 🛡️ DECORATORS
# ============================================================

def admin_only(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text(
                ModernUI.error_box(
                    "🚫 *Access Denied!*\n\n"
                    "You don't have permission to use this command."
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        return await func(self, update, context, *args, **kwargs)
    return wrapper

def premium_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        
        if not self.check_premium_status(user_id):
            keyboard = [
                ("💰 Buy Premium", "show_plans", "primary"),
                ("🔑 Enter Key", "enter_key", "success")
            ]
            inline_keyboard = ButtonStyles.get_colored_keyboard([keyboard])
            
            await update.message.reply_text(
                ModernUI.info_box(
                    "💎 *Premium Required!*\n\n"
                    "This feature requires an active premium subscription.\n\n"
                    "✨ *Get Premium to unlock:*\n"
                    "• Unlimited Reporting\n"
                    "• Priority Support\n"
                    "• VIP Features\n\n"
                    "⬇️ *Choose an option below:*"
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_keyboard
            )
            return
        
        return await func(self, update, context, *args, **kwargs)
    return wrapper

# ============================================================
# 🤖 MAIN BOT CLASS
# ============================================================

class FacebookReportBot:
    def __init__(self):
        self.application = None
        self.active_reports = {}
        self.start_time = datetime.now()
        self.report_reasons = REPORT_REASONS
        self.plans = PLANS
        self.animation_frames = 0
    
    # ========== START ==========
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username or "User"
        
        user_data = DataManager.get_user(user_id)
        if not user_data:
            user_data = {
                "joined_at": datetime.now().isoformat(),
                "premium_active": False,
                "reports_used": 0,
                "reports_limit": 0,
                "username": username
            }
            DataManager.update_user(user_id, user_data)
        
        if not await self.check_channels(update, context):
            return
        
        await self.show_main_menu(update, context, user_data)
    
    async def check_channels(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        user_id = update.effective_user.id
        
        settings = DataManager.get_settings()
        force_join = settings.get("force_join", True)
        
        if not force_join:
            return True
        
        not_joined = []
        
        for channel in REQUIRED_CHANNELS:
            try:
                chat_member = await context.bot.get_chat_member(
                    chat_id=channel["id"],
                    user_id=user_id
                )
                
                if chat_member.status in ["left", "kicked"]:
                    not_joined.append(channel)
                    
            except Exception as e:
                logger.error(f"Error checking channel {channel['id']}: {e}")
                not_joined.append(channel)
        
        if not_joined:
            keyboard = []
            for channel in not_joined:
                try:
                    invite_link = await context.bot.create_chat_invite_link(
                        chat_id=channel["id"],
                        member_limit=1
                    )
                    channel["link"] = invite_link.invite_link
                except:
                    pass
                
                keyboard.append([(
                    f"{channel.get('emoji', '📢')} Join {channel['name']}",
                    channel.get("link", f"https://t.me/joinchat/placeholder"),
                    "primary"
                )])
            
            keyboard.append([(
                "✅ I've Joined All",
                "check_join",
                "success"
            )])
            
            inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
            
            await update.message.reply_text(
                ModernUI.info_box(
                    "🌟 *WELCOME TO FB REPORT BOT* 🌟\n\n"
                    "🎯 *Join Required Channels*\n"
                    "━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"📌 *{len(not_joined)} channels pending*\n\n"
                    "✨ *Why join?*\n"
                    "• Get latest updates\n"
                    "• Premium giveaways\n"
                    "• Support community\n\n"
                    "⬇️ *Click buttons below to join*"
                ),
                reply_markup=inline_keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            return False
        
        return True
    
    async def check_join_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer("🔍 Verifying your subscriptions...")
        
        if await self.check_channels(update, context):
            user_data = DataManager.get_user(update.effective_user.id)
            await query.edit_message_text(
                "✅ *All channels joined successfully!*\n\n"
                "🎯 *Loading main menu...*"
            )
            await asyncio.sleep(1)
            await self.show_main_menu(update, context, user_data)
    
    # ========== MAIN MENU ==========
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict = None):
        user_id = update.effective_user.id
        
        if user_data is None:
            user_data = DataManager.get_user(user_id)
        
        has_premium = self.check_premium_status(user_id)
        
        keyboard = []
        
        if has_premium:
            keyboard.append([KeyboardButton("🎯 📊 Start Reporting")])
        else:
            keyboard.append([KeyboardButton("💎 💳 Get Premium")])
            
        keyboard.extend([
            [KeyboardButton("🔵 📊 Report Account"), KeyboardButton("🔵 💎 Plans")],
            [KeyboardButton("🟡 📈 My Status"), KeyboardButton("🔵 📢 Support")],
        ])
        
        if user_id in ADMIN_IDS:
            keyboard.append([KeyboardButton("🔴 👑 Admin Panel")])
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        if has_premium:
            plan = user_data.get("premium_plan", "Basic")
            expiry = user_data.get("premium_expiry", "N/A")
            reports_used = user_data.get("reports_used", 0)
            reports_limit = user_data.get("reports_limit", 50)
            remaining = reports_limit - reports_used
            
            status_text = (
                "━━━━━━━━━━━━━━━━━━━━━\n"
                f"🌟 *Plan:* {plan}\n"
                f"✅ *Status:* Active\n"
                f"⏰ *Expires:* {expiry}\n"
                f"📊 *Reports:* {reports_used}/{reports_limit}\n"
                f"📈 *Remaining:* {remaining}\n"
                "━━━━━━━━━━━━━━━━━━━━━"
            )
        else:
            status_text = (
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "❌ *Status:* Inactive\n"
                "💎 *Plan:* None\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "⭐ *Get premium to start reporting!*"
            )
        
        welcome = (
            "🌟 *FB REPORT BOT* 🌟\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🎯 *Premium Report Bot*\n"
            "💪 *Report fake accounts easily*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{status_text}\n\n"
            "📌 *Select an option below:*"
        )
        
        await update.message.reply_text(
            welcome,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def check_premium_status(self, user_id: int) -> bool:
        user_data = DataManager.get_user(user_id)
        
        if not user_data.get("premium_active", False):
            return False
        
        expiry_str = user_data.get("premium_expiry")
        if not expiry_str:
            return False
        
        try:
            expiry_date = datetime.fromisoformat(expiry_str)
            if datetime.now() > expiry_date:
                user_data["premium_active"] = False
                DataManager.update_user(user_id, user_data)
                return False
            return True
        except:
            return False
    
    # ========== MENU HANDLERS ==========
    
    async def handle_menu_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        clean_text = re.sub(r'[^\w\s]', '', text).strip()
        
        if "Start Reporting" in clean_text or "Report Account" in clean_text:
            await self.start_reporting(update, context)
        elif "Get Premium" in clean_text or "Plans" in clean_text:
            await self.show_premium_plans(update, context)
        elif "My Status" in clean_text:
            await self.show_status(update, context)
        elif "Support" in clean_text:
            await self.show_support(update, context)
        elif "Admin Panel" in clean_text and user_id in ADMIN_IDS:
            await self.show_admin_panel(update, context)
    
    # ========== PREMIUM PLANS ==========
    
    async def show_premium_plans(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        
        for plan_key, plan in self.plans.items():
            color = "success" if plan_key == "ultimate" else "primary"
            keyboard.append([(
                f"{plan['emoji']} {plan['name']} - ₹{plan['price']}",
                f"plan_{plan_key}",
                color
            )])
        
        keyboard.append([(
            "🔑 Enter Premium Key",
            "enter_key",
            "primary"
        )])
        keyboard.append([(
            "⬅️ Back to Menu",
            "back_menu",
            "danger"
        )])
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        plans_text = "\n".join([
            f"{plan['emoji']} *{plan['name']}* - ₹{plan['price']}\n"
            f"  • {plan['reports']} Reports\n"
            f"  • {plan['duration']} Day{'s' if plan['duration'] > 1 else ''} Access"
            for plan in self.plans.values()
        ])
        
        await update.message.reply_text(
            ModernUI.header("💎 PREMIUM PLANS", "Choose your plan!") +
            f"\n{plans_text}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "💳 *Payment Methods:*\n"
            "• UPI: `piyush200a@fam`\n"
            "• Premium Keys: Supported\n\n"
            "⬇️ *Select a plan below:*",
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_plans_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        keyboard = []
        for plan_key, plan in self.plans.items():
            color = "success" if plan_key == "ultimate" else "primary"
            keyboard.append([(
                f"{plan['emoji']} {plan['name']} - ₹{plan['price']}",
                f"plan_{plan_key}",
                color
            )])
        
        keyboard.append([(
            "🔑 Enter Premium Key",
            "enter_key",
            "primary"
        )])
        keyboard.append([(
            "⬅️ Back to Menu",
            "back_menu",
            "danger"
        )])
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        plans_text = "\n".join([
            f"{plan['emoji']} *{plan['name']}* - ₹{plan['price']}\n"
            f"  • {plan['reports']} Reports\n"
            f"  • {plan['duration']} Day{'s' if plan['duration'] > 1 else ''} Access"
            for plan in self.plans.values()
        ])
        
        await query.edit_message_text(
            ModernUI.header("💎 PREMIUM PLANS", "Choose your plan!") +
            f"\n{plans_text}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "💳 *Payment Methods:*\n"
            "• UPI: `piyush200a@fam`\n"
            "• Premium Keys: Supported\n\n"
            "⬇️ *Select a plan below:*",
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_plan_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer("💎 Loading plan details...")
        
        plan_key = query.data.replace("plan_", "")
        plan = self.plans.get(plan_key)
        
        if not plan:
            await query.edit_message_text(ModernUI.error_box("Invalid plan!"))
            return
        
        keyboard = [
            [(
                "💰 Pay via UPI",
                f"pay_upi_{plan_key}",
                "success"
            )],
            [(
                "🔑 Enter Premium Key",
                "enter_key",
                "primary"
            )],
            [(
                "⬅️ Back to Plans",
                "show_plans",
                "danger"
            )]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        features = "\n".join([f"└ {f}" for f in plan['features']])
        
        await query.edit_message_text(
            f"{plan['emoji']} *{plan['name']}*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 *Price:* ₹{plan['price']}\n"
            f"📊 *Reports:* {plan['reports']}\n"
            f"⏰ *Duration:* {plan['duration']} days\n\n"
            "✨ *Features:*\n" + features + "\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "💳 *How to pay:*\n"
            "1. UPI: `piyush200a@fam`\n"
            "2. Enter premium key\n\n"
            "⬇️ *Choose payment method:*",
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_upi_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        plan_key = query.data.replace("pay_upi_", "")
        plan = self.plans.get(plan_key)
        
        if not plan:
            await query.edit_message_text(ModernUI.error_box("Invalid plan!"))
            return
        
        keyboard = [
            [(
                "✅ I've Paid",
                f"verify_payment_{plan_key}",
                "success"
            )],
            [(
                "⬅️ Back to Plans",
                "show_plans",
                "danger"
            )]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await query.edit_message_text(
            ModernUI.info_box(
                f"💰 *PAYMENT DETAILS*\n\n"
                f"📋 *Plan:* {plan['name']}\n"
                f"💰 *Amount:* ₹{plan['price']}\n\n"
                "💳 *UPI Payment:*\n"
                "`piyush200a@fam`\n\n"
                "📌 *Instructions:*\n"
                "1. Send payment to above UPI\n"
                "2. Screenshot payment proof\n"
                "3. Send to @prikshitthe\n"
                "4. Wait for admin to activate\n\n"
                "⭐ *After payment, click button below*"
            ),
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ========== PREMIUM KEY ==========
    
    async def enter_premium_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            ModernUI.info_box(
                "🔑 *ENTER PREMIUM KEY*\n\n"
                "Please enter your premium key.\n\n"
                "📌 *Key Format:*\n"
                "`XXX-XXXXXXXX-YYYYMMDD`\n\n"
                "📌 *Example:*\n"
                "`PRE-ABCDEFGH-20241231`\n\n"
                "💡 *How to get a key?*\n"
                "• Buy from admin\n"
                "• Participate in giveaways\n\n"
                "Send /cancel to cancel."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['entering_key'] = True
    
    async def handle_key_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        key = update.message.text.strip().upper()
        
        if not context.user_data.get('entering_key'):
            return
        
        msg = await update.message.reply_text(
            f"🔍 *Verifying premium key...*\n"
            f"{Animations.spinner(0)}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        for i in range(3):
            await asyncio.sleep(0.3)
            await msg.edit_text(
                f"🔍 *Verifying premium key...*\n"
                f"{Animations.spinner(i)}",
                parse_mode=ParseMode.MARKDOWN
            )
        
        valid, data = KeyGenerator.validate_key(key)
        
        if valid:
            user_data = DataManager.get_user(user_id)
            plan = self.plans.get(data['plan_type'])
            
            if plan:
                user_data["premium_active"] = True
                user_data["premium_plan"] = plan['name']
                user_data["premium_expiry"] = data['expires_at']
                user_data["reports_limit"] = plan['reports']
                user_data["reports_used"] = 0
                DataManager.update_user(user_id, user_data)
                
                keys = DataManager.get_premium_keys()
                keys[key]["is_used"] = True
                keys[key]["used_by"] = user_id
                DataManager.save_premium_keys(keys)
                
                await msg.edit_text(
                    ModernUI.success_box(
                        f"✅ *PREMIUM ACTIVATED!*\n\n"
                        f"📋 *Plan:* {plan['name']}\n"
                        f"⏰ *Expires:* {data['expires_at']}\n"
                        f"📊 *Reports:* {plan['reports']}\n\n"
                        "🎯 *You can now start reporting!*"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await msg.edit_text(ModernUI.error_box("❌ Invalid plan data!"))
        else:
            await msg.edit_text(
                ModernUI.error_box(f"{data['message']}\n\nPlease try again."),
                parse_mode=ParseMode.MARKDOWN
            )
        
        context.user_data['entering_key'] = False
    
    # ========== STATUS ==========
    
    async def show_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_data = DataManager.get_user(user_id)
        
        has_premium = self.check_premium_status(user_id)
        
        if has_premium:
            status = "✅ Active"
            plan = user_data.get("premium_plan", "Basic")
            expiry = user_data.get("premium_expiry", "N/A")
            reports_used = user_data.get("reports_used", 0)
            reports_limit = user_data.get("reports_limit", 50)
            remaining = reports_limit - reports_used
        else:
            status = "❌ Inactive"
            plan = "None"
            expiry = "N/A"
            reports_used = 0
            reports_limit = 0
            remaining = 0
        
        reports_log = DataManager.load_json(REPORTS_FILE)
        user_reports = reports_log.get(str(user_id), [])
        total_reports = len(user_reports)
        
        recent = user_reports[-3:] if user_reports else []
        recent_text = "\n".join([
            f"└ {r['timestamp'][:10]} | {r['target']} | {r['count']}x"
            for r in recent
        ]) if recent else "└ No recent reports"
        
        await update.message.reply_text(
            ModernUI.header("📈 MY STATUS", "Your account details") +
            f"""
👤 *User ID:* `{user_id}`
📋 *Plan:* {plan}
🔖 *Status:* {status}
⏰ *Expires:* {expiry}
━━━━━━━━━━━━━━━━━━━━━
📊 *Reports Used:* {reports_used}/{reports_limit}
📈 *Remaining:* {remaining}
📝 *Total Reports:* {total_reports}
━━━━━━━━━━━━━━━━━━━━━
🕐 *Recent Activity:*
{recent_text}
━━━━━━━━━━━━━━━━━━━━━
🤖 *Bot Uptime:* {self.get_uptime()}
            """,
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ========== SUPPORT ==========
    
    async def show_support(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [(
                "📢 Join Support Group",
                "https://t.me/prikshitthe",
                "primary"
            )],
            [(
                "👨‍💻 Contact Admin",
                "https://t.me/prikshitthe",
                "success"
            )],
            [(
                "⬅️ Back to Menu",
                "back_menu",
                "danger"
            )]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await update.message.reply_text(
            ModernUI.header("📢 SUPPORT CENTER", "We're here to help!") +
            """
📌 *Need help?*

• Join our support group
• Contact admin directly
• Check FAQ below

📋 *FAQ:*
❓ How to report?
→ Buy premium, then use report

❓ How to get premium?
→ Buy or use premium key

❓ Reports not working?
→ Contact support

━━━━━━━━━━━━━━━━━━━━━
💫 *We're here to help!*
            """,
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    def get_uptime(self) -> str:
        delta = datetime.now() - self.start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        else:
            return f"{hours}h {minutes}m {seconds}s"
    
    # ========== REPORTING ==========
    
    @premium_required
    async def start_reporting(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [("🎭 Fake Profile", "reason_fake", "danger")],
            [("⚠️ Harassment", "reason_harassment", "danger")],
            [("🔞 Nudity/Violence", "reason_nudity", "danger")],
            [("📧 Spam/Scam", "reason_spam", "primary")],
            [("💢 Hate Speech", "reason_hate", "danger")],
            [("👤 Impersonation", "reason_impersonation", "primary")],
            [("📝 Other", "reason_other", "primary")],
            [("❌ Cancel", "cancel_report", "danger")]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await update.message.reply_text(
            ModernUI.header("📊 REPORT SYSTEM", "Report fake accounts") +
            """
🎯 *Step 1: Enter Facebook ID*

Please enter the Facebook User ID or Profile URL:

📌 *Example:*
• `1000123456789`
• `https://facebook.com/user`

⚠️ *Note:* Make sure the ID is correct.
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['reporting_step'] = 'waiting_fb_id'
    
    async def handle_report_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        step = context.user_data.get('reporting_step')
        
        if step == 'waiting_fb_id':
            context.user_data['fb_id'] = text.strip()
            
            keyboard = [
                [("🎭 Fake Profile", "reason_fake", "danger")],
                [("⚠️ Harassment", "reason_harassment", "danger")],
                [("🔞 Nudity/Violence", "reason_nudity", "danger")],
                [("📧 Spam/Scam", "reason_spam", "primary")],
                [("💢 Hate Speech", "reason_hate", "danger")],
                [("👤 Impersonation", "reason_impersonation", "primary")],
                [("📝 Other", "reason_other", "primary")],
                [("❌ Cancel", "cancel_report", "danger")]
            ]
            
            inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
            
            await update.message.reply_text(
                ModernUI.header("📊 REPORT SYSTEM", "Select a reason") +
                f"""
🎯 *Target:* `{context.user_data['fb_id']}`

Select the reason for reporting:
                """,
                reply_markup=inline_keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            context.user_data['reporting_step'] = 'waiting_reason'
        
        elif step == 'waiting_count':
            try:
                count = int(text)
                if count < 1 or count > 500:
                    await update.message.reply_text(
                        ModernUI.error_box(
                            "❌ *Invalid Count!*\n\n"
                            "Please enter a number between 1 and 500."
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                user_data = DataManager.get_user(user_id)
                reports_used = user_data.get("reports_used", 0)
                reports_limit = user_data.get("reports_limit", 50)
                
                if reports_used + count > reports_limit:
                    keyboard = [[
                        "💎 Upgrade Plan",
                        "show_plans",
                        "success"
                    ]]
                    inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
                    
                    await update.message.reply_text(
                        ModernUI.error_box(
                            f"❌ *Insufficient Reports!*\n\n"
                            f"📊 *Used:* {reports_used}/{reports_limit}\n"
                            f"📊 *Requested:* {count}\n\n"
                            "Please upgrade your plan."
                        ),
                        reply_markup=inline_keyboard,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
                
                context.user_data['report_count'] = count
                await self.execute_reporting(update, context)
                
            except ValueError:
                await update.message.reply_text(
                    ModernUI.error_box(
                        "❌ *Invalid Input!*\n\n"
                        "Please enter a valid number."
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
    
    async def handle_reason_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer("📋 Selecting reason...")
        
        reason_key = query.data.replace("reason_", "")
        reason_data = self.report_reasons.get(reason_key, {"label": "📝 Other", "color": "primary"})
        reason = reason_data["label"]
        
        context.user_data['reason'] = reason
        
        user_id = update.effective_user.id
        user_data = DataManager.get_user(user_id)
        reports_used = user_data.get("reports_used", 0)
        reports_limit = user_data.get("reports_limit", 50)
        remaining = reports_limit - reports_used
        
        if remaining <= 0:
            await query.edit_message_text(
                ModernUI.error_box(
                    "❌ *No Reports Left!*\n\n"
                    f"You've used all {reports_limit} reports.\n"
                    "Please upgrade your plan."
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💎 Upgrade Plan", callback_data="show_plans")]
                ]),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        await query.edit_message_text(
            ModernUI.header("📊 REPORT SYSTEM", "Enter report count") +
            f"""
🎯 *Target:* `{context.user_data.get('fb_id')}`
📋 *Reason:* {reason}
📊 *Remaining:* {remaining} reports

🎯 *Step 3: Enter Report Count*

How many reports to send?
(Max: {min(remaining, 500)})
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['reporting_step'] = 'waiting_count'
    
    async def execute_reporting(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        fb_id = context.user_data.get('fb_id')
        reason = context.user_data.get('reason', 'Spam/Scam')
        count = context.user_data.get('report_count', 50)
        
        progress_msg = await update.message.reply_text(
            ModernUI.header("🔄 REPORTING IN PROGRESS", "Please wait") +
            f"""
🎯 *Target:* `{fb_id}`
📋 *Reason:* {reason}
📊 *Total:* {count}

⏳ *Initializing...*
{Animations.spinner(0)}
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        
        DataManager.log_report(user_id, fb_id, reason, count)
        
        def report_worker():
            for i in range(1, count + 1):
                time.sleep(random.uniform(0.05, 0.15))
                
                if i % 5 == 0 or i == count:
                    try:
                        asyncio.run_coroutine_threadsafe(
                            self.update_report_progress(
                                update, context, progress_msg, i, count
                            ),
                            self.application.loop
                        )
                    except:
                        pass
            
            user_data = DataManager.get_user(user_id)
            user_data["reports_used"] = user_data.get("reports_used", 0) + count
            DataManager.update_user(user_id, user_data)
            
            asyncio.run_coroutine_threadsafe(
                self.report_completed(update, context, progress_msg, fb_id, reason, count),
                self.application.loop
            )
        
        threading.Thread(target=report_worker, daemon=True).start()
    
    async def update_report_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     msg, current: int, total: int):
        try:
            progress = current / total
            bar = Animations.loading_bar(progress, 25)
            spinner = Animations.spinner(current)
            
            await msg.edit_text(
                ModernUI.header("🔄 REPORTING IN PROGRESS", "Please wait") +
                f"""
🎯 *Target:* `{context.user_data.get('fb_id')}`
📊 *Progress:* {bar}
📈 *Status:* {spinner} Sending reports...

⏳ *Processing...*
🌟 *Thank you for using our service!*
                """,
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
    
    async def report_completed(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                               msg, fb_id, reason, count):
        try:
            keyboard = [
                [("🔄 Report Again", "report_again", "success")],
                [("🏠 Main Menu", "back_menu", "primary")]
            ]
            
            inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
            
            await msg.edit_text(
                ModernUI.success_box(
                    f"✅ *REPORTING COMPLETE!*\n\n"
                    f"🎯 *Target:* `{fb_id}`\n"
                    f"📋 *Reason:* {reason}\n"
                    f"📊 *Reports Sent:* {count}\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ *Disclaimer:*\n"
                    "This is a simulation for\n"
                    "educational purposes only.\n"
                    "━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "🌟 *Made with ❤️ by @PRIKSHIT_THE*"
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_keyboard
            )
        except:
            pass
        
        context.user_data['reporting_step'] = None
        context.user_data['fb_id'] = None
        context.user_data['reason'] = None
        context.user_data['report_count'] = None
    
    # ========== CALLBACK HANDLERS ==========
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data
        
        if data.startswith("plan_"):
            await self.handle_plan_selection(update, context)
        elif data.startswith("genkey_"):
            await self.generate_key_callback(update, context)
        elif data.startswith("reason_"):
            await self.handle_reason_selection(update, context)
        elif data.startswith("pay_upi_"):
            await self.handle_upi_payment(update, context)
        elif data == "enter_key":
            await self.enter_premium_key(update, context)
        elif data == "show_plans":
            await self.show_plans_callback(update, context)
        elif data == "back_menu":
            await self.back_to_menu(update, context)
        elif data == "back_admin":
            await self.back_to_admin(update, context)
        elif data == "send_broadcast":
            await self.execute_broadcast(update, context)
        elif data == "cancel_broadcast":
            await self.cancel_broadcast(update, context)
        elif data == "toggle_force_join":
            await self.toggle_force_join(update, context)
        elif data == "check_join":
            await self.check_join_callback(update, context)
        elif data == "report_again":
            await self.report_again(update, context)
        elif data == "cancel_report":
            await self.cancel_report(update, context)
    
    async def back_to_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text("🏠 *Returning to main menu...*")
        await asyncio.sleep(0.5)
        
        user_data = DataManager.get_user(update.effective_user.id)
        await self.show_main_menu(update, context, user_data)
    
    async def back_to_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text("👑 *Returning to admin panel...*")
        await asyncio.sleep(0.5)
        
        await self.show_admin_panel(update, context)
    
    async def report_again(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        context.user_data['reporting_step'] = None
        context.user_data['fb_id'] = None
        context.user_data['reason'] = None
        context.user_data['report_count'] = None
        
        await query.edit_message_text("🔄 *Starting new report...*")
        await asyncio.sleep(0.5)
        
        await self.start_reporting(update, context)
    
    async def cancel_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        context.user_data['reporting_step'] = None
        context.user_data['fb_id'] = None
        context.user_data['reason'] = None
        context.user_data['report_count'] = None
        
        await query.edit_message_text(
            ModernUI.info_box(
                "❌ *Report Cancelled!*\n\n"
                "Use /start to go back to the menu."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ========== ADMIN PANEL ==========
    
    @admin_only
    async def show_admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            ["✅ 📊 Statistics", "🔑 🔑 Generate Key"],
            ["📢 📢 Broadcast", "👥 👥 User List"],
            ["⚙️ ⚙️ Settings", "📁 📁 Report Logs"],
            ["🔙 🔙 Back to Menu"]
        ]
        
        await update.message.reply_text(
            ModernUI.header("👑 ADMIN PANEL", "Admin Control Center") +
            """
📌 *Admin Control Center*

⚡ *Quick Actions:*
• Monitor bot status
• Manage premium keys
• Send broadcasts
• View user data

━━━━━━━━━━━━━━━━━━━━━
🔐 *Admin Access Granted*
            """,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def handle_admin_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        clean_text = re.sub(r'[^\w\s]', '', text).strip()
        
        if "Statistics" in clean_text:
            await self.show_statistics(update, context)
        elif "Generate Key" in clean_text:
            await self.generate_key_menu(update, context)
        elif "Broadcast" in clean_text:
            await self.start_broadcast(update, context)
        elif "User List" in clean_text:
            await self.show_user_list(update, context)
        elif "Settings" in clean_text:
            await self.show_settings(update, context)
        elif "Report Logs" in clean_text:
            await self.view_reports(update, context)
        elif "Back to Menu" in clean_text:
            await self.back_to_menu(update, context)
    
    @admin_only
    async def show_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = DataManager.load_json(DATA_FILE)
        total_users = len(user_data)
        active_premium = sum(1 for u in user_data.values() if u.get("premium_active", False))
        total_reports = sum(u.get("reports_used", 0) for u in user_data.values())
        
        keys = DataManager.get_premium_keys()
        total_keys = len(keys)
        used_keys = sum(1 for k in keys.values() if k.get("is_used", False))
        
        await update.message.reply_text(
            ModernUI.header("📊 BOT STATISTICS", "Live stats") +
            f"""
👥 *User Stats:*
├ Total Users: {total_users}
├ Premium Users: {active_premium}
└ Free Users: {total_users - active_premium}

📊 *Usage Stats:*
├ Total Reports: {total_reports}
└ Avg Reports/User: {total_reports / total_users if total_users > 0 else 0:.1f}

🔑 *Key Stats:*
├ Total Keys: {total_keys}
├ Used Keys: {used_keys}
└ Available Keys: {total_keys - used_keys}

🤖 *Bot Stats:*
├ Uptime: {self.get_uptime()}
└ Status: Online ✅
━━━━━━━━━━━━━━━━━━━━━
            """,
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def generate_key_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = []
        for plan_key, plan in self.plans.items():
            color = "success" if plan_key == "ultimate" else "primary"
            keyboard.append([(
                f"🔑 Generate {plan['name']}",
                f"genkey_{plan_key}",
                color
            )])
        keyboard.append([(
            "⬅️ Back to Admin",
            "back_admin",
            "danger"
        )])
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await update.message.reply_text(
            ModernUI.header("🔑 GENERATE PREMIUM KEY", "Create premium keys") +
            """
📌 *Select a plan to generate a key:*

✨ *Keys can be distributed to users*
💫 *Each key is unique and secure*
            """,
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def generate_key_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer("🔑 Generating key...")
        
        plan_key = query.data.replace("genkey_", "")
        plan = self.plans.get(plan_key)
        
        if not plan:
            await query.edit_message_text(ModernUI.error_box("Invalid plan!"))
            return
        
        key = KeyGenerator.generate_key(plan_key, plan['duration'])
        
        keyboard = [
            [(
                "⬅️ Back",
                "back_admin",
                "danger"
            )]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await query.edit_message_text(
            ModernUI.success_box(
                f"✅ *KEY GENERATED*\n\n"
                f"📋 *Plan:* {plan['name']}\n"
                f"🔑 *Key:* `{key}`\n"
                f"⏰ *Duration:* {plan['duration']} days\n"
                f"📊 *Reports:* {plan['reports']}\n\n"
                "⚠️ *Keep this key secure!*"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inline_keyboard
        )
    
    @admin_only
    async def start_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            ModernUI.header("📢 BROADCAST SYSTEM", "Send message to all users") +
            """
📌 *Send a message to all users*

✏️ *Type your broadcast message below.*

💡 *Tips:*
• Use Markdown for formatting
• Keep messages clear and concise

⛔ Type /cancel to cancel.
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['broadcast_step'] = 'waiting_message'
    
    @admin_only
    async def handle_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get('broadcast_step') == 'waiting_message':
            message = update.message.text
            
            user_data = DataManager.load_json(DATA_FILE)
            
            if not user_data:
                await update.message.reply_text(
                    ModernUI.error_box("❌ No users found to broadcast!")
                )
                return
            
            keyboard = [
                [("✅ Send Broadcast", "send_broadcast", "success")],
                [("❌ Cancel", "cancel_broadcast", "danger")]
            ]
            
            inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
            
            context.user_data['broadcast_message'] = message
            context.user_data['broadcast_users'] = list(user_data.keys())
            
            await update.message.reply_text(
                ModernUI.header("📢 BROADCAST PREVIEW", "Review your message") +
                f"""
📝 *Message:*
{message}

👥 *Total Users:* {len(user_data)}

━━━━━━━━━━━━━━━━━━━━━
❓ *Confirm sending:*
                """,
                reply_markup=inline_keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
    
    @admin_only
    async def execute_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer("📢 Sending broadcast...")
        
        message = context.user_data.get('broadcast_message')
        user_ids = context.user_data.get('broadcast_users', [])
        
        if not message or not user_ids:
            await query.edit_message_text(ModernUI.error_box("❌ Broadcast data not found!"))
            return
        
        sent = 0
        failed = 0
        
        progress_msg = await query.edit_message_text(
            ModernUI.header("📢 SENDING BROADCAST", "Please wait") +
            f"""
⏳ Progress: {Animations.loading_bar(0, 20)}
👥 Users: 0/{len(user_ids)}
            """,
            parse_mode=ParseMode.MARKDOWN
        )
        
        for i, user_id in enumerate(user_ids, 1):
            try:
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=f"📢 *Broadcast Message*\n━━━━━━━━━━━━━━━━━━━━━\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                sent += 1
            except Exception as e:
                failed += 1
                logger.error(f"Failed to send to {user_id}: {e}")
            
            if i % 10 == 0 or i == len(user_ids):
                progress = i / len(user_ids)
                try:
                    await progress_msg.edit_text(
                        ModernUI.header("📢 SENDING BROADCAST", "Please wait") +
                        f"""
⏳ Progress: {Animations.loading_bar(progress, 20)}
👥 Users: {i}/{len(user_ids)}
✅ Sent: {sent} | ❌ Failed: {failed}
                        """,
                        parse_mode=ParseMode.MARKDOWN
                    )
                except:
                    pass
            
            await asyncio.sleep(0.05)
        
        await query.edit_message_text(
            ModernUI.success_box(
                f"✅ *BROADCAST COMPLETE*\n\n"
                f"✅ *Sent:* {sent}\n"
                f"❌ *Failed:* {failed}\n"
                f"👥 *Total:* {len(user_ids)}"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        
        context.user_data['broadcast_step'] = None
        context.user_data['broadcast_message'] = None
        context.user_data['broadcast_users'] = None
    
    @admin_only
    async def cancel_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        context.user_data['broadcast_step'] = None
        context.user_data['broadcast_message'] = None
        context.user_data['broadcast_users'] = None
        
        await query.edit_message_text(
            ModernUI.info_box("❌ *Broadcast Cancelled!*"),
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def show_user_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = DataManager.load_json(DATA_FILE)
        
        if not user_data:
            await update.message.reply_text("📊 No users found.")
            return
        
        user_list = list(user_data.items())[:10]
        text = ModernUI.header("👥 USER LIST", f"Showing {min(10, len(user_data))} of {len(user_data)} users") + "\n"
        
        for user_id, data in user_list:
            premium = "✅" if data.get("premium_active", False) else "❌"
            reports = data.get("reports_used", 0)
            username = data.get("username", "Unknown")
            text += f"👤 `{user_id}` | {username}\n└ Premium: {premium} | Reports: {reports}\n\n"
        
        text += f"\n📊 *Total:* {len(user_data)} users"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    @admin_only
    async def show_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = DataManager.get_settings()
        
        keyboard = [
            [(
                f"🔒 Force Join: {'ON' if settings.get('force_join', True) else 'OFF'}",
                "toggle_force_join",
                "success" if settings.get('force_join', True) else "danger"
            )],
            [("⬅️ Back to Admin", "back_admin", "danger")]
        ]
        
        inline_keyboard = ButtonStyles.get_colored_keyboard(keyboard)
        
        await update.message.reply_text(
            ModernUI.header("⚙️ BOT SETTINGS", "Bot configuration") +
            f"""
📌 *Configuration:*

🔒 *Force Join:* {settings.get('force_join', True)}
👥 *Channels:* {len(REQUIRED_CHANNELS)}
💎 *Plans:* {len(self.plans)}

━━━━━━━━━━━━━━━━━━━━━
⭐ *Click buttons to toggle settings*
            """,
            reply_markup=inline_keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def toggle_force_join(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        settings = DataManager.get_settings()
        settings["force_join"] = not settings.get("force_join", True)
        DataManager.save_settings(settings)
        
        await query.edit_message_text(
            ModernUI.success_box(
                f"✅ *Force Join Toggled!*\n\n"
                f"🔒 Status: {'ON' if settings['force_join'] else 'OFF'}\n\n"
                f"Users will {'need' if settings['force_join'] else 'not need'} "
                f"to join channels."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    
    @admin_only
    async def view_reports(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reports = DataManager.load_json(REPORTS_FILE)
        
        if not reports:
            await update.message.reply_text(
                ModernUI.info_box("📊 No reports found."),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        total_reports = sum(len(log) for log in reports.values())
        recent_reports = []
        
        for user_id, logs in list(reports.items())[:5]:
            for log in logs[-3:]:
                recent_reports.append({
                    "user_id": user_id,
                    "target": log.get("target"),
                    "reason": log.get("reason"),
                    "count": log.get("count"),
                    "time": log.get("timestamp", "")[:10]
                })
        
        text = ModernUI.header("📁 REPORT LOGS", "All report activity") + f"""
📊 *Total Reports:* {total_reports}
👥 *Users:* {len(reports)}

🕐 *Recent Reports:*
"""
        
        for r in recent_reports[:5]:
            text += f"└ {r['time']} | User: `{r['user_id']}`\n"
            text += f"  └ Target: {r['target']} | {r['count']}x\n"
        
        text += "━━━━━━━━━━━━━━━━━━━━━"
        
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    
    # ========== ERROR HANDLING ==========
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")
        
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    ModernUI.error_box(
                        "❌ *Error Occurred!*\n\n"
                        "Please try again later."
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
        except:
            pass
    
    async def cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        await update.message.reply_text(
            ModernUI.info_box(
                "❌ *Cancelled!*\n\n"
                "Current operation cancelled.\n"
                "Use /start to go back to menu."
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ========== MESSAGE HANDLER ==========
    
    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        text = update.message.text
        
        if context.user_data.get('entering_key'):
            await self.handle_key_input(update, context)
            return
        
        if context.user_data.get('reporting_step'):
            await self.handle_report_input(update, context)
            return
        
        if context.user_data.get('broadcast_step'):
            await self.handle_broadcast(update, context)
            return
        
        menu_buttons = [
            "Start Reporting", "Get Premium", "Report Account", "Plans",
            "My Status", "Support", "Admin Panel",
            "Statistics", "Generate Key", "Broadcast",
            "User List", "Settings", "Report Logs", "Back to Menu"
        ]
        
        clean_text = re.sub(r'[^\w\s]', '', text).strip()
        
        if any(btn in clean_text for btn in menu_buttons):
            await self.handle_menu_buttons(update, context)
        elif user_id in ADMIN_IDS:
            await self.handle_admin_buttons(update, context)
        else:
            await update.message.reply_text(
                ModernUI.info_box(
                    "❓ *Unknown Command*\n\n"
                    "Use /start to see the main menu."
                ),
                parse_mode=ParseMode.MARKDOWN
            )
    
    # ========== RUN BOT ==========
    
    def run(self):
        """Run the bot with Flask server"""
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("buy", self.show_premium_plans))
        self.application.add_handler(CommandHandler("cancel", self.cancel_handler))
        
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_messages)
        )
        
        self.application.add_handler(
            CallbackQueryHandler(self.handle_callback)
        )
        
        self.application.add_error_handler(self.error_handler)
        
        # Print banner
        print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🚀 FB REPORT BOT - ULTIMATE EDITION                   ║
║   📱 Modern UI with Animations                          ║
║   👑 Created by @PRIKSHIT_THE                           ║
║   ⚡ Version: 3.1 - Render Optimized                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        print(f"🌟 Starting Facebook Report Bot...")
        print(f"📊 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👑 Admin IDs: {ADMIN_IDS}")
        print(f"📢 Required Channels: {len(REQUIRED_CHANNELS)}")
        print("━━━━━━━━━━━━━━━━━━━━━")
        print("✅ Bot is running!")
        print("📡 Waiting for messages...")
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ============================================================
# 🚀 FLASK SERVER FOR RENDER
# ============================================================

from flask import Flask, request, jsonify
import threading
import signal

app = Flask(__name__)
bot_instance = None

@app.route('/')
def home():
    """Health check endpoint for Render"""
    return {
        "status": "running",
        "bot": "FB Report Bot",
        "version": "3.1",
        "uptime": bot_instance.get_uptime() if bot_instance else "N/A",
        "timestamp": datetime.now().isoformat()
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/stats')
def stats():
    """Get bot statistics"""
    if not bot_instance:
        return {"error": "Bot not initialized"}, 500
    
    user_data = DataManager.load_json(DATA_FILE)
    return {
        "total_users": len(user_data),
        "premium_users": sum(1 for u in user_data.values() if u.get("premium_active", False)),
        "uptime": bot_instance.get_uptime(),
        "timestamp": datetime.now().isoformat()
    }

def run_flask():
    """Run Flask server"""
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    """Run the bot"""
    global bot_instance
    bot_instance = FacebookReportBot()
    bot_instance.run()

# ============================================================
# 🎯 MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    # Initialize data files
    files = [DATA_FILE, KEYS_FILE, BROADCAST_FILE, SETTINGS_FILE, REPORTS_FILE]
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump({}, f, indent=4)
    
    # Initialize settings
    settings = DataManager.get_settings()
    if not settings:
        settings = {
            "force_join": True,
            "created_at": datetime.now().isoformat(),
            "version": "3.1"
        }
        DataManager.save_settings(settings)
    
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run Flask server (main thread)
    print("🌐 Starting Flask server for Render...")
    run_flask()
