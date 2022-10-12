import tweepy
import os
import sys
import geocoder
import create_pdf as pdf
from datetime import date,datetime

#set environment variables using following lines
os.environ['api_key'] = api_key
os.environ['api_key_secret'] = api_key_secret
os.environ['api_token'] = api_token
os.environ['api_token_secret'] = api_token_secret

def get_api(**kwargs):
    """Gets the API object after authorization
    and authentication.
    :keyword api_key: The consumer API key.
    :keyword api_key_secret: The consumer API key secret.
    :keyword access_token: The access token.
    :keyword access_token_secret: The access token secret.
    :returns: The Tweepy API object.
    """
    auth = tweepy.OAuthHandler(kwargs["api_key"], kwargs["api_key_secret"])
    auth.set_access_token(
        kwargs["access_token"],
        kwargs["access_token_secret"]
        )
    return tweepy.API(auth)


def get_trends(api, loc):
    """Gets the trending search results from Twitter.
    :param api: The Tweepy API object.
    :param loc: The location to search for.
    :returns: A dictionary of trending search results.
    """
    # Get available locations that have trends.
    # available_loc = api.available_trends()

    # Object that has location's latitude and longitude.
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    #print(trends)
    return trends[0]["trends"]


def extract_hashtags(trends):
    """Extracts the hashtags from the trending search results.
    :param trends: A list of trending search results.
    :returns: A lisselft of hashtags.
    """
    hashtags = [trend["name"] for trend in trends if "#" in trend["name"]]
    return hashtags


def get_n_tweets(api, hashtag, n, lang=None):
    """Gets the n tweets of the trending hashtag.
    :param api: The Tweepy API object.
    :param hashtag: The trending hashtag.
    :param n: The number of tweets to get.
    :returns: A string of the status.
    """
    for status in tweepy.Cursor(
        api.search_tweets,
        q=hashtag,
        lang=lang
    ).items(n):
        print(f"https://twitter.com/i/web/status/{status.id}")

def analyse(data):
    dic1={}
    dic2={}
    for i in data:
        #if i['name'][1:].isalpha():
        if i['tweet_volume'] is not None:
            dic1[i['name']]=i['tweet_volume']
        else:
            dic2[i['name']]=i['tweet_volume']
    return dic1,dic2

if __name__ == "__main__":
    api = get_api(
        api_key=os.getenv('api_key'),
        api_key_secret=os.getenv('api_key_secret'),
        access_token=os.getenv('api_token'),
        access_token_secret=os.getenv('api_token_secret')
    )
    loc = input("Enter country name to get trends -> ")
    trends = get_trends(api, loc)
    dic1,dic2=analyse(trends)
    dic3={}
    dic3['country']=str(loc)
    today=date.today()
    now=datetime.now()
    dic3['datetime']=str(today.strftime("%B %d, %Y"))+" "+str(now.strftime("%H:%M:%S"))
    pdf.write_pdf(dic1,dic2,dic3)
    #hashtags = extract_hashtags(trends)
    #for hashtag in hashtags:
    #    print(hashtag)
    #hashtag = hashtags[0]
    #status = get_n_tweets(api, hashtag, 5, "ar")