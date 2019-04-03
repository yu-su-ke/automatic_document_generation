import MeCab
import re


class SeparateSentence:
    def __init__(self, save, date):
        self.save = save
        self.date = date

    def noun(self):
        for tweet in self.save:
            if self.date in str(tweet['created_at']):
                t = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
                t.parse('')
                node = t.parseToNode(tweet['text'])
                output = []
                # カウントからはじく単語を指定
                stop_words = [u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
                              u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', u'思う', u'ます',
                              u'それ', u'ここ', u'ちゃん', u'くん', u'って', u'て', u'に', u'を', u'は', u'の', u'が', u'と', u'た', u'し', u'で',
                              u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'から', u'けど',
                              'https', 't', '.', '/', '://', 'co', '@', '_', 'http',
                              '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                              '()', '！']
                while node:
                    if node.surface != "":  # ヘッダとフッタを除外
                        word_type = node.feature.split(",")[1]
                        word_type2 = node.feature.split(",")[2]
                        if word_type in ["固有名詞"] and node.surface not in stop_words:
                            output.append(node.surface)
                            # print(node.surface)
                            return node.surface
                        # if word_type2 in ["人名", "地域"] and node.surface not in stop_words:
                        #     output.append(node.surface)
                        # elif word_type2 in ["組織"] and node.surface.isalpha() is False:
                        #     output.append(node.surface)
                    node = node.next
                    if node is None:
                        break

                # print(output)
                # return self.format_text(str(output))

    def format_text(self, text):
        text = re.sub(r'[!-~]', '', text)
        return text
