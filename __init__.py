from bot import TwitterBot
from configparser import ConfigParser
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    config = ConfigParser()
    config.read('config.ini')
    emo_bot = TwitterBot(config['Twitter'], config['API']['LAST_ID'])