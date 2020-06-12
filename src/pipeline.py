import requests
import pandas as pd
import numpy as np
import time

def main():

    # define URL
    url = 'https://covidtracking.com/api/v1/states/daily.json'

    # get the data from url
    res = requests.get(url)

    # load data into pandas dataframe for manipulation
    df = pd.read_json(res.content)

    # convert date to a datetime
    df['date']=pd.to_datetime(df['date'].astype(str)).values

    # Make a new column called positive test rate
    df['positiveTestRate'] = (df['positiveIncrease'] / (df['positiveIncrease'] + df['negativeIncrease'])) * 100

    # pickle the data
    df.to_pickle('data/all_data.csv')

if __name__ == '__main__':

    while True:

        # scrape the data using main function
        main()

        # Wait 24 hours = 86400 seconds
        time.sleep(86400)