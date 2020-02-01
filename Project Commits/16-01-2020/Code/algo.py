import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator


analyzer = SentimentIntensityAnalyzer()
translator = Translator()

count = 0
pos_count = 0
pos_correct = 0
neg_count = 0
neg_correct = 0
neu_count = 0
neu_correct = 0
rat = 0
rat_count = 0

print("\n")
filename = input('$')
with open(filename,'r',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        rating = float(line[4])
        trans = translator.translate(line[5]).text

        vs = analyzer.polarity_scores(trans)
        if vs['compound'] > 0.3:
            pos_correct += 1
            pos_count += 1
            print(" - {:-<65} : {} ===> {}% ".format(trans, rating, vs), end='\n')
            print(" - {:-<65} ===> (POSITIVE {}%) ".format(trans, vs['pos']*100), end='\n')
        if vs['compound'] < -0.3:
            neg_correct += 1
            neg_count += 1
            print(" - {:-<65} : {} ===> {}% ".format(trans,rating, vs), end='\n')
            print(" - {:-<65} ===> (NEGATIVE {}%) ".format(trans, vs['neg']*100), end='\n')
        if (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
            neu_correct += 1
            neu_count += 1
            print(" - {:-<65} : {} ===> {}% ".format(trans,rating, vs), end='\n')
            print(" - {:-<65} ===> (NEUTRAL {}%) ".format(trans, vs['neu']*100), end='\n')
        print(rating)
        rat += rating
        print(rat)
        count += 1


pos = pos_correct/count*100
neg = neg_correct/count*100
neu = neg_correct/count*100        

print("\n")
print("Total count = {} sentences".format(count))
print("Positive Accuracy = {}% , {} positive sentences".format(pos_correct / count * 100.0, pos_count))
print("Negative Accuracy = {}% , {} negative sentences".format(neg_correct / count * 100.0, neg_count))
print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_correct / count * 100.0, neu_count))
print("Rating Accuracy = {}% , {} Rating sentences".format(rat / count * 10.0 + rat / count * 10.0, count))
print("\n")