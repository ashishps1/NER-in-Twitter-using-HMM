from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import time

#consumer key, consumer secret, access token, access secret.
ckey="ZvghhRGSbIF5AIFdpr7uE9dcx"
csecret="C3Z0a8Z3G8jaRMicos8B0iylW1nLc4yWZNj7zWq1Df9y6TdD4L"
atoken="1676249395-yGwErJNDT8gLe7S3olMAwSjqG4qNCuZ82l2ufUF"
asecret="eqpMpQRO8R9mYV1GtN2hrN1tm5rCvMOR4gk98xV0gh5xK"

stopWords=[]

with open('en.txt') as swords:
	allWords=swords.readlines()
	for line in allWords:
		stopWords.append(line.strip())
		
punctuationSymbols = ['?','!','.','-','@','\\','#',';']

class listener(StreamListener):
	
	def on_data(self, data):
		try:
			tweet=data.split(',"text":"')[1].split('","source')[0]
			print(tweet)
			
			if tweet.split()[0]!='RT':
				tweet=" ".join([w for w in tweet.split() if w.lower() not in stopWords])
				cleanedTweet=[]
				for s in tweet.split():
					cond=True
					for c in s:
						if c in punctuationSymbols:
							cond=False
							break
					if cond:
						cleanedTweet.append(s)
			
				cleanedTweet=" ".join([w for w in cleanedTweet])
				
				if len(cleanedTweet.split())!=0:
					tim=data.split('":"')[1].split('+')[0]
					print(tim)
					saveThis=str(tim) + ' :: ' + str(cleanedTweet)	    	
					saveFile=open('tweetDB.txt','a')
					saveFile.write(saveThis+'\n')
					saveFile.close()
			return True

		except BaseException as e:
			print('failed ondata,',str(e))
			time.sleep(5)

	def on_error(self, status):
		print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["india"])
