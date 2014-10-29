import ConfigParser
import os.path
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import threading
import time
import liblo
import sys


targetYes = None
targetNo = None


#Connect to the arduino Yes
try:
    targetYes = liblo.Address(1234)
except liblo.AddressError, err:
    print str(err)
    sys.exit()

#Connect to the arduino No
try:
    targetNo = liblo.Address(1235)
except liblo.AddressError, err:
    print str(err)
    sys.exit()



# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
#consumer_key=""
#consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
#access_token=""
#access_token_secret=""

#auth = OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)




### SETUP CONFIG
config = ConfigParser.ConfigParser()
#Read file if exists
if os.path.isfile("counter.cfg"):
     config.read("counter.cfg")

currentDate = time.strftime("%d-%m-%Y")

if not config.has_section(currentDate):
     config.add_section(currentDate)
     config.set(currentDate,"yes",0)
     config.set(currentDate,"no",0)
     config.write(open("counter.cfg","wb"))

if config.has_section("app"):
     consumer_key = config.get("app","consumer_key")
     consumer_secret = config.get("app","consumer_secret")
     access_token = config.get("app","access_token")
     access_token_secret = config.get("app","access_token_secret")
    
     TAG_ONE = config.get("app","targetOne")# "yes"
     TAG_TWO = config.get("app","targetTwo") #"no"
     TWITTER_ACCOUNT = config.get("app","twitter_user")#"musofsharednow"
else:
     print "No config to start the installation"
     sys.exit()    


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


totalYes = config.getint(currentDate,"yes")
totalNo = config.getint(currentDate,"no")

print "total",totalYes,totalNo 

def addCount(tYes,tNo):
    global totalYes, totalNo
    doYes = True  if tYes > 0 else False
    doNo = True if tNo > 0 else  False
    
    totalYes += tYes
    totalNo += tNo
    config.set(currentDate,"yes",totalYes)
    config.set(currentDate,"no",totalNo)
    config.write(open("counter.cfg","wb"))
    print "total",totalYes,totalNo
    if doYes:
         liblo.send(targetYes,"/update",totalYes)
    if doNo:
         liblo.send(targetNo,"/update",totalNo)



#Init arduino
liblo.send(targetYes,"/update",totalYes)
liblo.send(targetNo,"/update",totalNo)



### SETUP TWITTER

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def parseData(self,data):
        #print data
        jdata = json.loads(data)
        #print jdata
        if "user" in jdata:
             if jdata['user']['screen_name'] != TWITTER_ACCOUNT: #If the tweet comes from the same user, discare it
                 print "Tweet from someone ",jdata['text']
             else:  #We dont care about the account's tweets
                 print "Tweet from himself"
                 return True
             hash = jdata['entities']['hashtags'] #Getting all hashtags from the post
             if (len(hash) > 0):
                 foundHashOne = False
                 foundHashTwo = False
                 for h in hash: #Parsing hashtags
                      if h['text'].lower() == TAG_ONE:
                           foundHashOne = True
                      if h['text'].lower()  == TAG_TWO:
                           foundHashTwo = True
                 if foundHashOne and foundHashTwo:  #No valid tweet if there are both hashtags
                      print "no valid tweet"
                 elif foundHashOne or foundHashTwo: #Found only one of the two, this is a valid tweet
                      if foundHashOne: 
                          addCount(1,0)
                      else:
                          addCount(0,1)
                      print "Valid twtter", foundHashOne, foundHashTwo
                 else: #No hashtag found in the tweet
                      print "no hash tag.."
             else: #No hashtag found in the tweet
                  print "no hash tag.."
        else: #This is not a tweet, just other info
	     print "Not a tweet", jdata
       

    def on_data(self, data):
        try:
             self.parseData(data)
        except:
             print "error parse"
        return True

    def on_error(self, status):
        print "Error twitter: ",status


follow = ['']
track  = ['']
l = StdOutListener()


stream = Stream(auth, l)
stream.userstream(TWITTER_ACCOUNT)
stream.filter(track = track, follow = follow)
