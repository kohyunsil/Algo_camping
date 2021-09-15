import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import sql_create
import sql_insert


if __name__ == '__main__':
    # sql 접속
    sql = sql_create.Query()
    cursor, engine, db = sql.connect_sql()

    # sql create table
    create = sql_create.CreateDb()
    fk = sql_create.Constraint()

    # create.create_camp_tb(sql.DB, cursor)
    # create.create_algopoint_tb(sql.DB, cursor)
    # fk.fk_algopoint_camp(sql.DB, cursor)
    # create.create_algotag_tb(sql.DB, cursor)
    # fk.fk_algotag_camp(sql.DB, cursor)
    # create.create_tourspot_tb(sql.DB, cursor)
    # create.create_feature_tb(sql.DB, cursor)
    # create.create_sigungu_tb(sql.DB, cursor)
    # create.create_dimension_tb(sql.DB, cursor)
    # create.create_user_tb(sql.DB, cursor)
    # create.create_sns_info_tb(sql.DB, cursor)
    # create.create_user_action_tb(sql.DB, cursor)
    # create.create_visitor_past_tb(sql.DB, cursor)
    # create.create_visitor_future_tb(sql.DB, cursor)


    # make data for table & sql insert
    content = sql_insert.MakeDataframe()

    # camp_df = content.make_camp_df()
    # print(camp_df.columns)
    # sql.save_sql(engine, camp_df, 'camp', 'append')

    # dimension_df = content.make_dimension_df()
    # sql.save_sql(engine, dimension_df, 'dimension', 'append')
    #
    # sigungu_df = content.make_sigungu_df()
    # sql.save_sql(engine, sigungu_df, 'sigungu', 'append')
    #
    # tourspot_df = content.make_tourspot_df()
    # print(tourspot_df.columns)
    # sql.save_sql(engine, tourspot_df, 'tourspot', 'append')

    algopoint_df = content.make_algopoint_df()
    sql.save_sql(engine, algopoint_df, 'algopoint', 'append')

    algotag_df = content.make_algotag_df()
    sql.save_sql(engine, algotag_df, 'algotag', 'append')

    # visitor_past_df = content.make_visitor_past_df(20180101, 20210910)
    # print(visitor_past_df.columns)
    # sql.save_sql(engine, visitor_past_df, 'visitor_past', 'append')
    #
    # visitor_future_df = content.make_visitor_future_df(startYmd=20180101, endYmd=20210910, period=90)
    # print(visitor_future_df.columns)
    # sql.save_sql(engine, visitor_past_df, 'visitor_future', 'append')