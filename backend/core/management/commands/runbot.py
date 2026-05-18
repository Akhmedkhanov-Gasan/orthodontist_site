from django.conf import settings
from django.core.management.base import BaseCommand

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from core.bot.handlers import (
    contact_message,
    start,
    text_message,
    register_command,
    appointment_command,
    contacts_command,
    info_command,
)


class Command(BaseCommand):
    help = "Run Telegram bot"

    def handle(self, *args, **options):
        token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")

        if not token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

        proxy_url = getattr(settings, "TELEGRAM_PROXY_URL", "")

        builder = Application.builder().token(token)

        if proxy_url:
            builder = builder.proxy_url(proxy_url).get_updates_proxy_url(proxy_url)

        application = builder.build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.CONTACT, contact_message))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
        application.add_handler(CommandHandler("register", register_command))
        application.add_handler(CommandHandler("appointment", appointment_command))
        application.add_handler(CommandHandler("contacts", contacts_command))
        application.add_handler(CommandHandler("info", info_command))

        self.stdout.write(self.style.SUCCESS("Bot started"))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
