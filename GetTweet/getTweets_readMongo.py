from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# データベース指定
db = client.mydb

# コレクション指定
collection = 'afpbbcom'
document_num = 1000

count = db[collection + '_tweets'].find().limit(document_num)

open_path = './tweet/'


# 書き込みファイル指定(確認用)
def confirm_tweets():
    cnt = 0
    with open(open_path + collection + '.txt', mode='w', encoding="utf-8") as text_file:
        for record in count:
            cnt += 1
            # データベース内のツイート情報表示
            print('------ %d' % cnt)

            # テキストファイルへの書き込み
            text_file.write(record['text'] + '\n')


confirm_tweets()
