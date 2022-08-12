import logging
from telegram import Update, Message
from telegram.ext import (
    Updater,
    CallbackContext,
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from tok import TELEGRAM_TOKEN, TEST_GR0UP_ID

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )
    await dele(update.effective_message, context, from_message=update.effective_message)


async def unknown(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )
    await dele(update.effective_message, context, from_message=update.effective_message)


async def callback_30(context: CallbackContext):
    await context.bot.deleteMessage(chat_id=TEST_GR0UP_ID, message_id=context)


async def dele(
    message: Message, context: CallbackContext, from_message=None, seconds=3
):
    job_queue.run_once(callback_30, seconds, context=message)


if __name__ == "__main__":
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    job_queue = application.job_queue
    start_handler = CommandHandler("start", start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
