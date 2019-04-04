import MeCab

mecab = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
print(mecab.parse("乗り換え案内でお馴染みのジョルダン。主要施設の中に「野球場」がある。12球団の本拠地に加え神戸があるほか、大谷清宮フィーバーのせいか鎌ヶ谷が入っているまではわかる。"))

# 乗り換え 案内 で お 馴染み の ジョルダン 。 主要 施設 の 中 に 「 野球場 」 が ある 。 12球団 の 本拠地 に 加え 神戸 が ある ほか 、 大谷 清宮 フィーバー の せい か 鎌ヶ谷 が 入っ て いる まで は わかる 。