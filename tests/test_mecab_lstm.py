import unittest
from LSTM.mecab import mecab_lstm
from LSTM.format import text_format


class TestMecab(unittest.TestCase):
    def test_mecab_lstm(self):
        # ファイルパス
        document_type = 'novel'
        text_file = 'wagahaiwa_nekodearu'
        open_path = '../' + document_type + '/'
        format_path = '../' + document_type + '/format/'
        text_format(open_path, format_path, text_file, document_type)

        with open(format_path + text_file + '_format.txt', "r", encoding="utf-8") as file:
            for text in file:
                print(mecab_lstm(text))


if __name__ == '__main__':
    unittest.main()
