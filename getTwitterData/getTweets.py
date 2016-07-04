from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from authToken import *

import time

stopWords=[]

with open('en.txt') as swords:
	allWords=swords.readlines()
	for line in allWords:
		stopWords.append(line.strip())
		
punctuationSymbols = ['?','!','.','-','@','\\','#',';','|',':','(',')']

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
			time.sleep(1)

	def on_error(self, status):
		print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track='sport')
