from feedparser import parse
from collections import defaultdict
import time
import re
import nltk
from nltk.corpus import stopwords
import datetime

def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})

class Article(object):
    """docstring for Article"""
    def __init__(self, entry ):
        self.link = entry['link'].encode('ascii','ignore')
        self.title = entry['title'].encode('ascii','ignore').lower()
        self.published = entry['published'].encode('ascii','ignore')
        self.published_parsed = entry['published_parsed']
        self.summary = entry['summary'].encode('ascii','ignore')
        self.timesince = (time.mktime(time.gmtime()) - time.mktime(self.published_parsed)) / 60
    
    def __repr__(self):
        return self.title

    def to_dict(self):
        return {
            "link": self.link,
            "title": self.title,
            "published": self.published,
            "summary": self.summary,
            "timesince": self.timesince
            }
    
# https://www.ccn.com:443
class CoinFeels(object):
    """docstring for CoinFeels"""
    def __init__(self, symbol):
        self.symbol = symbol
        
    def populate_articles(self):
        # https://www.ccn.com:443
        d = parse('https://news.google.com/news/rss/search/section/q/'+self.symbol+'/'+self.symbol+'?hl=en&gl=US&ned=us')
        articles = list()
        for entry in d['entries']:
            data = Article( entry )
            articles += [data]
        print "Downloaded %s" % len(articles)
        self.articles = sorted(articles, key=lambda x: x.timesince, reverse=False)
        
    def train(self, positive_articles, negative_articles):
        start_time = datetime.datetime.now()
        print "Start training %s" % start_time
        stops = stopwords.words("english")
        pos = []
        pos_counter = 0
        with open(positive_articles) as f:
            for i in f: 
                pos_counter += 1
                pos.append([format_sentence(i), 'pos'])

        neg = []
        neg_counter = 0
        with open(negative_articles) as f:
            for i in f: 
                neg_counter += 1
                neg.append([format_sentence(i), 'neg'])

        training = pos[:int((.8)*len(pos))] + neg[:int((.8)*len(neg))]
        test = pos[int((.8)*len(pos)):] + neg[int((.8)*len(neg)):]

        if neg_counter + pos_counter > 10:
            from nltk.classify import NaiveBayesClassifier
            self.classifier = NaiveBayesClassifier.train(training)
            end_time = datetime.datetime.now()
            print "POS: %s NEG: %s" % (pos_counter, neg_counter)
            print "Done training %s \nTook: %s" % (end_time, end_time - start_time)
            self.classifier.show_most_informative_features()
        else:
            print "Not enough data to train model"