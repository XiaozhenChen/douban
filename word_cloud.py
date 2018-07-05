# coding = UTF8

import jieba    #分词包
import pandas as pd  
import re
import csv
import numpy    #numpy计算包

import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud#词云包

def read_comments():
    result = ''
    with open('comments.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            try:
                result += row[-1]
            except:
                pass
    return result

def main():
    comments = read_comments()
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)

    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})

    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]

    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    print(words_stat)

    wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80) #指定字体类型、字体大小和字体颜色
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
    word_frequence_list = []
    for key in word_frequence:
        temp = (key,word_frequence[key])
        word_frequence_list.append(temp)
    
    wordcloud=wordcloud.fit_words(dict(word_frequence_list))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    main()
