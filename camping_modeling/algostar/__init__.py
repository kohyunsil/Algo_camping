import pandas as pd
from datetime import datetime
from tqdm import tqdm
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/preprocessing')
import config as config
import cat_points as cp
import algo_points as ap
import tag_points as tp
import weights as wc
import recommend as rc
today = datetime.today().strftime('%m%d')

if __name__ == '__main__':
    # c5 = cp.Cat5Points()
    # algo = ap.AlgoPoints()
    # tag = tp.TagPoints()
    # tag = tp.TagMerge()
    # final_weights = wc.FinalWeights().final_weights()
    profile = rc.ProfilePro()
    b_login = rc.BeforeLogin()

    # print(profile.animal_camp()['all_animal'])
    # print(profile.induty_camp()['auto_car'])
    # print(profile.purpose_camp()['stress_df'])

    print(profile.final_merge('all_animal', 'etc', 'healing_final_df'))

    # print(b_login.main_thema()['all_season'])
    # print(b_login.camp_thema()['downtown'])


    # algo.polar_points('답게')
    # algo.algo_star('별똥별 글램핑')
    # algo_df = algo.make_algo_df()
    # algo_df.to_csv(config.Config.PATH + f"algo_df_{today}.csv", encoding='utf-8-sig')
    # algo_log_scale = algo.algo_log_scale()

    # tag.tag_priority(8036, rank=3)
    # tag.tag_priority(7980, rank=5)
    # tag_df = tag.make_tag_prior_df(rank=7)

    # final_weights.final_weights()

    # tag.tag_merge()