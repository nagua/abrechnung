#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import os.path
import logging, yaml, time
from telegram.ext import Updater, CommandHandler

import group as g
import account as a
import event as e

class AbrechnungsBot:
  def __init__(self, config, groups):
    self.private_chat = int(config["private_chat"])
    self.token        = config["token"]
    self.groups       = groups
    logging.getLogger().setLevel(logging.INFO)
    self.logger = logging.getLogger('AbrechnungsBot')



  def connect_and_run(self):
    updater = Updater(token=self.token)
    dispatcher = updater.dispatcher

    dispatcher.addHandler(CommandHandler('start', self.start))
    dispatcher.addHandler(CommandHandler('add_account', self.add_account))
    dispatcher.addHandler(CommandHandler('show_account_data', self.show_account_data))
    dispatcher.addHandler(CommandHandler('calculate_balancing', self.calculate_balancing))
    dispatcher.addHandler(CommandHandler('do_balancing', self.do_balancing))
    dispatcher.addHandler(CommandHandler('export', self.export))
    dispatcher.addHandler(CommandHandler('import_from_file', self.import_from_file))
    dispatcher.addHandler(CommandHandler('easter', self.easter))
    dispatcher.addHandler(CommandHandler('add_event', self.add_event))

    dispatcher.addErrorHandler(self.unknown)
    
    updater.start_polling()
    updater.idle()
    

  def start(self, bot, update):
    group_id = update.message.chat_id

    found = False

    try:
      self.groups[group_id]
      found = True
    except KeyError:
      bot.sendMessage(chat_id=update.message.chat_id, text="Added new group")

    self.groups[group_id] = g.Group(group_id)

    if found:
      bot.sendMessage(chat_id=update.message.chat_id, text="Recreated group")

  def add_account(self, bot, update, args):
    group_id = update.message.chat_id

    if len(args) != 1:
      return

    self.groups[group_id].add_account(a.Account(args[0]))

  def add_event(self, bot, update, args):
    group_id = update.message.chat_id
    logger = logging.getLogger('add_event')

    if len(args) < 2:
      return 

    amount = args[0]
    payer = args[1]
    participants = args[1:]

    try:
      self.groups[group_id].add_event(e.Event(amount, payer, participants))
      self.export_to_file()

      bot.sendMessage(chat_id=group_id, text="Event was added")
    except g.GroupError as ex:
      bot.sendMessage(chat_id=group_id, text=str(ex))



  def show_account_data(self, bot, update):
    group_id = update.message.chat_id
    
    text = ""
    for acc in self.groups[group_id].accounts:
      text += str(acc) + '\n'

    bot.sendMessage(chat_id=group_id, text=text)

  def calculate_balancing(self, bot, update):
    group_id = update.message.chat_id
    gr = self.groups[group_id]

    text = ""
    transactions = gr.calculate_balancing()

    for trans in transactions:
      text += str(trans) + '\n'

    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def do_balancing(self, bot, update):
    pass
    #group_id = update.message.chat_id
    #gr = self.groups[group_id]

    #text = "All account balances were set back to zero\n"
    #transactions = gr.do_balancing()

    #for trans in transactions:
    #  text += str(trans) + '\n'

    #bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def export(self, bot, update):
    group_id = update.message.chat_id

    if group_id != self.private_chat:
      return

    text = self.export_to_file()
    self.logger.info(text)
    bot.sendMessage(chat_id=update.message.chat_id, text="Export done")

  def export_to_file(self):
    export_file = '/usr/backup/export.yml'
    text = yaml.dump(self.groups)
    with open(export_file, 'w') as f:
      f.write(text)
    return text

  def import_from_file(self, bot, update):
    import_file = '/usr/backup/import.yml'
    group_id = update.message.chat_id

    if group_id != self.private_chat:
      return

    with open(import_file) as f:
      obj = yaml.load(f)

    self.groups = obj

  def easter(self, bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="This is a easter egg!")

  def unknown(self, bot, update, error):
    self.logger.info(error)
    bot.sendMessage(chat_id=update.message.chat_id, text="Tut mir leid, ich habe dein Kommando nicht verstanden!")

def main():
  logging.basicConfig(format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')
  logging.getLogger().setLevel(logging.INFO)
  logger = logging.getLogger('main')

  logger.info("Initialisiere TelegramBot!")

  # Load configuration
  with open("config.yml") as data_file:
    config = yaml.load(data_file)

  try:
    with open("/usr/backup/import.yml") as f:
      groups = yaml.load(f)
  except OSError as e:
    groups = {}

  bot = AbrechnungsBot(config, groups)
  bot.connect_and_run()
  
  logger.info("Bot initialisiert")

if __name__ == '__main__':
	main()

