#Simple script to export Twitter stream -> Kafka messages

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

#twitter access tokens - see https://developer.twitter.com/en/apps 
#these are secret keys and so need to be obtained by the user.
access_token = "XXX"
access_token_secret =  "XXX"
consumer_key =  "XXX"
consumer_secret =  "XXX"


#simple class that will take the twitter stream and publish messages
class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("tweets", data.encode('utf-8'))
        return True
    def on_error(self, status):
        print (status)


#Create the connection to Kafka and the producer for publishing messages
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

#create the stream
twitterStream = TwitterStreamListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, twitterStream)

#for the purposes of the demo limit to English and only those tweets containing the keyword(s) 
# A particular set of users tweets can be filtered via follow - see tweepy API and 
# https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
# for some of the options available.
stream.filter(languages=["en"],track=["Lady Gaga"])


