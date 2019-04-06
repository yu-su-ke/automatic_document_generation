import MeCab
import platform


def mecab_lstm(text):
    pf = platform.system()
    if pf == 'Windows':
        mecab = MeCab.Tagger('-Owakati')
    elif pf == 'Darwin':
        mecab = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    elif pf == 'Linux':
        mecab = MeCab.Tagger("-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd/")

    mecab.parse("")
    split_text = ""
    output = []

    breaking_chars = ['(', ')', '[', ']', '"', "'"]

    # split whole text to sentences by newline, and split sentence to words by space.
    for line in text.split():
        mp = mecab.parseToNode(line)
        while mp:
            try:
                if mp.surface not in breaking_chars:
                    split_text += mp.surface    # skip if node is markovify breaking char
                if mp.surface != '。' and mp.surface != '、':
                    split_text += ' '    # split words by space
                if mp.surface == '。':
                    split_text += '\n'    # reresent sentence by newline
            except UnicodeDecodeError as e:
                # sometimes error occurs
                print('(error)' + line)
            finally:
                if mp != 'None':
                    output.append(mp.surface)
                mp = mp.next

    # print(output)
    return split_text
