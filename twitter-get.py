import twitter
import configparser
import argparse

parser = argparse.ArgumentParser(description='Get the list of "friends" of a twitter user and add them to a named collection')
parser.add_argument("-u", "--user",
                    help='The user whose friends list should be exported')

args = parser.parse_args()

user = ''
if hasattr(args, 'user') and vars(args)['user'] != None:
    user = vars(args)['user']

config = configparser.ConfigParser()
config.read('twitter-auth.config')

api = twitter.Api(consumer_key=config['main']['consumer_key'],
                      consumer_secret=config['main']['consumer_secret'],
                      access_token_key=config['main']['access_token_key'],
                      access_token_secret=config['main']['access_token_secret'])

print("Scanning Twitter Friends list of " + user)
users = api.GetFriends(screen_name=user)
for user in users:
    print(user.name)
