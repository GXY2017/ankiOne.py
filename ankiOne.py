import requests
from PyDictionary import PyDictionary as pydict
import nltk
# nltk.download()  # download to C:\..
from nltk.tokenize import word_tokenize, sent_tokenize

# 导入完整的英语词汇表
words = set(nltk.corpus.words.words())
# 导入英语常用词，后面去除常用词
english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
# Get the file of 10 k most common words from TXT file in a github repo
response = requests.get(english_most_common_10k)
data = response.text
set_of_common_words = {x for x in data.split('\n')}
# 导入文章
with open(r"C:\Users\XIYU.GONG\Downloads\Lehman-Brothers_-Modelling-Credit-Theory-and-Practice.txt",
          "r", encoding='utf-8') as f:
    text = f.read().replace('\n', '')
    tokens = word_tokenize(text)
    tokenSent = sent_tokenize(text)

wordTokens = [x for x in tokens if (x in words) and (len(x)>3)]
# 单词变成原型
wordRoot = [nltk.PorterStemmer().stem(word) for word in wordTokens]
wordRoot = list(dict.fromkeys(wordRoot))
wordRoot = [x for x in wordRoot if x not in list(set_of_common_words)]
# 找出含有这个单词的完整句子
sentHvWord = [[s for s in tokenSent if w in s] for w in wordRoot]

# 找出单词的含义
pydict().meaning('brother')  # En-En
# EN-CN 使用 ECDICT

# 导出ANKI 卡片，符合ANKI特殊格式的txt文件即可

# # 再找出高频词
# freqs = nltk.FreqDist(wordTokens)
# blah_list = [(k, v) for k, v in freqs.items()]
# print(blah_list)