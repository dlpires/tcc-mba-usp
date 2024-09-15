## IMPORTS
import pandas as pd

TRENDINS_PATH = '../datasets/trendings.json'

## READING PANDAS DATASET
def readTrendings(dataset_path):
    try:
        df = pd.read_json(dataset_path, encoding='utf-8')
        return df
    except ValueError as ve:
        print(ve)
        return None
    except FileNotFoundError as fe:
        print(fe)
        return None

## FUNCTION FOR MATCH CHANNELS WITH KEYWORDS CHANNEL INFO   
def filterMatchChannels(keyword):
    df = readTrendings(TRENDINS_PATH)
    channels = []
    ## IF DATAFRAME IS NOT RECEIVE NONE
    if not df.empty:
        ## LOOP OBSERVATIONS IN DATAFRAME
        for index, row in df.iterrows():
            ## CHECK IF WORD APPEAR IN KEYWORDS CHANNEL
            if keyword.lower() in [x.lower() for x in row['keywords']]:
                ## if not exist in channel, append de value
                if row['video_channel_account'] not in channels:
                    channels.append(row['video_channel_account'])
    
    return channels

