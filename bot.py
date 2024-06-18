from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import os

# Bot token and photo URL
TOKEN = '6733069227:AAHYq8EdSBslEZBk_RYcjMJ0XbmcPYR-nVM'
PHOTO_URL = 'https://graph.org/file/c68a92276df042c2d5b49.jpg'

# Telegram IDs and URLs
TELEGRAM_ID = 'Yourpriye'
CHANNEL_URL = 'https://t.me/Electric_Hacker_Team'
GITHUB_URL = 'https://github.com/electricalscammer'

# Function to handle /start command
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_message = f"Namaste {user.mention_html()}! 😊\n\nMain aapki text files mein caption add kar sakta hoon. Apne text files ko edit karne ke liye /settings ka upayog karein."

    # Welcome message ke liye button ka definition
    buttons = [
        [InlineKeyboardButton("Help ⛔️️", callback_data='help')],
        [InlineKeyboardButton("About 💡", callback_data='about')],
        [InlineKeyboardButton("Developer 🪪", url=f'https://t.me/{TELEGRAM_ID}')],
        [InlineKeyboardButton("Follow me 😊", url=CHANNEL_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Photo ke sath caption aur buttons bhejna
    context.bot.send_photo(
        chat_id=update.message.chat_id,
        photo=PHOTO_URL,
        caption=welcome_message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# Function to add "Join Channel" button with file
def send_file_with_button(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    original_filename = update.message.document.file_name
    new_file_path = f'Electric Hacker_{original_filename}'

    file.download(custom_path=new_file_path)

    # File ke sath caption banao
    caption = f"[Electric Hacker](https://t.me/{TELEGRAM_ID})\n\nFile Name: {original_filename}"
    buttons = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # File aur caption ke sath message bhejna
    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(new_file_path, 'rb'),
        filename=new_file_path,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

    os.remove(new_file_path)

# Function to show settings with buttons
def settings(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🔒 Set Prefix", callback_data='set_prefix')],
        [InlineKeyboardButton("👀 View Prefix", callback_data='view_prefix')],
        [InlineKeyboardButton("🗑 Remove Prefix", callback_data='remove_prefix')],
        [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option ✨️:', reply_markup=reply_markup)

# Function to handle button clicks
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'help':
        help_message = (
            "Bot ka istemal kaise karein:\n\n"
            "- /start: Swagat sandesh aur vikalpon ka chayan.\n"
            "- /settings: Apne prefix ko configure karein.\n"
            "- /setprefix [text]: Apne files ke liye ek prefix set karein.\n"
            "- /viewprefix: Vartaman prefix ko dekhein.\n"
            "- /removeprefix: Vartaman prefix ko hatayein.\n"
            "- Ek text file bhejkar usme prefix ko add karein."
        )
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
        ]
        query.edit_message_text(text=help_message, reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data == 'about':
        about_message = (
            "Bot ke baare mein:\n\n"
            "- Developer: [Aapka Naam](https://t.me/Yourpriye)\n"
            "- Source: [GitHub Repository](https://github.com/electricalscammer)\n"
            "- Support: [Contact Us](https://t.me/Electric_Hacker_Team)"
        )
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
        ]
        query.edit_message_text(
            text=about_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == 'set_prefix':
        context.user_data['awaiting_prefix'] = True
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
        ]
        query.edit_message_text(
            text="Apna caption bhejein, main use aapke text file mein add kar doonga:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == 'view_prefix':
        current_prefix = context.user_data.get('prefix', "Koi prefix set nahi hai.")
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
        ]
        query.edit_message_text(
            text=f'Vartaman prefix hai: {current_prefix}',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == 'remove_prefix':
        context.user_data['prefix'] = ""
        buttons = [
            [InlineKeyboardButton("🔙 Back", callback_data='back'), InlineKeyboardButton("🏘 Home", callback_data='home')]
        ]
        query.edit_message_text(
            text="Prefix hata diya gaya hai ❌️.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == 'back':
        settings(update, context)

    elif query.data == 'home':
        start(update, context)

# Function to handle text input for prefix
def handle_text(update: Update, context: CallbackContext):
    if context.user_data.get('awaiting_prefix', False):
        prefix_to_set = update.message.text
        context.user_data['prefix'] = prefix_to_set
        context.user_data['awaiting_prefix'] = False
        update.message.reply_text(f'Prefix set kiya gaya hai: {prefix_to_set}')

# Function to handle file edits and adding prefix
def edit_file(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    original_filename = update.message.document.file_name
    new_file_path = f'Electric Hacker_{original_filename}'

    file.download(custom_path=new_file_path)

    current_prefix = context.user_data.get('prefix', "Electric Hacker")

    # File ke sath caption aur "Join Channel" button bhejna
    caption = f"[{current_prefix}](https://t.me/{TELEGRAM_ID} ✨️\n\nFile Name: {original_filename}"
    buttons = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=open(new_file_path, 'rb'),
        filename=new_file_path,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

    os.remove(new_file_path)

# Main function to start the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('settings', settings))

    # Handle document and edit file
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), edit_file))

    # Handle button clicks
    dp.add_handler(CallbackQueryHandler(button))

    # Handle text input for prefix
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
