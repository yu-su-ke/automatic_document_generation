path = './novel/'

file_names = ['bocchan.txt', 'kokoro.txt', 'kusamakura.txt', 'wagahaiwa_nekodearu.txt']
with open(path + 'souseki_merge.txt', 'w', encoding="Shift_JIS") as outfile:
    for f_name in file_names:
        with open(path + f_name, encoding="Shift_JIS") as infile:
            outfile.write(infile.read())
