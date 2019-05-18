from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM
from keras.optimizers import RMSprop
from keras.callbacks import LambdaCallback
import numpy as np
import random
import datetime
import sys
from LSTM import format


def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probs = np.random.multinomial(1, preds, 1)
    return np.argmax(probs)


# ファイルパス
document_type = 'tweet'
text_file = 'WSJJapan'

open_path = '../' + document_type + '/'
format_path = '../' + document_type + '/format/'
save_path = '../' + document_type + '/lstm/'
format.text_format(open_path, format_path, text_file, document_type)
text_data = open(format_path + text_file + '_format.txt', "rb").read()
text = text_data.decode("utf-8")

# 現在時刻
now = datetime.datetime.now()
now_time = '{0:%Y_%m_%d %H:%M:%S}'.format(now)
# ファイル更新
update_file1 = open(save_path + text_file + '_char_detail' + '.txt', 'w+', encoding='utf-8').write(now_time + '\n')
update_file2 = open(save_path + text_file + '_char' + '.txt', 'w+', encoding='utf-8').write(now_time + '\n')
# テキスト内の文字数
print("Size of text: ", len(text))
chars = sorted(list(set(text)))
# テキスト内の文字種
print("Total chars :", len(chars))

# 辞書を作成する
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))
# (max_len)文字の次の1文字を学習させる. (step)文字ずつずらして(max_len)文字と1文字というセットを作る
max_len = 15
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - max_len, step):
    sentences.append(text[i:i + max_len])
    next_chars.append(text[i + max_len])
X = np.zeros((len(sentences), max_len, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
    # テキストのベクトル化
    X = np.zeros((len(sentences), max_len, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# LSTMを使ったモデルを作る
model = Sequential()  # 連続的なデータを扱う
model.add(LSTM(128, input_shape=(max_len, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation("softmax"))
# 学習率
optimizer = RMSprop(lr=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer)
# epoch数
ep = 15


def on_epoch_end(epoch, _):
    print()
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(text) - max_len - 1)
    start_index = 0  # テキストの最初からスタート
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
            x_pred = np.zeros((1, max_len, len(chars)))
            for t, char in enumerate(sentence_list):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            sentence_list = sentence_list[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

        output = 'epoch : ' + str(epoch + 1) + ', ' + 'diversity : ' + str(diversity) + '\n' + str(generated) + '\n'
        with open(save_path + text_file + '_char_detail' + '.txt', 'a+', encoding='utf-8') as save_file1:
            save_file1.write(output)
        if epoch + 1 == ep:
            with open(save_path + text_file + '_char' + '.txt', 'a+', encoding='utf-8') as save_file2:
                save_file2.write(output)


print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(X, y,
          batch_size=128,
          epochs=ep,
          callbacks=[print_callback])

model.save(save_path + text_file + '_char_model' + '.h5')
