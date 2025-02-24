import pandas as pd
import logging


class SearchNews:
    def __init__(self,csv_path):

        self.df = pd.read_csv(csv_path)

    def extract_news(self, df):
        out = []
        df = df.head()
        for i,row in df.iterrows():
            
            
            title = row['title']
            content = row['content']
            
            out.append({'title':title,'content':content})
        return out

    def search_news(self, company_code,from_date,to_date):

        logging.info(f"Entered search news with company code {company_code}, from date: {from_date}, to_date: {to_date}")
        if company_code is not None:
            df_mini = self.df[self.df['company_code'] == company_code]
        else:
            df_mini = self.df
        
        logging.info(f"INITIAL DATAFRAME {df_mini.shape}")

        if not to_date:
                
            df_mini = df_mini[df_mini['date'] == from_date]
            shuffled_df = df_mini.sample(frac=1).reset_index(drop=True)
            df_mini = shuffled_df.head()

        else:
            df_mini = df_mini[(df_mini["date"] >= from_date) & (df_mini["date"] <= to_date)]
            df_mini = df_mini.head()
        
        logging.info(f"FINAL DATAFRAME {df_mini.shape}")

        news = self.extract_news(df_mini)

        return news
    
    def get_news(self,company_code,from_date,to_date):
        """
        get news based on keyword
        """
        data = self.search_news(company_code,from_date,to_date)
        return data  

