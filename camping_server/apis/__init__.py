import gocamping_api as ga
import pandas as pd
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

if __name__ == '__main__':
    s = ga.GocampingApi()
    s.get_secretKey()
    s.gocampingAPI()