from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import camp_api_crawling_merge as cacm
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import warnings
import config as config
warnings.simplefilter("ignore", UserWarning)

# 한글 폰트 설정
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Linux':
    rc('font', family='NanumBarunGothic')
else:
    print('Unknown system... sorry~')


class WeightsCalc:

    def __init__(self):
        self.path = config.Config.PATH
        self.kakao = config.Config.KAKAO
        self.naver = config.Config.NV_DATA
        self.gocamp = cacm.ReviewCamp().review_camp_merge()
        self.dm = config.Config.DIMENSION

    def weights_calc(self):

        kakao_groupby = self.kakao.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        kakao_groupby = kakao_groupby.set_index('category')
        naver_groupby = self.naver.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        naver_groupby = naver_groupby.set_index('category')

        # 리뷰 카테고리 갯수세는 코드
        count = pd.concat([naver_groupby, kakao_groupby], 1)
        count.columns = ['count_x', 'count_y']
        count['count_y'] = count['count_y'].fillna(0)
        count['count'] = count.count_x + count.count_y
        count = count.iloc[1:]

        # dimension 에서 review,tag,고캠핑 데이터 가져오기
        def review_count(polar):
            polar_dm = self.dm[self.dm.category == f'{polar}']
            polar_dm = polar_dm.dropna(subset = ['weights'])
            polar_dm_r = polar_dm[polar_dm.origindf == 'review'].originalname.tolist()
            polar_review = count.loc[polar_dm_r]
            re_cols = polar_review.index.tolist()
            for re_col in re_cols:
                col_names = self.dm[self.dm.originalname == f'{re_col}']
                col_name = np.unique(col_names.colname)
                polar_review = polar_review.rename(index = {f'{re_col}': f'{"".join(col_name)}'})
            polar_review = polar_review[['count']]
            return polar_review

        def tag_count(polar):
            polar_dm = self.dm[self.dm.category == f'{polar}']
            polar_dm_t = polar_dm[polar_dm.origindf == 'tag']
            polar_tag = polar_dm_t[['originalname', 'colname', 'weights', 'count']]
            polar_tag = polar_tag.dropna(subset = ['weights'])[['colname', 'count']]
            polar_tag = polar_tag.set_index('colname')
            return polar_tag

        def camp_columns(polar):
            polar_dm = self.dm[self.dm.category == f'{polar}']
            polar_dm_c = polar_dm[polar_dm.origindf == 'camp'].originalname.tolist()
            polar_camp = self.gocamp[polar_dm_c]
            return polar_camp

        def count_weights(data, total_r):
            mm = MinMaxScaler()
            x = np.log(data)
            mm_fit = mm.fit_transform(x)
            data['log_count'] = x
            data['log_mm'] = mm_fit
            x = total_r / data.log_count.sum()
            y = data.log_count * x
            data['weights'] = y
            return round(data, 1)

        def camp_weights(data, total_r):
            x = data.sum() / len(data)
            y = total_r / x.sum()
            w_df = pd.DataFrame(x * y, columns=['weights'])
            w_df = w_df.astype('float')
            result = w_df.weights
            return round(result, 1)

        ## comfort review & gocamp
        comfort_review = review_count('comfort')
        comfort_camp = camp_columns('comfort')
        def yon_data(colname):
            comfort_camp[[f'{colname}']] = comfort_camp[[f'{colname}']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        binary_colname = ['insrncAt', 'trlerAcmpnyAt', 'caravAcmpnyAt']
        for i in binary_colname:
            yon_data(i)
        comfort_camp[['trsagntNo']] = comfort_camp[['trsagntNo']].fillna(0)
        comfort_camp[['mangeDivNm']] = comfort_camp[['mangeDivNm']].replace('직영', 1).replace('위탁', 0).fillna(0).astype('int')
        comfort_camp[['brazierCl']] = comfort_camp[['brazierCl']].replace('개별', 1).replace('공동취사장', 1).replace('불가', 0).fillna(0).astype('int')
        for i in comfort_camp.columns:
            comfort_camp.loc[(comfort_camp[f'{i}'] != 0), f'{i}'] = 1

        ## together review & tag & camp
        together_review = review_count('together')
        together_tag = tag_count('together')
        together_camp = camp_columns('together')
        together_camp[['animalCmgCl']] = together_camp[['animalCmgCl']].replace('가능', 1).replace('가능(소형견)', 1).replace('불가능', 0).fillna(0).astype('int')
        for i in together_camp.columns:
            together_camp.loc[(together_camp[f'{i}'] != 0), f'{i}'] = 1

        ## FUN review & tag & camp
        fun_review = review_count('fun')
        fun_tag = tag_count('fun')
        fun_camp = camp_columns('fun')
        for i in fun_camp.columns:
            fun_camp.loc[(fun_camp[f'{i}'] != 0), f'{i}'] = 1

        ## HEARLING review & tag & camp
        healing_review = review_count('healing')
        healing_tag = tag_count('healing')
        healing_camp = camp_columns('healing')
        for i in healing_camp.columns:
            healing_camp.loc[(healing_camp[f'{i}'] != 0), f'{i}'] = 1


        def polar_w1(p_name_review, p_name_camp, sum, r_sum, c_sum):
            polar_w = count_weights(p_name_review, (100/sum) * r_sum)
            polar_w2 = pd.DataFrame(camp_weights(p_name_camp, (100/sum) * c_sum))
            polar_weights = pd.concat([polar_w.weights, polar_w2.weights], 0)
            return polar_weights

        def polar_w2(p_review, p_camp, p_tag, sum, r_sum, c_sum, t_sum):
            polar_w = count_weights(p_review, (100 / sum) * r_sum)
            polar_w2 = pd.DataFrame(camp_weights(p_camp, (100 / sum) * c_sum))
            polar_w3 = count_weights(p_tag, (100/sum) * t_sum)
            polar_weights = pd.concat([polar_w.weights, polar_w2.weights, polar_w3.weights], 0)
            return polar_weights

        comfort_weights = pd.DataFrame(polar_w1(comfort_review, comfort_camp, 35, 15, 20))
        comfort_weights['category'] ='comfort'
        together_weights = pd.DataFrame(polar_w2(together_review, together_camp, together_tag, 11, 5, 3, 3))
        together_weights['category'] ='together'
        fun_weights = pd.DataFrame(polar_w2(fun_review, fun_camp, fun_tag, 14, 4, 2, 8))
        fun_weights['category'] = 'fun'
        healing_weights = pd.DataFrame(polar_w2(healing_review, healing_camp, healing_tag, 10, 3, 1, 6))
        healing_weights['category'] = 'healing'
        clean_weights = pd.DataFrame({'weights':[50,50]}, index ={'clean_r','clean_s'})
        clean_weights['category'] = 'clean'

        df = pd.concat([comfort_weights, together_weights, fun_weights, healing_weights, clean_weights], 0)

        return df

class RegPreprocess:

    def reg_preprocessing(self):

        cm = cacm.CampMerge()
        api_data = cm.camp_api_data_merge()

        rp = cacm.ReviewPre()
        re_df = rp.review_preprocessing()

        df2 = re_df[['camp', 'avg_point']]
        df2 = df2.groupby('camp').mean().reset_index()

        df = re_df[['camp', 'category', 'final_point']]
        df = pd.pivot_table(df, index='camp', columns='category')
        df = df.fillna(0)
        df = df.reset_index()
        review_result = pd.concat([df["camp"], df["final_point"]], 1)
        camp_name = ['느티나무 캠핑장', '늘푸른캠핑장', '두리캠핑장', '둥지캠핑장', '백운계곡캠핑장', '별빛야영장',
                     '별헤는 밤', '산여울캠핑장', '소풍캠핑장', '솔바람 캠핑장', '솔밭야영장', '솔밭캠핑장', '포시즌',
                     '포시즌 캠핑장']
        for i in camp_name:
            review_result = review_result.query(f'camp != "{i}"')

        merge_result = pd.merge(api_data, review_result, how='outer', left_on='camp', right_on='camp')
        merge_result2 = pd.merge(merge_result, df2, how='left', left_on='camp', right_on='camp')
        result1 = merge_result2.iloc[:, 44:]
        result2 = merge_result2.iloc[:, :44]
        algo_reg_df = pd.concat([result2,result1],1)

        algo_reg_df['avg_point'] = algo_reg_df['avg_point'].fillna(0)
        data_df = algo_reg_df[algo_reg_df['avg_point'] != 0]
        data_df[['insrncAt']] = data_df[['insrncAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        data_df[['trsagntNo']] = data_df[['trsagntNo']].fillna(0)
        data_df.loc[(data_df['trsagntNo'] != 0), 'trsagntNo'] = 1
        data_df[['trsagntNo']] = data_df[['trsagntNo']].astype('int')
        data_df[['mangeDivNm']] = data_df[['mangeDivNm']].replace('직영', 1).replace('위탁', 0).fillna(0).astype('int')
        data_df[['brazierCl']] = data_df[['brazierCl']].replace('개별', 2).replace('공동취사장', 1).replace('불가', 0).fillna(
            0).astype('int')
        data_df[['animalCmgCl']] = data_df[['animalCmgCl']].replace('가능', 2).replace('가능(소형견)', 1).replace('불가능',
                                                                                                           0).fillna(
            0).astype('int')
        data_df[['trlerAcmpnyAt']] = data_df[['trlerAcmpnyAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        data_df[['caravAcmpnyAt']] = data_df[['caravAcmpnyAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        data_df['mangeDivNm'] = data_df.mangeDivNm.fillna(0)
        data_df['brazierCl'] = data_df.brazierCl.fillna(0)
        data_df['animalCmgCl'] = data_df.animalCmgCl.fillna(0)

        return data_df

class RegDef(RegPreprocess):

    def __init__(self):
        self.dm = config.Config.DIMENSION

    def remove_iqr(self, data, column):
        column_data = data[column]
        q1 = np.percentile(column_data.values, 25)
        q3 = np.percentile(column_data.values, 75)
        iqr = (q3 - q1) * 1.5
        low = q1 - iqr
        high = q3 + iqr
        outlier_idx = column_data[(column_data < low) | (column_data > high)].index
        data.drop(outlier_idx, axis=0, inplace=True)
        return data

    def outlier_record(self, df, colname):
        cond1 = df[f'{colname}'] < 1
        cond2 = df['avg_point'] > 3
        outlier_index = df[cond1 & cond2].index
        df.drop(outlier_index, axis=0, inplace=True)
        return df

    def reg_weights(self, df):
        X = df.drop('avg_point', 1)
        y = df['avg_point']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=13)
        lr_reg = LinearRegression()
        lr_reg.fit(X_train, y_train)
        datas2 = pd.DataFrame(lr_reg.coef_, index=X.columns, columns=['lr_coef'])
        datas2['lr_coef'] = abs(datas2['lr_coef'])
        datas2 = datas2.reset_index()
        return datas2

    def weights(self, df):
        datas2 = self.reg_weights(df)
        x = 100 / datas2.lr_coef.sum()
        y = datas2.lr_coef * x
        datas2['weights'] = round(y, 1)
        return datas2

    def polar_linear_reg(self):

        data_df = self.reg_preprocessing()
        dm = self.dm

        ## comfort
        comfort_dm = dm[dm.category == 'comfort'].dropna(subset = ['weights']).originalname.tolist()
        comfort = data_df[comfort_dm + ['avg_point']].reset_index(drop=True).fillna(0)
        comfort = self.remove_iqr(comfort, 'extshrCo')
        comfort = self.outlier_record(comfort, '서비스')
        comfort_reg = self.reg_weights(comfort)

        x = 100 / comfort_reg.lr_coef.sum()
        y = comfort_reg.lr_coef * x
        comfort_reg['weights'] = round(y, 2)
        comfort_reg['category'] ='comfort'


        ## together
        together_dm = dm[dm.category == 'together'].dropna(subset = ['weights']).originalname.tolist()
        together = data_df[together_dm + ['avg_point']].reset_index(drop=True).fillna(0)
        together = self.remove_iqr(together, 'posblFcltyCl')
        together = self.remove_iqr(together, 'animalCmgCl')
        together = self.remove_iqr(together, 'sbrsEtc')
        together = self.outlier_record(together, '만족도')
        together = self.outlier_record(together, '부대/공용시설')
        together_reg = self.weights(together)
        together_reg['category'] ='together'


        ## fun
        fun_dm = dm[dm.category == 'fun'].dropna(subset = ['weights']).originalname.tolist()
        fun = data_df[fun_dm + ['avg_point']].reset_index(drop = True).fillna(0)
        fun = self.remove_iqr(fun, '수영장')
        fun = self.remove_iqr(fun, '즐길거리')
        fun = self.remove_iqr(fun, '수영장 있는')
        fun = self.outlier_record(fun, '수영장')
        fun_reg = self.weights(fun)
        fun_reg['category'] ='fun'


        ## healing
        healing_dm = dm[dm.category == 'healing'].dropna(subset = ['weights']).originalname.tolist()
        healing = data_df[healing_dm + ['avg_point']].reset_index(drop = True).fillna(0)
        healing = self.remove_iqr(healing, 'brazierCl')
        healing = self.remove_iqr(healing, '바다가 보이는')
        healing = self.remove_iqr(healing, '그늘이 많은')
        healing = self.remove_iqr(healing, '물맑은')
        healing = self.outlier_record(healing, '전망')
        healing = self.outlier_record(healing, '분위기')
        healing_reg = self.weights(healing)
        healing_reg['category'] ='healing'



        ## clean
        clean_dm = dm[dm.category == 'clean'].dropna(subset = ['weights']).originalname.tolist()
        clean = data_df[clean_dm + ['avg_point']].reset_index(drop = True).fillna(0)
        clean = clean.reset_index(drop=True)
        clean = clean.fillna(0)
        clean = self.outlier_record(clean, '청결도')
        clean_reg = self.weights(clean)
        clean_reg['category'] ='clean'


        reg_df = pd.concat([comfort_reg, together_reg, fun_reg, healing_reg, clean_reg],0)
        reg_df = reg_df.drop('lr_coef', 1).set_index('index')
        reg_dms = dm.dropna(subset = ['weights']).originalname.tolist()
        for reg_dm in reg_dms:
            col_names = dm[dm.originalname == f'{reg_dm}']
            col_name = np.unique(col_names.colname)
            reg_df = reg_df.rename(index = {f'{reg_dm}': f'{"".join(col_name)}'})

        return reg_df

class FinalWeights:

    def final_weights(self):

        weights_freq = WeightsCalc().weights_calc().reset_index(drop=False)
        weights_freq["full_col"] = weights_freq[['index', 'category']].apply('_'.join, axis = 1)
        weights_reg = RegDef().polar_linear_reg().reset_index(drop=False)
        weights_reg["full_col"] = weights_reg[['index', 'category']].apply('_'.join, axis = 1)
        weights_reg = weights_reg.drop(['index', 'category'],1)
        weights_reg = weights_reg.rename(columns={'weights':'reg_weights'})

        df = pd.merge(weights_freq, weights_reg, on='full_col')
        df['final_weights'] = (df.weights+df.reg_weights)/2
        final_weigths = df[['index', 'category', 'final_weights']].set_index('index')
        return final_weigths
