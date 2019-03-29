#!/usr/bin/env python3
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import logging, yaml, time, os, datetime
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

import group as g
import account as a
import event as e
import transaction as t
import billingdata as b

class AbrechnungsBot:
  def __init__(self, config, billingdata):
    self.private_chat = int(config["private_chat"])
    self.token        = config["token"]
    self.backup_file  = config["backup_file"]
    self.billingdata  = billingdata
    logging.getLogger().setLevel(logging.INFO)
    self.logger = logging.getLogger('AbrechnungsBot')



  def connect_and_run(self):
    updater = Updater(token=self.token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', self.start))
    dispatcher.add_handler(CommandHandler('add_account', self.add_account, pass_args=True))
    dispatcher.add_handler(CommandHandler('show_account_data', self.show_account_data))
    dispatcher.add_handler(CommandHandler('calculate_balancing', self.calculate_balancing))
    dispatcher.add_handler(CommandHandler('do_balancing', self.do_balancing))
    dispatcher.add_handler(CommandHandler('export', self.export))
    dispatcher.add_handler(CommandHandler('import_from_file', self.import_from_file))
    dispatcher.add_handler(CommandHandler('easter', self.easter))
    dispatcher.add_handler(CommandHandler('add_event', self.add_event, pass_args=True))
    dispatcher.add_handler(CommandHandler('do_transaction', self.do_transaction, pass_args=True))

    dispatcher.add_error_handler(self.unknown)

    updater.start_polling()
    updater.idle()


  def start(self, bot, update):
    group_id = update.message.chat_id

    found = False

    try:
      self.billingdata.groups[group_id]
      found = True
    except KeyError:
      bot.sendMessage(chat_id=update.message.chat_id, text="Added new group")

    self.billingdata.groups[group_id] = g.Group(group_id)

    if found:
      bot.sendMessage(chat_id=update.message.chat_id, text="Recreated group")

  def add_account(self, bot, update, args):
    """
    add_account {name}
    """
    group_id = update.message.chat_id

    if len(args) != 1:
      bot.sendMessage(chat_id=update.message.chat_id, text="Wrong number of arguments")
      return

    self.billingdata.groups[group_id].add_account(a.Account(args[0]))

  def add_event(self, bot, update, args):
    """
    add_event {amount} {payer} {participants}
    """
    group_id = update.message.chat_id
    logger = logging.getLogger('add_event')
    logger.info("Start add event")

    if len(args) < 2:
      bot.sendMessage(chat_id=group_id, text="This command requires at least two arguments")
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')
      return

    amount = args[0]
    payer = args[1]
    participants = args[1:]

    try:
      self.billingdata.groups[group_id].add_event(e.Event(amount, payer, participants))
      self.export_to_file()

      event = self.billingdata.groups[group_id].get_last_event()
      remainder = event.cost_in_cents % len(event.participants)
      cost_per_person = ( event.cost_in_cents - remainder) / len(event.participants)

      if event.remainder_person == "":
        bot.sendMessage(chat_id=group_id,
          text="{} payed {}€ for {}. The cost per person was {}€." \
          .format(payer, amount, ", ".join(participants), cost_per_person/100))
      else:
        bot.sendMessage(chat_id=group_id,
          text="{} payed {}€ for {}. The cost per person was {}€. The remainder is {}€ and {} had to pay it." \
          .format(payer, amount, ", ".join(participants), cost_per_person/100, remainder / 100, event.remainder_person))

      self.show_account_data(bot, update)
    except g.GroupError as ex:
      bot.sendMessage(chat_id=group_id, text=str(ex))
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')
    except ValueError:
      bot.sendMessage(chat_id=group_id, text="Could not convert {} to an amount".format(amount))
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')


  def do_transaction(self, bot, update, args):
    """
    do_transaction {amount} {source} {destination}
    """
    group_id = update.message.chat_id
    logger = logging.getLogger('do_transaction')
    logger.info("Start do transaction")

    if len(args) != 3:
      bot.sendMessage(chat_id=group_id, text="This command requires three arguments")
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')
      return

    try:
      amount, source, destination = args
      self.billingdata.groups[group_id].do_transaction(t.Transaction(amount, source, destination))
      self.export_to_file()

      bot.sendMessage(chat_id=group_id, text="Transfered {}€ from {} to {}".format(amount, source, destination))
      self.show_account_data(bot, update)

    except g.GroupError as ex:
      bot.sendMessage(chat_id=group_id, text=str(ex))
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')
    except ValueError:
      bot.sendMessage(chat_id=group_id, text="Could not convert {} to an amount".format(args[0]))
      bot.sendSticker(chat_id=group_id, sticker='CAADAwADnQEAAr-MkATNKNQOPN0QfQI')

  def show_account_data(self, bot, update):
    group_id = update.message.chat_id

    text = self.billingdata.groups[group_id].readable_account_data()

    bot.sendMessage(chat_id=group_id, text=text, parse_mode=ParseMode.MARKDOWN)

  def calculate_balancing(self, bot, update):
    group_id = update.message.chat_id
    gr = self.billingdata.groups[group_id]

    text = ""
    transactions = gr.calculate_balancing()

    for trans in transactions:
      text += str(trans) + '\n'

    bot.sendMessage(chat_id=update.message.chat_id, text=text)

  def do_balancing(self, bot, update):
    pass
    #group_id = update.message.chat_id
    #gr = self.billingdata.groups[group_id]

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
    os.rename(self.backup_file, self.backup_file +'_' + '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now()))
    text = yaml.dump(self.billingdata)
    with open(self.backup_file, 'w') as f:
      f.write(text)
    return text

  def import_from_file(self, bot, update):
    group_id = update.message.chat_id

    if group_id != self.private_chat:
      return

    with open(self.backup_file) as f:
      obj = yaml.load(f)

    self.billingdata = obj

  def easter(self, bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="This is an easter egg!")

  def unknown(self, bot, update, error):
    self.logger.info(error)
    if bot is not None and update is not None:
      bot.sendMessage(chat_id=update.message.chat_id, text="I'm sorry, I did not understand your command.")

def main():
  logging.basicConfig(format='%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')
  logging.getLogger().setLevel(logging.INFO)
  logger = logging.getLogger('main')

  logger.info("Initialisiere TelegramBot!")

  # Load configuration
  with open("config.yml") as data_file:
    config = yaml.load(data_file)

  try:
    with open(config["backup_file"]) as f:
      billingdata = yaml.load(f)
      billingdata.update()
  except OSError as e:
    billingdata = b.BillingData()

  bot = AbrechnungsBot(config, billingdata)
  bot.connect_and_run()

  logger.info("Bot initialisiert")

if __name__ == '__main__':
	main()

