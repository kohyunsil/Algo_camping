import pandas as pd
from datetime import date
import config as config
from main_table import MainInsert

class CongestionInsert:
    def __init__(self):
        self.past = config.Config.PAST
        self.future = config.Config.FUTURE

    # 과거 혼잡도
    def past_df (self, camp_df):
        visitor_api = self.past
        visitor_api = visitor_api.rename(columns={'signguCode' : 'sigungu_code'})
        out = visitor_api['touDivCd'] == '2'
        foreign = visitor_api['touDivCd'] == '3'
        visitor_api = visitor_api[out | foreign]
        visitor_api_df = visitor_api.groupby(['sigungu_code', 'baseYmd']).sum()
        visitor_api_df = visitor_api_df.reset_index()
    
        visitor_api_merge = pd.merge(visitor_api_df, camp_df, how='left', on='sigungu_code')
        past_api = visitor_api_merge[['sigungu_code', 'baseYmd', 'touNum', 'content_id']]
        past_api = past_api.dropna()
        past_api = past_api.rename(columns={'baseYmd' : 'base_ymd',
                    'touNum' : 'congestion'})
        return past_api
    
    # 미래 혼잡도
    def future_df(self, camp_df):
        esti_api = self.future
        esti_api_df = pd.merge(esti_api, camp_df, how='left', left_on='contentId', right_on='content_id')

        future = esti_api_df[['baseYmd', 'estiNum', 'content_id', 'sigungu_code']]
        future_df = future.groupby(['sigungu_code', 'baseYmd']).sum()
        future_df = future_df.reset_index()
        future_api = pd.merge(future_df, future, how='left', on = ['sigungu_code', 'baseYmd'])
        future_api = future_api.drop(['content_id_x', 'estiNum_y'],1)
        future_api = future_api.rename(columns={'baseYmd' : 'base_ymd',
                        'estiNum_x' : 'congestion',
                        'content_id_y' : 'content_id'})
        return future_api

    # 과거 미래 concat
    def congestion_table(self, past_api, future_api):
        con_df = pd.concat([past_api,future_api])
        congestion_df = con_df.reset_index()
        congestion_df = congestion_df.drop(['index'],1)
        today = date.today()
        congestion_df['created_date'] = today.isoformat()
        congestion_df = congestion_df.rename(columns={'index' : 'id', 'baseYmd' : 'base_ymd', 
                                    'touNum' : 'congestion'})
        congestion_df = congestion_df.dropna()
        return congestion_df

    