import twitter
import configparser
import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='Get the list of "friends" of a twitter user and add them to a named collection')
parser.add_argument("-u", "--user",
                    help='The user whose friends list should be exported', required=True)
parser.add_argument("-c", "--collection",
                    help='The collection to which the user\'s followers should be added', required=True)

args = parser.parse_args()

mongoclient = MongoClient()
db = mongoclient.twitter
coll = db.candidates

user = ''
if hasattr(args, 'user') and vars(args)['user'] != None:
    user = vars(args)['user']
if hasattr(args, 'collection') and vars(args)['collection'] != None:
    collection = vars(args)['collection']

config = configparser.ConfigParser()
config.read('twitter-auth.config')

api = twitter.Api(consumer_key=config['main']['consumer_key'],
                      consumer_secret=config['main']['consumer_secret'],
                      access_token_key=config['main']['access_token_key'],
                      access_token_secret=config['main']['access_token_secret'])

users_collection = dict()
# check if we already have a collection in Mongo
collection_document = coll.find_one({"collection": collection})

if type(collection_document) is dict:
    users_collection = collection_document['users_collection']
else:
    print("The object type returned by Mongo was ", type(users_collection))

print("Scanning Twitter Friends list of " + user)

users = api.GetFriends(screen_name=user)
for user in users:
    users_collection[user.screen_name] = user.name

coll.update_one({"collection": collection},{'$set': {'users_collection': users_collection}},upsert = True)

