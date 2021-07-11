import pandas as pd
import cat_points as cp
import algo_points as ap

if __name__ == '__main__':
    c5 = cp.Cat5Points()
    algo = ap.AlgoPoints()

    # algo.polar_points('답게')
    # algo.algo_star('별똥별 글램핑')
    algo.make_algo_df()

    # wc = WeightsCalc()
    # wc.data_preprocessing()
    # wc.weights_calc()
