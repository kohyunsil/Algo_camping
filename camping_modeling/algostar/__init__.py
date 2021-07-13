import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import config as config
import cat_points as cp
import algo_points as ap


if __name__ == '__main__':
    c5 = cp.Cat5Points()
    algo = ap.AlgoPoints()

    # algo.polar_points('답게')
    # algo.algo_star('별똥별 글램핑')
    algo_df = algo.make_algo_df()
    algo_df.to_csv(config.Config.PATH + f"algo_df_{config.Config.TODAY}.csv", encoding='utf-8-sig')

    # wc = WeightsCalc()
    # wc.data_preprocessing()
    # wc.weights_calc()
