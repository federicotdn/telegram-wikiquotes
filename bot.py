from telegram.ext import Updater, CommandHandler
import wikiquote
import random
import logging

LANGS = wikiquote.supported_languages()
MAX_QUOTES = 100
DEFAULT_LANG = 'en'

with open('token.txt') as f:
    apiToken = f.read()

def lang_and_terms(args):
    if not args:
        return DEFAULT_LANG, []
    
    if args[0] in LANGS:
        return args[0], args[1:]
    
    return DEFAULT_LANG, args

def start(bot, update):
    update.message.reply_text('Hello, I\'m the Wikiquote bot.')

def qotd(bot, update, args):
    lang, terms = lang_and_terms(args)
    try:
        quote, author = wikiquote.quote_of_the_day(lang=lang)
        reply = '"' + quote + '" - ' + author
        update.message.reply_text(reply)
    except:
        update.message.reply_text('An error occured when fetching the quote of the day.')   

def quote(bot, update, args):
    lang, terms = lang_and_terms(args)
    if not terms:
        update.message.reply_text('Usage: /quote <article>')
        return
    
    try:
        quotes = wikiquote.quotes(' '.join(terms), lang=lang, max_quotes=MAX_QUOTES)
        if not quotes:
            update.message.reply_text('No quotes found.')
        else:
            reply = '"' + random.choice(quotes) + '"'
            update.message.reply_text(reply)
    except wikiquote.utils.DisambiguationPageException as e:
        update.message.reply_text('Try using a more specific article title.')
    except:
        update.message.reply_text('An error occured when fetching quotes from Wikiquote.org.')

def search(bot, update, args):
    lang, terms = lang_and_terms(args)
    if not terms:
        update.message.reply_text('Usage: /search <terms>')
        return
    
    try:
        results = wikiquote.search(' '.join(terms), lang=lang)
        if not results:
            update.message.reply_text('No results found.')
        else:
            reply = 'Results:\n'
            for result in results:
                reply += ' - ' + result + '\n'

            update.message.reply_text(reply)
    except:
        update.message.reply_text('An error occured when searching Wikiquote.org.')

updater = Updater(apiToken)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('quote', quote, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('search', search, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('qotd', qotd, pass_args=True))

updater.start_polling(poll_interval=1.0)
updater.idle()