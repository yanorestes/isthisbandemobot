from isthisbandemo import get_itbe_answer, get_tmp_img
from traceback import format_exc
import tweepy
import re
import logging


class TwitterBot:
    mention_regex = re.compile(r'is (.*) emo\?', re.IGNORECASE)

    def __init__(self, credentials, since_id):
        self.auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'],
                                        credentials['CONSUMER_SECRET'])
        self.auth.set_access_token(credentials['ACCESS_KEY'],
                                   credentials['ACCESS_SECRET'])
        self.api = tweepy.API(self.auth)
        self.since_id = since_id

    def _get_mentions(self, since_id):
        mentions = self.api.mentions_timeline(since_id=since_id, count=100)
        return mentions

    def reply_mentions(self):
        recent_mentions = self._get_mentions(self.since_id)
        try:
            for mention in recent_mentions[::-1]:
                match = TwitterBot.mention_regex.search(mention.text)
                if match:
                    band = match.group(1)
                    answer, img_url = get_itbe_answer(band)
                    if img_url:
                        filename, img = get_tmp_img(img_url)
                        self.api.update_with_media(filename, answer, mention.id, file=img)
                        img.close()
                    else:
                        self.api.update_status(answer, mention.id)
        except:
            logging.error(format_exc())
        finally:
            self.since_id = mention.id

