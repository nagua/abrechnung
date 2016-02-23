#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import logging, yaml, time
from telegram import Updater

def start(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Hallo ich bin dein Abrechnungsbot!")

def unknown(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Tut mir leid, ich habe dein Kommando nicht verstanden!")

def easter(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="This is a easter egg!")

def add_event(bot, update, args):
  pass

def main():
  logging.basicConfig(format='$(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logging.setLevel(logging.INFO)
  mainLogger = logging.getLogger('main')

  mainLogger.info("Initialisiere TelegramBot!")

  # Load configuration
  with open("config.yaml") as data_file:
    config = yaml.load(data_file)

  updater = Updater(token=config["token"])
  dispatcher = updater.dispatcher

  dispatcher.addTelegramCommandHandler('start', start)
  dispatcher.addTelegramCommandHandler('easter', easter)
  dispatcher.addTelegramCommandHandler('add_event', add_event)
  dispatcher.addUnknownTelegramCommandHandler(unknown)
  
  updater.start_polling()
  
  mainLogger.info("Bot initialisiert")

if __name__ == '__main__':
	main()