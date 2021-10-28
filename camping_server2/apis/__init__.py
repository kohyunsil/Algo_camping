import apis.gocamping_api as ga
import apis.koreatour_api as ka
import apis.make_sigungucode as ms
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)
#
if __name__ == '__main__':
#     s0 = ga.GocampingApi()
    s1 = ka.KoreaTourApi()
#     sgg = ms.Sigungucode()
#
#     df = s0.gocampingAPI()
#     # df = s1.festivalAPI(20210701)
#     # df = s1.tourspotAPI(900, 12)
#     # df = s1.tourlistAPI(10)
#
#     df = sgg.make_sigungucode(df)
#     sgg.final_check_save('camp_api_info', df) #저장하고자 하는 filename 기입
#
#     """아래 함수 sigungucode 처리 불필요, 실행시 바로 csv 저장"""
#     s1.tour_estiDecoAPI(20180101, 20211028)
    s1.visitors_API(20180101, 20211028) #region_type: metco(광역시), locgo(지자체)