# Script to measure retweet bot activity on a target account and capture suspected bot usernames
# By Lawrence Alexander @LawrenceA_UK

import tweepy
import argparse
import csv


ap = argparse.ArgumentParser()
ap.add_argument("-u","--username",    required=True,help="Enter username of target Twitter account.")
args = vars(ap.parse_args())
searchuser = args['username']


# Set Twitter API credentials

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# CSV file to save bot data to:

outCSV= 'retweet_bots.csv'

# Text file to log suspected bot usernames:

botsLogFile = "bot_accounts.txt"


# Iterate through account's recent statuses

retweeters = []


print "Searching timeline of account: " + searchuser


for status in tweepy.Cursor(api.user_timeline, id = searchuser).items(20):
    if status.retweet_count > 0:
        
        num_retweets=status.retweet_count
        
        retweets = api.retweets (id=status.id)
        
        # Get usernames of retweeters
        
        for x in range (-2,4):            
            try:
                screen_name = retweets.__getitem__(x).user.screen_name
                retweeters.append(screen_name)
                
            except:                
                break
           
# Check timeline to see if recent tweets are all retweets, if so flag as potential bot     
       
def botcheck(username, bot_score):
    rt = 0    
    bot_score = 0
    count = 0
        
    for tweet in tweepy.Cursor(api.user_timeline, id = username).items(30):       
                
        try:
            text = tweet.retweeted_status.truncated
            client = tweet.source
            rt=rt+1
            pass
                                
        except:
            botcheck.bot_score = 0            
            return bot_score
                
        count=count + 1
        
        if count == 30:   
            
            botcheck.bot_score = rt      
           
            return (bot_score)


# Iterate through target's recent retweeters checking for potential retweet bots


bot_hit = 0

# Remove any duplicate entries

retweeters = list(set(retweeters))

botsFound = []
for retweeter in retweeters:
    
    botcheck(username = retweeter, bot_score = "")
    
    if botcheck.bot_score > 29: 
        
        print "Found potential retweet bot: " + retweeter
        
        bot_hit=bot_hit + 1
        
        botsFound.append(retweeter)
        pass
    

num_accounts=len(retweeters)

percent = int(100 * float(bot_hit)/float(num_accounts))

print "User: " + searchuser + " has " + str(bot_hit) + " possible bot accounts out of " + str(len(retweeters)) + " retweeters ("+ str(percent)+"%)"


# Write results to a CSV file

with open(outCSV, 'a') as botstats:
    
    twitterbots = csv.writer(botstats, delimiter=',', lineterminator='\n', dialect='excel')
    
    twitterbots.writerow([searchuser] + [percent] + [num_accounts])
    
    botstats.close()

# Append detected bots to logfile

botLog = open(botsLogFile, "a")
botLog.write("=== Bots retweeting: "+ searchuser +" ==="+"\n")

for account in botsFound:
    botLog.write(account +"\n")

botLog.close()    