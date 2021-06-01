import gocamping_api as ga
import koreatour_api as ka
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

if __name__ == '__main__':
    s0 = ga.GocampingApi()
    s0.gocampingAPI()

    # s1 = ka.KoreaTourApi()
    # s1.tourspotAPI(i, contentTypeId, 1000) # def docsring 참조
    # s1.festivalAPI(20210601) #축제 시작일 기준 설정: YYYYMMDD