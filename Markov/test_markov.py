from glob import iglob
import sys
import MeCab
import markovify
import datetime
import pathlib
# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append( str(current_dir) + '/../' )
from text_format import text_format


def load_from_file(files_pattern):
    # read text
    text = ""
    for path in iglob(files_pattern):
        with open(path, 'r', encoding="utf-8") as f:
            text += f.read().strip()

    return text


def split_for_markovify(text):
    # separate words using mecab
    # windows
    mecab = MeCab.Tagger('-Owakati')
    # mac
    # mecab = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    splitted_text = ""

    breaking_chars = ['(', ')', '[', ']', '"', "'"]

    # split whole text to sentences by newline, and split sentence to words by space.
    for line in text.split():
        mp = mecab.parseToNode(line)
        while mp:
            try:
                if mp.surface not in breaking_chars:
                    splitted_text += mp.surface    # skip if node is markovify breaking char
                if mp.surface != '。' and mp.surface != '、':
                    splitted_text += ' '    # split words by space
                if mp.surface == '。':
                    splitted_text += '\n'    # reresent sentence by newline
            except UnicodeDecodeError as e:
                # sometimes error occurs
                print('(error)' + line)
            finally:
                mp = mp.next

    return splitted_text


def main():
    # ファイルパス
    document_type = 'tweet'
    text_file = 'afpbbcom'

    open_path = '../' + document_type + '/'
    format_path = '../' + document_type + '/format/'
    save_path = '../' + document_type + '/markov/'
    text_format(open_path, format_path, text_file, document_type)
    text_data = load_from_file(format_path + text_file + '_format.txt')
    # 現在時刻
    now = datetime.datetime.now()
    now_time = '{0:%Y_%m_%d %H:%M:%S}'.format(now)
    # ファイル更新
    file = open(save_path + text_file + '_markov' + '.txt', 'a+', encoding='utf-8').write('\n' + now_time + '\n')

    # split text to learnable form
    splitted_text = split_for_markovify(text_data)

    # learn model from text.
    # rangeの中身は実行回数
    for i in range(5):
        text_model = markovify.NewlineText(splitted_text, state_size=2)
        # ... and generate from model. tries default 10
        sentence = text_model.make_sentence(tries=10)
        if str(sentence) != 'None':
            print(''.join(sentence.split()))    # need to concatenate space-splitted text
            with open(save_path + text_file + '_markov.txt', 'a+', encoding='utf-8') as save_file1:
                save_file1.write(str(i + 1) + ' : ' + ''.join(sentence.split()) + '\n')
        else:
            print('None')
            with open(save_path + text_file + '_markov.txt', 'a+', encoding='utf-8') as save_file2:
                save_file2.write(str(i + 1) + ' : ' + ''.join('None') + '\n')

        # save learned data
        with open(save_path + text_file + '_learned_data.json', 'w', encoding="utf-8") as f:
            f.write(text_model.to_json())

        # later, if you want to reuse learned data...
        """
        with open('learned_data.json') as f:
            text_model = markovify.NewlineText.from_json(f.read())
        """


if __name__ == '__main__':
    main()
