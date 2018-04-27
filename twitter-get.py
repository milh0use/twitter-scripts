import twitter
import configparser

config = configparser.ConfigParser()
config.read('twitter-auth.config')


api = twitter.Api(consumer_key=config['main']['consumer_key'],
                      consumer_secret=config['main']['consumer_secret'],
                      access_token_key=config['main']['access_token_key'],
                      access_token_secret=config['main']['access_token_secret'])

