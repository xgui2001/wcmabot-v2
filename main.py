import time
import tweepy
import helper

wcma_hashtag = '#WilliamsCollegeMuseumOfArt'
FILE_NAME = 'log.txt'


# get api credentials from twitterkeys
def get_api():
    all_keys = open('twitterkeys', 'r').read().splitlines()
    api_key = all_keys[0]
    api_key_secret = all_keys[1]
    bearer_token = all_keys[2]
    access_token = all_keys[3]
    access_token_secret = all_keys[4]

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    client = tweepy.Client(bearer_token, api_key,
                           api_key_secret, access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

# create a tweet that has an image


def tweet(api: tweepy.API, message: str, image_path=None):
    if image_path:
        api.update_status_with_media(message, image_path)
    else:
        api.update_status(message)
    return 0


# This function will open the text file and return the ID of
# the latest tweet the bot has successfully replied to
def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')  # open the file in read mode
    # read the Tweet ID as an integer
    last_seen_id = int(file_read.read().strip())
    file_read.close()  # close file reader
    return last_seen_id  # return the result

# Overwrite the previous Tweet ID with latest


def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')  # open the file in write mode
    file_write.write(str(last_seen_id))  # write the ID as a string
    file_write.close()  # close file writer
    return  # return void


def reply():
    # The API will only send a response containing tweets with IDs that come after the ID
    # stored in the text file
    tweets = api.mentions_timeline(
        read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        if '#wcmabot' in tweet.full_text.lower():
            print("Hello!: " + str(tweet.id) +
                  " - " + tweet.full_text.lower())
            api.update_status(
                status="Hello!: " + str(tweet.id) +
                " - " + tweet.full_text.lower(),
                in_reply_to_status_id=tweet.id,)

        elif '#wcmabot' not in tweet.full_text.lower():
            print("Liked!: " + str(tweet.id) + " - " + tweet.full_text.lower())

        store_last_seen(FILE_NAME, tweet.id)
        api.create_favorite(tweet.id)  # Like the tweet with mentions


# verify api authentication and tweet out object every 20 minutes
if __name__ == "__main__":
    api = get_api()
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    while True:
        tweet(api, helper.generate_object() +
              ' \n' + wcma_hashtag)
        reply()
        time.sleep(1200)
