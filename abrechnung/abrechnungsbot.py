from telegram import Updater
import yaml, time

print("Initialisiere TelegramBot!")

with open("config.yaml") as data_file:
    config = yaml.load(data_file)

updater = Updater(token=config["token"])
dispatcher = updater.dispatcher

def start(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Hallo ich bin dein Abrechnungsbot!")

def unknown(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Tut mir leid, ich habe dein Kommando nicht verstanden!")

def easter(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="This is a easter egg!")

def add_event(bot, update, args):
  event = Event()
  event.cost = float(args[0])
  event.persons = args[1:]
  print(args)

dispatcher.addTelegramCommandHandler('start', start)
dispatcher.addTelegramCommandHandler('easter', easter)
dispatcher.addTelegramCommandHandler('add_event', add_event)
dispatcher.addUnknownTelegramCommandHandler(unknown)

updater.start_polling()

print("Bot initialisiert")
