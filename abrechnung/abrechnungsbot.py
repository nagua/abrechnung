#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import os.path
import logging, yaml, time
from telegram import Updater

import group as g
import account as a
import event as e

private_chat = 0
class AbrechnungsBot:
  def __init__(self, import_file="import.yml"):
    try:
      with open(import_file) as f:
        groups = yaml.load(f)
    except OSError as e:
      groups = {}

  def start(self, bot, update):
    group_id = update.message.chat_id

    found = False

    try:
      groups[group_id]
      found = True
    except KeyError:
      bot.sendMessage(chat_id=update.message.chat_id, text="Added new group")

    groups[group_id] = g.Group(group_id)

    if found:
      bot.sendMessage(chat_id=update.message.chat_id, text="Recreated group")

  def add_account(self, bot, update, args):
    group_id = update.message.chat_id

    if len(args) != 1:
      return

    groups[group_id].add_account(a.Account(args[0]))

  def add_event(self, bot, update, args):
    group_id = update.message.chat_id
    logger = logging.getLogger('add_event')

    if len(args) < 2:
      return 

    amount = args[0]
    payer = args[1]
    participants = args[1:]

    groups[group_id].add_event(e.Event(amount, payer, participants))

    bot.sendMessage(chat_id=group_id, text="Event was added")


  def show_account_data(self, bot, update):
    group_id = update.message.chat_id
    
    text = ""
    for acc in groups[group_id].accounts:
      text += str(acc)

    bot.sendMessage(chat_id=group_id, text=text)

  def calculate_balancing(self, bot, update):
    group_id = update.message.chat_id
    gr = groups[group_id]

    text = ""
    transactions = gr.calculate_balancing()

    for trans in transactions:
      text += str(trans)

    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def do_balancing(self, bot, update):
    group_id = update.message.chat_id
    gr = groups[group_id]

    text = "All account balances were set back to zero\n"
    transactions = gr.do_balancing()

    for trans in transactions:
      text += str(trans)

    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def export(self, bot, update):
    group_id = update.message.chat_id

    if group_id != private_chat:
      return

    text = yaml.dump(groups)
    with open('export.yml', 'w') as f:
      f.write(text)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def import_from_file(self, bot, update):
    global groups
    group_id = update.message.chat_id

    if group_id != private_chat:
      return

    with open('import.yml') as f:
      obj = yaml.load(f)

    #Not working, don't know why...
    groups = obj

  def easter(self, bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="This is a easter egg!")

  def unknown(self, bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Tut mir leid, ich habe dein Kommando nicht verstanden!")

def main():
  global private_chat
  logging.basicConfig(format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')
  logging.getLogger().setLevel(logging.INFO)
  logger = logging.getLogger('main')

  logger.info("Initialisiere TelegramBot!")

  # Load configuration
  with open("config.yml") as data_file:
    config = yaml.load(data_file)

  private_chat = int(config["private_chat"])

  updater = Updater(token=config["token"])
  dispatcher = updater.dispatcher

  bot = AbrechnungsBot()
  dispatcher.addTelegramCommandHandler('start', bot.start)
  dispatcher.addTelegramCommandHandler('add_account', bot.add_account)
  dispatcher.addTelegramCommandHandler('show_account_data', bot.show_account_data)
  dispatcher.addTelegramCommandHandler('calculate_balancing', bot.calculate_balancing)
  dispatcher.addTelegramCommandHandler('do_balancing', bot.do_balancing)
  dispatcher.addTelegramCommandHandler('export', bot.export)
  dispatcher.addTelegramCommandHandler('import_from_file', bot.import_from_file)
  dispatcher.addTelegramCommandHandler('easter', bot.easter)
  dispatcher.addTelegramCommandHandler('add_event', bot.add_event)
  dispatcher.addUnknownTelegramCommandHandler(bot.unknown)
  
  updater.start_polling()
  
  logger.info("Bot initialisiert")

if __name__ == '__main__':
	main()

