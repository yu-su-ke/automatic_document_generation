from pymongo import MongoClient
from getTweets import TweetsGetterBySearch
from getTweets import TweetsGetter
import time
from timeMeasurement import time_measurement
from pathlib import Path

# 検索語ツイート収集準備
word = 'test'
search = u'甲子園'
# 日付指定
since = '2018-08-21_00:00:00_JST'
until = '2018-08-21_23:59:59_JST'
tweets_num = 0

# ユーザツイート収集準備
user = 'Snow12Yuki24'

client = MongoClient('localhost', 27017)

# データベース指定
db = client.mydb

# コレクション指定
save = db[word]
save2 = db[user + '_tweets']

#ファイルパス
current = str(Path())


# 検索語を指定してツイートを取得
def save_database():
    """
    bySearch(u'~~~') : 検索語指定
    collect(total=~~~) : 取得件数
    10000件遅延なし
    18000件(9000件807秒待ち)
    30000件(10200件272秒待ち, 20800件798秒待ち)
    50000件(1:31:10待ち)
    617260件(12時間待ち)
    """
    tweets = TweetsGetter.bySearch(search + ' since:' + since + ' until:' + until).collect(total=tweets_num)
    for tweet in tweets:
        tweet_contents = {}
        '''
        id : ツイートID
        text : テキスト本文
        created_at : ツイート日時
        user : ユーザ名
        follower : フォロワー数
        favorite : いいね数
        retweet : リツイート数
        '''
        tweet_contents['id'] = tweet['id']
        tweet_contents['text'] = tweet['text']
        tweet_contents['created_at'] = tweet['created_at']
        tweet_contents['user'] = tweet['user']['screen_name']
        tweet_contents['follower'] = tweet['user']['followers_count']
        tweet_contents['favorite'] = tweet['favorite_count']
        tweet_contents['retweet'] = tweet['retweet_count']

        # コレクションに追加(コレクションもここで作成)
        save.insert(tweet_contents)


# ユーザを指定してツイートを取得
def user_database():
    with open(current + '/tweet/' + user + '.txt', mode='w', encoding="utf-8") \
            as user_file:
        tweets = TweetsGetterBySearch.byUser(user).collect()
        for tweet in tweets:
            tweet_contents = {}

            tweet_contents['id'] = tweet['id']
            tweet_contents['text'] = tweet['text']
            tweet_contents['created_at'] = tweet['created_at']
            tweet_contents['user'] = tweet['user']['screen_name']
            tweet_contents['follower'] = tweet['user']['followers_count']
            tweet_contents['favorite'] = tweet['favorite_count']
            tweet_contents['retweet'] = tweet['retweet_count']

            # コレクションに追加(コレクションもここで作成)
            save2.insert(tweet_contents)

            # テキストファイルへの書き込み
            user_file.write(tweet_contents['text'] + '\n')


start = time.time()
# save_database()
user_database()
elapsed_time = time.time() - start
print(time_measurement(elapsed_time))
