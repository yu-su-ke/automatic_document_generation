from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.callbacks import LambdaCallback
from keras.optimizers import RMSprop
import numpy as np
import random
import datetime
import sys
from mecab_text import mecab_text
from text_format import text_format


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probs = np.random.multinomial(1, preds, 1)
    return np.argmax(probs)


# ファイルパス
document_type = 'novel'
text_file = 'souseki_merge'

open_path = '../' + document_type + '/'
format_path = '../' + document_type + '/format/'
save_path = '../' + document_type + '/lstm/'
text_format(open_path, format_path, text_file, document_type)
text_data = open(format_path + text_file + '_format.txt', "rb").read()
text = text_data.decode("utf-8")
splitted_text = mecab_text(text)

# 現在時刻
now = datetime.datetime.now()
now_time = '{0:%Y_%m_%d %H:%M:%S}'.format(now)
# ファイル更新
update_file1 = open(save_path + text_file + '_word_detail' + '.txt', 'w+', encoding='utf-8').write(now_time + '\n')
update_file2 = open(save_path + text_file + '_word' + '.txt', 'w+', encoding='utf-8').write(now_time + '\n')
# テキスト内の文字数
print("Size of text: ", len(text))
words = sorted(list(set(splitted_text)))
# テキスト内の単語の種類
print("Total words :", len(words))

# 辞書を作成する
word_indices = dict((c, i) for i, c in enumerate(words))
indices_word = dict((i, c) for i, c in enumerate(words))
# (max_len)個の次の1単語を学習させる. (step)単語ずつずらして(max_len)単語と1単語というセットを作る
max_len = 3
step = 1
sentences = []
next_words = []
for i in range(0, len(text) - max_len, step):
    sentences.append(text[i:i + max_len])
    next_words.append(text[i + max_len])
X = np.zeros((len(sentences), max_len, len(words)), dtype=np.bool)
y = np.zeros((len(sentences), len(words)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        X[i, t, word_indices[word]] = 1
    y[i, word_indices[next_words[i]]] = 1
    # テキストのベクトル化
    X = np.zeros((len(sentences), max_len, len(words)), dtype=np.bool)
    y = np.zeros((len(sentences), len(words)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence):
        X[i, t, word_indices[word]] = 1
    y[i, word_indices[next_words[i]]] = 1

# LSTMを使ったモデルを作る
model = Sequential()  # 連続的なデータを扱う
model.add(LSTM(128, input_shape=(max_len, len(words))))
model.add(Dense(len(words)))
model.add(Activation("softmax"))
# 学習率
optimizer = RMSprop(lr=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer)
# epoch数
ep = 40


def on_epoch_end(epoch, _):
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(text) - max_len - 1)  # ランダムスタート
    # start_index = 0  # テキストの最初からスタート
    for diversity in [0.2, 0.5, 1.0, 1.2]:
        print('----- diversity:', diversity)

        generated = ''
        sentence_list = text[start_index: start_index + max_len]
        # sentence はリストなので文字列へ変換して使用
        generated += "".join(sentence_list)

        # sentence はリストなので文字列へ変換して使用
        print('----- Generating with seed: "' + "".join(sentence_list) + '"')
        sys.stdout.write(generated)

        # 次の文字を予測して足す. rangeの数字は単語数
        for i in range(100):
            x_pred = np.zeros((1, max_len, len(words)))
            for t, word in enumerate(sentence_list):
                x_pred[0, t, word_indices[word]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_word = indices_word[next_index]

            generated += next_word
            sentence_list = sentence_list[1:] + next_word

            sys.stdout.write(next_word)
            sys.stdout.flush()
        print()

        output = 'epoch : ' + str(epoch + 1) + ', ' + 'diversity : ' + str(diversity) + '\n' + str(generated) + '\n'
        with open(save_path + text_file + '_word_detail' + '.txt', 'a+', encoding='utf-8') as save_file1:
            save_file1.write(output)
        if epoch + 1 == ep:
            with open(save_path + text_file + '_word' + '.txt', 'a+', encoding='utf-8') as save_file2:
                save_file2.write(output)


print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(X, y,
          batch_size=128,
          epochs=ep,
          callbacks=[print_callback])

model.save(save_path + text_file + '_word_model' + '.h5')
