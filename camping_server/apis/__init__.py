import gocamping_api as ga
import koreatour_api as ka
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

if __name__ == '__main__':
    # s0 = ga.GocampingApi()
    # s0.gocampingAPI()

    s1 = ka.KoreaTourApi()
    # s1.tour_estiDecoAPI(20210701, 20210707)
    s1.visitors_API('metco', 20210601, 20210603) #region_type: metco(광역시), locgo(지자체)