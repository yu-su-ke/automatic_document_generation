import MeCab

mecab = MeCab.Tagger('')
print(mecab.parse("私はリンゴを食べるのが好きです"))
