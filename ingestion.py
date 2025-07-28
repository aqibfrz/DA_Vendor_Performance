import pandas as pd 
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename='logs/ingestion_DB.log',
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine= create_engine('sqlite:///inventory.db')

def db_ingest(df , file_name , engine):
    df.to_sql(file_name, con=engine, if_exists = 'replace', index = False)

def load_raw_data():
    '''This function will load the CSV file as DF and ingest to DB'''
    start=time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df=pd.read_csv('data/'+file)
            logging.info(f'ingestion {file} in DB')
            db_ingest(df , file[:-4], engine)
    end=time.time()
    total_time=(start-end)/60
    logging.info('...ingestion complete...')
    logging.info(f'Total time taken is {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()
    
