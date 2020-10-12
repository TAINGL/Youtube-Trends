import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import sys

import youtube_noapi
pd.options.mode.chained_assignment = None

class Predictions_noapi:
    def __init__(self, link):
        self.link = link

    def video_comments(self,link):
        """
        Created comments list, dataframe with comments and id
        """
        comment_lists = youtube_noapi.main(link)
        df = pd.DataFrame(comment_lists, columns =['comments']) 
        return df, comment_lists

    def sentiment_analysis(self,link):
        """
        Labelisation comments & count of goob and bad comments
        """
        classifier = pipeline('sentiment-analysis')
        df, comment_lists = self.video_comments(link)
        df["label"] = 0
        for i in range(df.shape[0]):
            if classifier(comment_lists[i])[0]["label"] == 'POSITIVE':
                df.label[i] = 'POSITIVE'
            else:
                df.label[i] = 'NEGATIVE'
        print(df)
        comments_list = df['label'].tolist()
        count_good = sum(1 for i in comments_list if i == 'POSITIVE')
        count_bad = sum(1 for i in comments_list if i  == 'NEGATIVE')
        print(count_good, count_bad)
        
        if count_good > count_bad:
            print("\U0001f600")
        else:
            print("\U0001F61E")
        return df, count_good, count_bad

    def show_word_cloud(self, cloud, title):
        """
        Print wordcloud
        """
        plt.figure(figsize = (16, 10))
        plt.imshow(cloud, interpolation='bilinear')
        plt.title(title)
        plt.axis("off")
        plt.show()

    def comments_splitting(self, df):
        """
        Splitting between positive and negative comments
        And printing wordcloud associated with the good or bad comment
        """
        #df = df.apply(lambda x : text_preprocessing(x))
        good_reviews = df[df.label == "POSITIVE"]
        bad_reviews = df[df.label == "NEGATIVE"]
        #print(good_reviews)
        good_reviews_text = " ".join(good_reviews.comments.to_numpy().tolist())
        bad_reviews_text = " ".join(bad_reviews.comments.to_numpy().tolist())
        good_reviews_cloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(good_reviews_text)
        bad_reviews_cloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(bad_reviews_text)
        #print(good_reviews_cloud, bad_reviews_cloud)
        
        show_word_cloud(good_reviews_cloud, 'good comments')
        show_word_cloud(bad_reviews_cloud, 'bad comments') 

#df, count_good, count_bad = sentiment_analysis('https://www.youtube.com/watch?v=Kkd9yWak9xw')
#comments_splitting(df)