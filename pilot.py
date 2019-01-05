import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import json
import ConfigParser
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        config = ConfigParser.ConfigParser()
        config.read('connection.conf')
        # keys and tokens from the Twitter Dev Console
        consumer_key = str(config.get('CONN','consumer_key'))
        print consumer_key
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
            self.api = tweepy.API(self.auth)
            print ("authentication successfull")
        except:
            print("Error: Authentication Failed")
    def getFriends(self,screen_name):
        '''
        To get the friends list as {user_id:screen_name}
        '''
        API = self.api
        my_screen_name = API.me().screen_name
        #print my_screen_name
        friends_user_ids = API.friends_ids(my_screen_name)
        #print API.friends_ids('7de9pk')
        friends_screen_name = [API.get_user(id).screen_name.encode('ascii') for id in friends_user_ids]
        id_and_screen_name = dict(zip(friends_user_ids, friends_screen_name))
        np.save('my_friends_id_n_screenName',id_and_screen_name)
        with open('my_friends_id_n_screenName.txt', 'w') as file:
            file.write(json.dumps(id_and_screen_name))
        return id_and_screen_name
#def getTimelineTweets(screen_name):

def main():
    # creating object of TwitterClient Class
    twitterConnect = TwitterClient()
    #id_and_screen_name = twitterConnect.getFriends(twitterConnect.api.me())
    #searched_tweets = twitterConnect.api.search(q="bitcoin",count=1,)
    #print searched_tweets[0]
    tweets = twitterConnect.api.user_timeline(screen_name = '7de9pk', count =1000)
    print len(tweets)
    print type(tweets)
    exit()

if __name__ == "__main__":
    # calling main function
    
    main()