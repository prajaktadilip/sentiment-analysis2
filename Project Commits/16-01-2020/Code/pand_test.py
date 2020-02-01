import csv
import os.path

import pandas as pd
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
translator = Translator()

count = 0
pos_count = 0
neg_count = 0
neu_count = 0

filename, file_extension = os.path.splitext('test.csv')

if file_extension == '.txt':
    df = pd.read_fwf('positive.txt', delimiter=',')
    df1 = df.to_csv('sample.csv')

elif file_extension == '.csv':
    df = pd.read_csv('test.csv')
    df1 = df.to_csv('sample.csv', index=False)

df1 = pd.read_csv('sample.csv')

print("\n")
#print(df1.columns)

df1 = df1.drop(columns=['id', 'name', 'asins', 'brand', 'categories', 'keys', 'manufacturer',
       'reviews.date', 'reviews.dateAdded', 'reviews.dateSeen',
       'reviews.didPurchase', 'reviews.doRecommend', 'reviews.id',
       'reviews.numHelpful', 'reviews.rating', 'reviews.sourceURLs',
       'reviews.title', 'reviews.userCity',
       'reviews.userProvince', 'reviews.username'])

df2 = df1.to_csv('demo.csv', index=False)
df2 = pd.read_csv('demo.csv')

'''
with open('sample.csv') as input_file:
    lines = [line.split("\n") for line in input_file.readlines()]
    text_list = [" ".join(line) for line in lines]

print("\n")
for line in text_list:
'''

with open('demo.csv', 'rt', encoding='utf-8', errors='ignore') as f:
    data = csv.reader(f)
    for line in data:

        line = str(line)
        text = ""

        vs = analyzer.polarity_scores(line)
        '''
        lang = translator.detect(line)

        if lang.lang == 'en':
            text += line

        else:
            text = translator.translate(line)
        '''
        text += line
        if vs['compound'] > 0.3:
            pos_count += 1
            print(" {}] {:-<65} ===> (POSITIVE {}%) ".format(str(count+1), text, vs['pos']*100), end='\n')

        elif vs['compound'] < -0.3:
            neg_count += 1
            print(" {}] {:-<65} ===> (NEGATIVE {}%) ".format(str(count+1), text, vs['neg']*100), end='\n')

        elif 0.3 >= vs['compound'] >= -0.3:
            neu_count += 1
            print(" {}] {:-<65} ===> (NEUTRAL {}%) ".format(str(count+1), text, vs['neu']*100), end='\n')

        count += 1

print("\n")

print("Total count = {} sentences".format(count))
print("Positive Accuracy = {}% , {} positive sentences".format(pos_count / count * 100.0, pos_count))
print("Negative Accuracy = {}% , {} negative sentences".format(neg_count / count * 100.0, neg_count))
print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_count / count * 100.0, neu_count))

print("\n")
