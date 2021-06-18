import pandas as pd
import numpy as np
import os
import re
import requests
import json
from PyDictionary import PyDictionary as pydict
import nltk
# nltk.download()  # download to C:\..
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from stardict import DictCsv
from spellchecker import SpellChecker
from nltk.corpus import names

spell = SpellChecker(distance=1)

# textUrl = r"C:\Users\gxy49\Downloads\Philosophers_Stone.txt"
# textUrl = r'C:\Users\XIYU.GONG\Downloads\Bill-Gates-How-to-Avoid-a-Climate-Disaster_-The-Solutions-We-Have-and-the-Breakthroughs-We-Need-Knop.txt'
textUrl = r'C:\Users\gxy49\Downloads\Philosophers_Stone.txt'

# 导入完整的英语词汇表
words = set(nltk.corpus.words.words())
peopleName = set(names.words())
# 导入英语常用词，后面去除常用词
english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_10k)
data = response.text
set_of_common_words = {x for x in data.split('\n')}
# 导入并清洗文章
with open(textUrl, "r", encoding='utf-8') as f:
    text = f.read().replace('\n', '').replace('\N{SOFT HYPHEN}', '')
    text = re.sub(re.compile(r"\s+"), " ", text)  # 剔除各种空格符号，[\r\n\t\f\v]
    text = re.sub(re.compile(r'\\x[0123456789abcdef]+'), " ", text)  # 剔除16进制字条
    text = re.sub(re.compile(r"-\s+"), "-", text)  # 剔除各种空格符号，[\r\n\t\f\v]
    text = text.replace('-', "")  # remove hyphen in word
    text = text.replace(u'\u200b', '')  # remove zero width space unicode charater
    tokens = word_tokenize(text)
    tokenSent = sent_tokenize(text, language='english')
    tokenSent = [re.sub(re.compile(r"\s+"), " ", s) for s in tokenSent]  # 对每段内再去除空格

"""清洗单词，单句"""
# 剔除简单字符
tokens = [spell.correction(x) for x in tokens]  # stripword(x)
wordTokens = [x for x in tokens if (x in words) and len(x) > 3 and (x not in peopleName)]
wordTokens = list(dict.fromkeys(wordTokens))  # 去重
# 按单词的原型剔除常用词
wordTokens = [x for x in wordTokens if WordNetLemmatizer().lemmatize(x) not in list(set_of_common_words)]
# 找出含有这个单词的完整句子, 生成例句，多个空格则只保留一个空格。
exampleSent = [[' '.join(s.split()) for s in tokenSent if w in s] for w in wordTokens]
exampleSent = [s[0] if len(s) > 0 else s for s in exampleSent]

"""翻译"""
# 单词变成原型后翻译
wordRoot = [WordNetLemmatizer().lemmatize(w) for w in wordTokens]
wordRoot = [x for x in wordRoot if x not in list(set_of_common_words)]
# 找出单词的含义
# pydicTrans = [pydict().meaning(t) for t in wordRoot]  # En-En
# EN-CN 使用 ECDICT
dictCsvTrans = DictCsv("ecdict.csv").query_batch(wordRoot)

'''制作并导出卡片， 这里出现异常符号，无法去除'''
transWord = [
    {k: v for k, v in d.items() if
     k in ['word', 'phonetic', 'translation', 'definition', 'frq', 'dnc']} if d is not None else None
    for d in dictCsvTrans]

# 导出至TXT文件
output = pd.DataFrame(
    {'word': wordRoot,
     'example': exampleSent,
     'translate': transWord
     })
# 剔除重复的单词
output.drop_duplicates(subset=['word'], keep='last', inplace=True)
# 导出至TXT
output.to_csv(os.getcwd() + r'\anki.txt', header=False, index=False, sep='\t', mode='w')

# 资源 https://github.com/dyeeee/English-Chinese-Dictionary
