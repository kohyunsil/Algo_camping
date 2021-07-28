import pandas as pd
import re
from datetime import date
import config as config
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler, MaxAbsScaler
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
import MySQLdb

import main_table as mt
import algorithm_table as at
import review_table as rt
import congestion_table as ct
import sql_insert as si

if __name__ == '__main__':
    main = mt.MainInsert()
    reviw = rt.ReviewInsert()
    algo = at.AlgoInsert()
    cong = ct.CongestionInsert()
    create = si.Create()
    constraint = si.Constraint()

    IP = "34.136.89.21"
    DB = "test2"
    PW = "dss"

    cursor, engine, db = create.connect_sql(IP, DB, PW)

    festival, tour, final_data = main.camping_data()
    data, camp_df = main.concat_table(final_data, festival, tour)
    place_df = main.place_table(data)
    create.create_place(cursor)
    create.save_sql(cursor, engine, db, place_df, 'place', 'append')

    convenience_df = main.convenience_table(camp_df)
    create.create_convenience(cursor)
    create.save_sql(cursor, engine, db, convenience_df, 'convenience', 'append')
    constraint.fk_conveniecnce(cursor)

    operation_df = main.operation_table(camp_df)
    create.create_operation(cursor)
    create.save_sql(cursor, engine, db, operation_df, 'operation', 'append')
    constraint.fk_operation(cursor)

    variety_df = main.variety_table(camp_df)
    create.create_variety(cursor)
    create.save_sql(cursor, engine, db, variety_df, 'variety', 'append')
    constraint.fk_variety(cursor)

    safety_df = main.safety_table(camp_df)
    create.create_safety(cursor)
    create.save_sql(cursor, engine, db, safety_df, 'safety', 'append')
    constraint.fk_safety(cursor)

    algo_search_df = algo.make_algo_search(camp_df) 
    count_df = algo.make_count_df(camp_df, algo_search_df)
    algo_result = algo.merge_dataset()

    search_df = algo.search_table(algo_search_df)
    create.create_search(cursor)
    create.save_sql(cursor, engine, db, search_df, 'search', 'append')
    constraint.fk_search(cursor)

    algo_df = algo.algorithm_table(count_df, algo_result)
    create.create_algorithm(cursor)
    create.save_sql(cursor, engine, db, algo_df, 'algorithm', 'append')
    constraint.fk_algorithm(cursor)

    weights_df = algo.weights_table()
    create.create_weights(cursor)
    create.save_sql(cursor, engine, db, weights_df, 'weights', 'append')

    main_cat_df = algo.maincat_table()
    create.create_main_cat(cursor)
    create.save_sql(cursor, engine, db, main_cat_df, 'main_cat', 'append')
    constraint.fk_main_cat(cursor)

    sigungu_df= main.sigungu_table()
    create.create_sigungu(cursor)
    create.save_sql(cursor, engine, db, sigungu_df, 'sigungucode', 'append')

    review_data_df = reviw.review_dataset(camp_df)
    review_df = reviw.review_table(review_data_df)
    create.create_review(cursor)
    create.save_sql(cursor, engine, db, review_df, 'review', 'append')
    constraint.fk_review(cursor)

    reviewer_df = reviw.reviewer_table(review_data_df)
    create.create_reviewer(cursor)
    create.save_sql(cursor, engine, db, reviewer_df, 'reviewer', 'append')
    constraint.fk_reviewer(cursor)

    past_api = cong.past_df(camp_df)
    future_api = cong.future_df(camp_df)
    congestion_df = cong.congestion_table(past_api, future_api)
    create.create_congestion(cursor)
    create.save_sql(cursor, engine, db, congestion_df, 'congestion', 'append')









    




