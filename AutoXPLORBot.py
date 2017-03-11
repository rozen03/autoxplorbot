#!/usr/bin/python3
# -*- coding: utf-8 -*-
# TODO: Restringir llamargente de 9 a 23
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram.ext import Job
from tokens import token
from telegram.ext.dispatcher import run_async
from time import sleep
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from telegram.ext import Updater
from telegram.error import (TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError)
logger = logging.getLogger("Bots.log")

def getText(bot, update):
    try:
        text = update.message.text
    except Exception as inst:
        text = update.callback_query.message.text
    return text


def getUser(update):
    user = ""
    try:
        user = update.message.from_user
    except Exception as inst:
        user = getattr(update.callback_query, "from_user")
    return user
def usernameOrFullName(user):
    if not user.username:
        return user.first_name+" "+ user.last_name
    else:
        return user.username
def loguear(texto):
	logger.info(str(texto.encode('utf8')))
@run_async
def register(bot, update):
	loguear(str(usernameOrFullName(getUser(update))) + ": " + getText(bot, update))
def start(bot, update):
	register(bot, update)
	bot.sendMessage(chat_id=update.message.chat_id,text="Try /list or /stats")
def list(bot,update):
	register(bot, update)
	bot.sendMessage(chat_id=update.message.chat_id,text="test - tester")
def stats(bot,update):
	register(bot, update)
	bot.sendMessage(chat_id=update.message.chat_id,text="Total Network: 13m | 18 Accs")


def handlearUpperLower(texto, funcion, dispatcher, botname: str):
    handlr = RegexHandler(
        "^(?i)/" + texto + "(|@" + botname + ")($|\s)",
        funcion,
        pass_groups=False,
        pass_groupdict=False,
        pass_update_queue=False,
        pass_job_queue=False)
    dispatcher.add_handler(handlr)
def main():
	global update_id
	try:
		logging.basicConfig(
				level=logging.INFO,
				#level=logging.DEBUG,
        		format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
        		filename="bots.log")
		loguear("Starting AutoXPLORBot")
		# Telegram Bot Authorization Token
		updater = Updater(token=token)
		dispatcher = updater.dispatcher
		j = updater.job_queue
		start_handler = CommandHandler('start', start)
		dispatcher.add_handler(start_handler)
		comandos = [('list',list),('stats',stats)]
		botname = "AutoXPLORBot"
		for c in comandos:
			handlearUpperLower(c[0], c[1], dispatcher, botname)

		#updater.start_polling(clean=True)
		updater.start_polling()
	except Exception as inst:
		loguear("ERROR INITIALIZING AUTOXPLORBOT")
		result = str(type(inst)) + "\n"    	# the exception instance
		result += str(inst.args) + "\n"     # arguments stored in .args
		# __str__ allows args to be printed directly,
		result += str(inst) + "\n"
		loguear(result)

if __name__ == '__main__':
    main()
