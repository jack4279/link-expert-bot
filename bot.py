from telegram.ext.dispatcher import run_async
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackQueryHandler,InlineQueryHandler
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,InputTextMessageContent,InlineQueryResultArticle
import logging
import os
import unshortenit
from unshortenit import UnshortenIt
import pyshorteners
import re
from uuid import uuid4


Api_key=os.environ.get("api_key","")
s=pyshorteners.Shortener(api_key=Api_key)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update,context):
    first=update.message.chat.first_name
    update.message.reply_text('Hi! '+str(first)+' \n\nWelcome to Link Expert Bot.\nThis bot can short long urls , and also unshort various short urls type /help to know how to use this bot.')

inlinekeyboard=[[InlineKeyboardButton("Go inline in other chats", switch_inline_query="")]]
switch_inline=InlineKeyboardMarkup(inlinekeyboard)
@run_async   
def help(update,context):
    update.message.reply_text('Just send the url that you want to short or unshort \nYou can also use this bot in other chats by using inline mode, click below button to go inline in other chats.\n\nNote:<i>⚠️ Url must start with http:// or https:// and it should not have spaces in it.</i>',parse_mode=telegram.ParseMode.HTML,reply_markup=switch_inline)

@run_async
def convert(update,context):
    global link
    remove = update.message.text
    URLless_string = re.sub(r'http\S+', '', stringliteral)
    link= (re.search("(?P<url>https?://[^\s]+)", remove).group("url"))
    unshortener=UnshortenIt()
    uri=unshortener.unshorten(link)
    pattern1="https://*"
    pattern2="http://*"
    if(re.search(pattern1,link)) or (re.search(pattern2,link)):
        keyboard = [[InlineKeyboardButton("Unshort", callback_data='unshort')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(URLless_string +"\n" + uri, reply_markup=reply_markup)
    else:
        update.message.reply_text("<i>⚠️ Url must start with http:// or https:// and it should not have spaces in it.</i>",parse_mode=telegram.ParseMode.HTML)

@run_async
def button(update,context):
    query=update.callback_query
    query.answer()
    a=query.data
    if a=="unshort":
        unshortener=UnshortenIt()
        uri=unshortener.unshorten(link)
        query.edit_message_text(text="Unshorted url 👇🏼 : \n"+str(uri))
    if a=="short":
        unshortener=UnshortenIt()

        uri=unshortener.unshorten(link)

        query.edit_message_text(text="Unshorted url 👇🏼 : \n"+str(uri))

def inlinequery(update,context):
	query = update.inline_query.query
	###for short links#######
	shortlink=s.bitly.short(query)
	#####for unshort link####$#$
	unshortener=UnshortenIt()
	unshortlink=unshortener.unshorten(query)
	
	results=[InlineQueryResultArticle(id=uuid4(),title="short",input_message_content=InputTextMessageContent(shortlink), description="Click to shorten the link"),
                     InlineQueryResultArticle(id=uuid4(),title="unshort",input_message_content=InputTextMessageContent(unshortlink), description="Click to unshort the link")]
	update.inline_query.answer(results)
		



def main():
    token=os.environ.get("bot_token","")
    updater = Updater(token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))

    dp.add_handler(MessageHandler(Filters.text,convert))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
