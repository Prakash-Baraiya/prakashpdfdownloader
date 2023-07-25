import os
import re
import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token (Replace 'YOUR_BOT_TOKEN' with your actual bot token)
BOT_TOKEN = '6350787351:AAEFb2fd16k8OyNQO0YzgnY6a-6TlgKv02M'

# Bot commands
START_COMMAND = "start"
DOWNLOAD_COMMAND = "download"

def start(update: Update, context: CallbackContext):
    """Handler for /start command."""
    update.message.reply_text("Welcome! Send me a .txt or txt file with name:url format to download PDFs.")

def download_pdf(update: Update, context: CallbackContext):
    """Handler for user messages containing .txt or txt files."""
    file = update.message.document
    file_name = file.file_name
    file_url = file.get_file().file_path

    # Download the file
    file_path = f"./{file_name}"
    file.download(file_path)

    # Read the content of the file and extract PDF URLs
    with open(file_path, 'r') as f:
        content = f.read()
        pdf_urls = re.findall(r'\S+\.pdf', content)

    # Download each PDF
    for url in pdf_urls:
        pdf_file_name = url.split('/')[-1]
        response = requests.get(url)

        if response.status_code == 200:
            with open(pdf_file_name, 'wb') as pdf_file:
                pdf_file.write(response.content)
            update.message.reply_document(document=open(pdf_file_name, 'rb'))
            os.remove(pdf_file_name)  # Remove the downloaded PDF after sending

    # Remove the temporary .txt file
    os.remove(file_path)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler(START_COMMAND, start))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("txt"), download_pdf))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
