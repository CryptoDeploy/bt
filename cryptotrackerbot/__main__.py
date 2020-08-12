
import logging
import sys
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters)

from cryptotrackerbot import commands


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    if len(sys.argv) == 2:
        bot_token = sys.argv[1]
    else:
        print("\n!WARNING!:\nadd the bot token as paramter when running the bot.\nExiting...")
        sys.exit(0)

    print("\nrunning...")
    # define the updater
    updater = Updater(token=bot_token, workers=10)
    
    # define the dispatcher
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler(('uprice', 'p'), commands.price_command, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler(('start', 'help'), commands.help, pass_job_queue=True))
    dp.add_handler(CommandHandler(('rank', 'r'), commands.rank_command, pass_job_queue=True))
    dp.add_handler(CommandHandler(('graph', 'g'), commands.graph_command, pass_args=True, pass_job_queue=True))


    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
