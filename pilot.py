import re
import tweepy
import os
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import json
import ConfigParser
 
class TwitterClient(object):
    '''
    Generic Twitter Class
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        config = ConfigParser.ConfigParser()
        config.read('connection.conf')
        # keys and tokens from the Twitter Dev Console
        consumer_key = str(config.get('CONN','consumer_key'))
        consumer_secret = str(config.get('CONN','consumer_secret'))
        access_token = str(config.get('CONN','access_token'))
        access_token_secret = str(config.get('CONN','access_token_secret'))
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            print("Error: Authentication Failed")
    def getFriends(self,screen_name):
        '''
        To get the all my friend list as {user_id:screen_name}
        '''
        print ("Collecting all friends...")
        API = self.api
        my_screen_name = API.me().screen_name
        #print my_screen_name
        friends_user_ids = API.friends_ids(my_screen_name)
        #print API.friends_ids('7de9pk')
        friends_screen_name = [API.get_user(id).screen_name.encode('ascii') for id in friends_user_ids]
        all_friends = dict(zip(friends_user_ids, friends_screen_name))
        #np.save('my_friends_id_n_screenName',id_and_screen_name)
        with open('my_friends_id_n_screenName.json', 'w') as file:
            file.write(json.dumps(all_friends))
        print ("Done collecting friends..")
        return all_friends
    def persistTimelineTweets(self, id, screen_name):
        '''Persists all the tweets of my friends in json files to disk'''
        print("Persisting "+screen_name+"'s tweets to disk..")
        if not (os.path.exists("all_tweets_dump/"+ str(screen_name) +"_"+str(id)+".json")):
            print ("all_tweets_dump/"+ str(screen_name) +"_"+str(id)+".json")
            #print("Persisting "+screen_name+"'s tweets to disk..")
            tweets = [json.dumps(tweet._json) for tweet in tweepy.Cursor(self.api.user_timeline, id = id).items()]
            file_name = 'all_tweets_dump/'+str(screen_name)+"_"+str(id)+".json"
            with open (file_name,'w') as file:
                #file.write(json.dumps(tweets))
                file.write('[')
                file.write(','.join(tweets))
                file.write(']')
            print ("done...")
        else:   
            print ("already present..")
def main():
    # creating object of TwitterClient Class
    twitterConnect = TwitterClient()
    all_friends = twitterConnect.getFriends(twitterConnect.api.me())

    #all_friends = {"1027086041998450688": "BTC_Macro", "856582889768615936": "fireice_uk", "947262969141977090": "brazukcoin"}
    for id, screen_name in all_friends.items():
        #print (str(id)+":"+str(screen_name)+"\n")
        twitterConnect.persistTimelineTweets(id, screen_name)
    #tweets = twitterConnect.api.user_timeline(screen_name = '7de9pk', count =1000)
if __name__ == "__main__":
    # calling main function
    main()