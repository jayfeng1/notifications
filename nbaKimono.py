# -*- coding: utf-8 -*-
"""
@author: Jay
"""

import json
import urllib
import tweepy

#Authenticate the login
def login():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    oauth_token = ''
    oauth_token_secret = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(oauth_token, oauth_token_secret)    
    return auth
   
#Call's the API at the URL and return the results
def callApi(url):
    results = json.load(urllib.urlopen(url))
    #Return the list of games. Extra nested values in the front that don't pertain. 
    return results['results']['collection1']

def wiregame(games):
    wire = []
    for game in games:
        gt = game['time']['text']
        #Find out if the game is actually playing
        if ':' in gt and 'PT' not in gt:
            time, quarter = str(gt).split('-')
            home = int(game['home_score']['text'])
            away = int(game['away_score']['text'])
            #Check if it's the 4th quarter, under 6 minutes to go, and socre differential under 7 points. 
            if quarter.strip() == '4th' and int(time[0]) < 6 and abs(home-away) < 7:
                wire.append(gt + ": " + game['home_team']['text'] + " " + \
                    str(home) + " - " + game['away_team']['text'] + " " + 
                    str(away) + ". GAME IS COMING DOWN TO THE WIRE.") 
    return wire
    
if __name__=='__main__':
    url = "https://www.kimonolabs.com/api/5c8gx236?apikey=[YOUR API KEY]"  
    games = callApi(url)
    msgs = wiregame(games)
    api = tweepy.API(login())
    #If there's a game going on, update the status
    if len(msgs) > 0:
        print msgs
        for msg in msgs:
            api.update_status(status=msg) 
    else:
        print 'NO GAMES'
            
            
        

#CRAIGSLIST HOUSING REMINDER
