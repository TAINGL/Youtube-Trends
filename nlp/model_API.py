# import nltk
# Uncomment to download "stopwords"
# nltk.download("stopwords")

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class Prediction:
    def __init__(self, text):
        self.text = text

    def text_preprocessing(self, texte):
        """
        Preprocessing to text for wordword
        """
        tex=[]
        # stop words list
        import stop_words
        sw_1=stop_words.get_stop_words('en')
        from nltk.corpus import stopwords
        sw_nltk = set(stopwords.words('english'))
        sw=list(set(sw_1+list(sw_nltk)))
    
        texte=texte.lower()
    
        texte=re.sub(r'\W', ' ', texte)
    
        for elem in texte.split():
            if elem in sw or elem==' ':
                continue
            else:
                tex.append(elem)
        return ' '.join(tex)


    def video_comments(self, videoid):
        """
        Created comments list, dataframe with comments and id
        """
        df = pd.read_csv('../data/video_comment.csv', lineterminator='\n', index_col=[0])
        df = df[['videoid','commentid','textdisplay']]
        #df = pd.DataFrame(np.array(df.textdisplay), columns=['textdisplay'])
        for_video = df['videoid'] == videoid
        comments_list = (df[for_video]['textdisplay']).tolist() 
        #print(comments_list)
        return df, for_video, comments_list


    def sentiment_analysis(self, videoid):
        """
        Labelisation comments & count of goob and bad comments
        """
        classifier = pipeline('sentiment-analysis')
        df, for_video, comments_list = self.video_comments(videoid)
        df_comments = df[for_video]
        df_comments["label"] = 0
        for i in range(df_comments.shape[0]):
            if classifier(comments_list[i])[0]["label"] == 'POSITIVE':
                df_comments.label[i] = 'POSITIVE'
            else:
                df_comments.label[i] = 'NEGATIVE'
        print(df_comments)
        comments_list = df_comments['label'].tolist()
        count_good = sum(1 for i in comments_list if i == 'POSITIVE')
        count_bad = sum(1 for i in comments_list if i  == 'NEGATIVE')
        print(count_good, count_bad)
        
        if count_good > count_bad:
            emoji = "\U0001f600"        
            print(emoji)
        elif count_good < count_bad:
            emoji = "\U0001F61E"
            print(emoji)
        else:
            emoji = "\U0001F610"
            print(emoji)
        return df_comments, count_good, count_bad, emoji
    
    
    def sentiment_analysis_comments(self, videoid, df_comments):
        """
        Labelisation comments & count of good and bad comments
        """
        classifier = pipeline('sentiment-analysis')

        comments_list = []
        for row in str(df_comments.values):
            comments_list.append(row)

        df_comments["label"] = 0
        for i in range(df_comments.shape[0]):
            if classifier(comments_list[i])[0]["label"] == 'POSITIVE':
                df_comments.label[i] = 'POSITIVE'
            else:
                df_comments.label[i] = 'NEGATIVE'
        #print(df_comments)
        comments_list = df_comments['label'].tolist()
        count_good = sum(1 for i in comments_list if i == 'POSITIVE')
        count_bad = sum(1 for i in comments_list if i  == 'NEGATIVE')
        #print(count_good, count_bad)
        
        if count_good > count_bad:
            print("\U0001f600")
        else:
            print("\U0001F61E")
        return df_comments, count_good, count_bad



    def show_word_cloud(self, cloud, title):
        """
        Print wordcloud
        """
        plt.figure(figsize = (16, 10))
        plt.imshow(cloud, interpolation='bilinear')
        plt.title(title)
        plt.axis("off")
        plt.show()
        return plt

    def comments_splitting(self, df_comments):
        """
        Splitting between positive and negative comments
        And printing wordcloud associated with the good or bad comment
        """
        #df_comments = df_comments.apply(lambda x : text_preprocessing(x))
        good_reviews = df_comments[df_comments.label == "POSITIVE"]
        bad_reviews = df_comments[df_comments.label == "NEGATIVE"]
        #print(good_reviews)
        good_reviews_text = " ".join(good_reviews.textdisplay.to_numpy().tolist())
        bad_reviews_text = " ".join(bad_reviews.textdisplay.to_numpy().tolist())
        good_reviews_cloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(good_reviews_text)
        bad_reviews_cloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(bad_reviews_text)
        #print(good_reviews_cloud, bad_reviews_cloud)
        
        show_word_cloud(good_reviews_cloud, 'good comments')
        show_word_cloud(bad_reviews_cloud, 'bad comments')

#df_comments, count_good, count_bad = sentiment_analysis('koMbIaJ8Tmo')
#comments_splitting(df_comments)