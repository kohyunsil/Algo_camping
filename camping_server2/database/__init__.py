import pymysql
pymysql.install_as_MySQLdb()

import main_table as mt
import review_table as rt
import sql_insert as si

if __name__ == '__main__':
    main = mt.MainInsert()
    reviw = rt.ReviewInsert()
    create = si.Create()
    constraint = si.Constraint()

    IP = " "
    DB = " "  # test2
    PW = " "

    cursor, engine, db = create.connect_sql(IP, DB, PW)

    festival, tour, final_data = main.camping_data()
    data, camp_df = main.concat_table(final_data, festival, tour)

    review_data_df = reviw.review_dataset(camp_df)
    review_df = reviw.review_table(review_data_df)
    create.create_review(cursor)
    create.save_sql(cursor, engine, db, review_df, 'review', 'append')
    constraint.fk_review(cursor)

    reviewer_df = reviw.reviewer_table(review_data_df)
    create.create_reviewer(cursor)
    create.save_sql(cursor, engine, db, reviewer_df, 'reviewer', 'append')
    constraint.fk_reviewer(cursor)








    




