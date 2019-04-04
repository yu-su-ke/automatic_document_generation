import MeCab


def mecab_text(text):
    # windows
    # mecab = MeCab.Tagger('-Owakati')
    # mac
    mecab = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
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
