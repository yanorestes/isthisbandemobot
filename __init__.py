from bot import TwitterBot
from configparser import ConfigParser
from time import sleep
from datetime import datetime
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.WARNING)
    config = ConfigParser()
    config.read('config.ini')
    emo_bot = TwitterBot(config['Twitter'], config['API']['LAST_ID'])
    run = True
    while run:
        try:
            emo_bot.reply_mentions()
            print('Running...')
            sleep(30)
        except KeyboardInterrupt:
            print('Are you sure you want to kill the bot? (Y/N)')
            if input().upper() == 'Y':
                run = False
            logging.warning('Bot killed by user - {}'.format(datetime.now()))
        finally:
            config['API']['LAST_ID'] = str(emo_bot.since_id)
            with open('config.ini', 'w') as config_file:
                config.write(config_file)
