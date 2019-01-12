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
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error: Authentication Failed")
def loadTweets(dir_path_of_tweets):
    if not os.path.isdir('all_tweets_withGeoData_dump/'):
        os.makedirs('all_tweets_withGeoData_dump/')
    geo_tweets = []
    json_tweets_files = [file for file in os.listdir(dir_path_of_tweets)]
    #print json_tweets_files
    for file in json_tweets_files:
        if not (os.path.exists("all_tweets_withGeoData_dump/"+ str(file[:-5]) +"_geo_tweets.json")):
            with open(str(dir_path_of_tweets)+file) as json_tweet:
                tweets = json.load(json_tweet)
                for tweet in tweets:
                    if (tweet['coordinates'] != None) or (tweet['place'] !=None) or (tweet['geo'] !=None):
                        geo_tweets.append(tweet)
                        #print json.dumps(geo_tweets)
                        #exit()
                    geo_tweets_str = json.dumps(geo_tweets)
                    #','.join(str(tweet) for tweet in geo_tweets)
                    #print geo_tweets_str
            if geo_tweets != []:
                print "found a geo tweet...."
                with open('all_tweets_withGeoData_dump/'+str(file[:-5])+'_geo_tweets.json','w') as geo_file:
                    #print type(geo_tweets)
                    #exit()
                    #geo_file.write('[')
                    #geo_file.write(','.join(geo_tweets_str))
                    geo_file.write(geo_tweets_str)
                    #print geo_tweets_str
                    #geo_file.write(']')
                    geo_tweets = []
                    geo_tweets_str = ''
                exit()
    return

def main():
    # creating object of TwitterClient Class
    #twitterConnect = TwitterClient()
    #tweet = twitterConnect.api.get_status('1076443602325258240')
    #print type(tweet.entities.media[display_url])
    dir_path_of_tweets = "all_tweets_dump/"
    loadTweets(dir_path_of_tweets)
    exit()
    #tweet = twitter.show_status(id='1076443602325258200')
    #print(tweet.media)
if __name__ == "__main__":
    # calling main function
    main()