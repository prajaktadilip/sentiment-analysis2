import csv
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

count = 0
pos_count = 0
neg_count = 0
neu_count = 0

df = pd.read_csv('test.csv')
df = df.drop(columns=['id', 'name', 'asins', 'brand', 'categories', 'keys', 'manufacturer',
       'reviews.date', 'reviews.dateAdded', 'reviews.dateSeen',
       'reviews.didPurchase', 'reviews.doRecommend', 'reviews.id',
       'reviews.numHelpful', 'reviews.rating', 'reviews.sourceURLs',
       'reviews.title', 'reviews.userCity',
       'reviews.userProvince', 'reviews.username'])
df1 = df.to_csv('demo.csv', index=False)
df1 = pd.read_csv('demo.csv')

with open('demo.csv', 'rt', encoding='utf-8', errors='ignore') as f:
    
    data = csv.reader(f)
    analyzer = SentimentIntensityAnalyzer()

    for line in data:

        line = str(line)
        vs = analyzer.polarity_scores(line)
        
        if vs['compound'] > 0.3:
            pos_count += 1
            print(" {}] {:-<65} ===> (POSITIVE {}%) ".format(str(count+1), line, vs['pos']*100), end='\n')

        elif vs['compound'] < -0.3:
            neg_count += 1
            print(" {}] {:-<65} ===> (NEGATIVE {}%) ".format(str(count+1), line, vs['neg']*100), end='\n')

        elif 0.3 >= vs['compound'] >= -0.3:
            neu_count += 1
            print(" {}] {:-<65} ===> (NEUTRAL {}%) ".format(str(count+1), line, vs['neu']*100), end='\n')

        count += 1

print("\n")

print("Total count = {} sentences".format(count))
print("Positive Accuracy = {}% , {} positive sentences".format(pos_count / count * 100.0, pos_count))
print("Negative Accuracy = {}% , {} negative sentences".format(neg_count / count * 100.0, neg_count))
print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_count / count * 100.0, neu_count))

print("\n")
