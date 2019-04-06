from glob import iglob
import markovify
import datetime
from mecab_markov import mecab_markov
from text_format import text_format


def load_from_file(files_pattern):
    # read text
    text = ""
    for path in iglob(files_pattern):
        with open(path, 'r', encoding="utf-8") as f:
            text += f.read().strip()

    return text


def markov(splitted_text, save_path, text_file, i):
    # learn model from text.
    text_model = markovify.NewlineText(splitted_text, state_size=2)
    # ... and generate from model. tries default 10
    sentence = text_model.make_sentence(tries=10)

    if str(sentence) != 'None':
        print(''.join(sentence.split()))  # need to concatenate space-splitted text
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
    # """
    # with open('learned_data.json') as f:
    #     text_model = markovify.NewlineText.from_json(f.read())
    # """


def main():
    # ファイルパス
    document_type = 'tweet'
    text_file = 'WSJJapan'

    open_path = '../' + document_type + '/'
    format_path = '../' + document_type + '/format/'
    save_path = '../' + document_type + '/markov/'
    text_format(open_path, format_path, text_file, document_type)
    text_data = load_from_file(format_path + text_file + '_format.txt')
    # 現在時刻
    now = datetime.datetime.now()
    now_time = '{0:%Y_%m_%d %H:%M:%S}'.format(now)
    # ファイル更新
    with open(save_path + text_file + '_markov' + '.txt', 'a+', encoding='utf-8') as file:
        file.write('\n' + now_time + '\n')

    splitted_text = mecab_markov(text_data)

    # rangeの中身は実行回数
    for i in range(5):
        markov(splitted_text, save_path, text_file, i)


if __name__ == '__main__':
    main()
