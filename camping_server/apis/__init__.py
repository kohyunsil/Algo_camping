import gocamping_api as ga
import festival_api as ta
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

if __name__ == '__main__':
    # s0 = ga.gocampingApi()
    # s0.get_secretKey()
    # s0.gocampingAPI()

    s1 = ta.gocampingApi()
    # s1.tourspotAPI()
    s1.festivalAPI(20210601) #축제 시작일 기준 설정: YYYYMMDD