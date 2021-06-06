import gocamping_api as ga
import koreatour_api as ka
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

if __name__ == '__main__':
    # s0 = ga.GocampingApi()
    # s0.gocampingAPI()

    s1 = ka.KoreaTourApi()
    s1.tour_estiDecoAPI(20210701, 20210707)