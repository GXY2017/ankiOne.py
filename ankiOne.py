import pandas as pd
import numpy as np
import os
import requests
from PyDictionary import PyDictionary as pydict
import nltk
# nltk.download()  # download to C:\..
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from stardict import DictCsv
from spellchecker import SpellChecker

spell = SpellChecker(distance=1)


def stripword(word):
    """
    去除整个字符串中非字母和数字的部分，并将字母转为小写
    :param word:
    :return:
    """
    return (''.join([n for n in word if n.isalnum()])).lower()


stripword('be- tween')

textUrl = r"C:\Users\gxy49\Downloads\Philosophers_Stone.txt"

# 导入完整的英语词汇表
words = set(nltk.corpus.words.words())
# 导入英语常用词，后面去除常用词
english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_10k)
data = response.text
set_of_common_words = {x for x in data.split('\n')}
# 导入文章
with open(textUrl, "r", encoding='utf-8') as f:
    text = f.read().replace('\n', '').replace('\N{SOFT HYPHEN}', '').replace('\u200b','')
    tokens = word_tokenize(text)
    tokenSent = sent_tokenize(text)



# 剔除简单字符
tokens = [spell.correction(stripword(x)) for x in tokens]
wordTokens = [x for x in tokens if (x in words) and len(x) > 3]
wordTokens = list(dict.fromkeys(wordTokens))  # 去重
# 按单词的原型剔除常用词
wordTokens = [x for x in wordTokens if WordNetLemmatizer().lemmatize(x) not in list(set_of_common_words)]
# 找出含有这个单词的完整句子, 生成例句，多个空格则只保留一个空格。
exampleSent = [[' '.join(s.split()) for s in tokenSent if w in s] for w in wordTokens]

# 单词变成原型后翻译
wordRoot = [WordNetLemmatizer().lemmatize(w) for w in wordTokens]
wordRoot = [x for x in wordRoot if x not in list(set_of_common_words)]
# 找出单词的含义
# pydicTrans = [pydict().meaning(t) for t in wordRoot]  # En-En

# EN-CN 使用 ECDICT
dictCsvTrans = DictCsv("ecdict.csv").query_batch(wordRoot)

transWord = [
    {v for k, v in d.items() if k in ['word', 'phonetic', 'translation', 'definition']} if d is not None else None
    for d in dictCsvTrans]

# 导出至TXT文件
output = pd.DataFrame(
    {'word': wordRoot,
     'example': exampleSent,
     'translate': transWord
     })

output.to_csv(os.getcwd() + r'\anki.txt', header=False, index=False, sep='\t', mode='w')

# 剔除原型重复的单词

# 导出ANKI 卡片，符合ANKI特殊格式的txt文件即可

#
# pydict().meaning('ridukulus')

# # 再找出高频词
# freqs = nltk.FreqDist(wordTokens)
# blah_list = [(k, v) for k, v in freqs.items()]
# print(blah_list)
