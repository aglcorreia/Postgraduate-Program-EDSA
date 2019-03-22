# -*- coding: utf-8 -*-
"""
Created on Sun May 13 16:45:12 2018

@author: Antonio
"""

import os
os.chdir('C:\\Users\\Antonio\\OneDrive - Instituto Superior de Estatística e Gestão de Informação\\Analyzing and Visualizing Data\\Trabalho')

import pandas as pd

from textblob import TextBlob
import re

# import file
test = pd.read_excel('tweet_search_xl.xlsx').reset_index()
test.drop(columns=['index'], inplace=True)
test.drop_duplicates(inplace=True)

# write function to clean tweet text
def clean_tweet(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

# write function to apply sentiment calculation
def sentiment_calc(text):
    try:
        return TextBlob(text).sentiment
    except:
        return None
    
test['clean_text'] = test['text'].apply(clean_tweet)
test['sentiment'] = test['clean_text'].apply(sentiment_calc)

# this returns a tuple of the form sentiment(polarity,subjectivity). Need to untuple
test['polarity']=test['sentiment'].apply(pd.Series)[0]
test['subjectiv']=test['sentiment'].apply(pd.Series)[1]
test.drop(columns=['sentiment'], inplace=True)
