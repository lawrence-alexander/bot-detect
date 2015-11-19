# Script to gather usernames of all accounts being retweeted based on a list of users
# Lawrence Alexander @LawrenceA_UK

import tweepy
import csv

# Set your Twitter API credentials

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Name of file containing target usernames to examine

inputfile = 'Bots Master List.txt'

# Name of CSV file to write to

outputfile = 'retweeted_accounts.csv' 
       
def GetRetweetAccounts(username, retweeted_users):
    
    retweets = []
    
    try:
            for tweet in tweepy.Cursor(api.user_timeline, id = username).items(30):       
                    
                try:                      
                    account=tweet.retweeted_status.user.screen_name
                    retweets.append(account)            
                    pass
                                        
                except:
                    print "Gap in retweets found, skipping user:" + username                    
                    return retweeted_users
    except:
        
        print "Couldn't get account: " + username
        GetRetweetAccounts.retweeted_users = ''
        return retweeted_users
    
    GetRetweetAccounts.retweeted_users=retweets 
    
    return retweeted_users

RT_Accounts = []

# Process list of target accounts and build list of accounts retweeted by them

with open(inputfile) as infile:
    
    for account in infile:
        
        print "Getting retweeted accounts for user: " + account
        GetRetweetAccounts(username = account, retweeted_users = "")                    
        try:
            RT_Accounts.extend(GetRetweetAccounts.retweeted_users)
        except:
            RT_Accounts.extend("Unreadable")
        
# Append results to a CSV file

with open(outputfile, 'a') as retweet_accounts:
    retweeted = csv.writer(retweet_accounts, delimiter=',', lineterminator='\n', dialect='excel')
    
    for userID in RT_Accounts:
        retweeted.writerow([userID])
        
    retweet_accounts.close()


print "Capture complete. Retrieved " + str(len(RT_Accounts)) + " user names."