from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

count = 0
pos_count = 0
pos_correct = 0
neg_count = 0
neg_correct = 0
neu_count = 0
neu_correct = 0

print("\n")
with open('sample.txt', 'r') as p:
    for line in p.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if vs['compound'] > 0.3:
            pos_correct += 1
            pos_count += 1
        if vs['compound'] < -0.3:
            neg_correct += 1
            neg_count += 1
        if (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
            neu_correct += 1
            neu_count += 1
        count += 1
        print(" - {:-<65} = {}".format(line, str(vs)), end='\n')

print("\n")
print("Total count = {} sentences".format(count))
print("Positive Accuracy = {}% , {} positive sentences".format(pos_correct / count * 100.0, pos_count))
print("Negative Accuracy = {}% , {} negative sentences".format(neg_correct / count * 100.0, neg_count))
print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_correct / count * 100.0, neu_count))
print("\n")
