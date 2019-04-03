import re


def text_format(open_path, format_path, text_file, document_type):
    if document_type == 'novel':
        # ファイルパス
        text_data = open(open_path + text_file + '.txt', "rb")
        lines = text_data.readlines()
        with open(format_path + text_file + '_format.txt', mode='w', encoding="utf-8") as save_file:
            for line in lines:
                text = line.decode('Shift_JIS')
                text = re.split(r'\r', text)[0]
                text = re.split(r'底本', text)[0]
                text = text.replace('｜', '')
                text = text.replace('-', '')
                text = text.replace("'", '')
                text = text.replace('\u3000', '')
                text = re.sub(r'《.+?》', '', text)
                text = re.sub(r'［＃.+?］', '', text)
                text = re.sub('[\s　]', '', text)
                save_file.write(text)

    if document_type == 'tweet':
        reply_pattern = '@[\w]+'
        url_pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
        hash_tag = '#[ぁ-んァ-ン 一-龥 \w]+'

        with open(open_path + text_file + '.txt', "r", encoding="utf-8") as file:
            with open(format_path + text_file + '_format.txt', mode='w', encoding="utf-8") as save_file:
                for i in file:
                    text = re.sub(reply_pattern, '', i)
                    text = re.sub(url_pattern, '', text)
                    text = re.sub(hash_tag, '', text)
                    text = re.sub('\n', '', text)
                    text = re.sub('[\s　]', '', text)
                    text = text.replace("'", '')
                    text = text.replace('\u3000', '')
                    save_file.write(text)
