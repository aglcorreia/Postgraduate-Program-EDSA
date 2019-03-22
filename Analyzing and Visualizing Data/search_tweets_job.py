# -*- coding: utf-8 -*-
"""
Created on Sat May 12 17:19:55 2018

@author: Antonio
"""
import os
os.chdir('C:\\Users\\Antonio\\OneDrive - Instituto Superior de Estatística e Gestão de Informação\\Analyzing and Visualizing Data\\Trabalho')

# import twython class
from twython import Twython  
import json
import pandas as pd
import time

from apscheduler.schedulers.background import BackgroundScheduler

def my_job():

    with open("twitter_credentials.json", "r") as file:  
        creds = json.load(file)
        
    
    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    
    # Create our query
    query = {'q': '$MSFT',  
            'result_type': 'mixed',
            'lang': 'en',
            }
    
    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}  
    for status in python_tweets.search(**query)['statuses']:  
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])
    
    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    
    df['date'] = df['date'].astype(str)
    df['text'] = df['text'].str.encode('utf-8')
    df['user'] = df['user'].astype(str)
    
    with open('tweet_search.csv', 'a') as f:
        df.to_csv(f, header=False, sep=';')
        

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_job, 'interval', minutes=20)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
