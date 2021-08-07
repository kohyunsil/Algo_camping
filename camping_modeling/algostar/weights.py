from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import camp_api_crawling_merge as cacm
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import warnings
import algostar.config as config
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
        self.gocamp = config.Config.ALGO_DF
        self.weights_df = config.Config.WEIGHTS_DF


    def data_preprocessing(self):
        global count, comfort_review, comfort_camp, to_review, to_tag, to_camp, fun_review, fun_tag, fun_camp, \
            healing_review, healing_tag, healing_camp

        kakao_groupby = self.kakao.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        kakao_groupby = kakao_groupby.set_index('category')
        naver_groupby = self.naver.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        naver_groupby = naver_groupby.set_index('category')


        # 리뷰 카테고리 갯수세는 코드
        count = pd.concat([naver_groupby, kakao_groupby], 1)
        count.columns = ['count_x', 'count_y']
        count['count_y'] = count['count_y'].fillna(0)
        count['sum'] = count.count_x + count.count_y
        count = count.iloc[1:]


        ## comfort review & gocamp
        comfort_review = count.drop(index=['맛', '메뉴', '분위기', '수영장', '아이 만족도', '음식/조식', '음식양', '전망', '즐길거리', '청결도'])
        comfort_review = pd.DataFrame(comfort_review['sum'].values, columns=['count'], index=comfort_review.index)
        comfort_review = comfort_review.rename(index = {'가격':'price_r', '만족도':'satisfied_r', '메인시설':'main_r', '목적':'object_r', '부대/공용시설':'facility_r',
                                                        '비품':'equipment_r', '서비스':'service_r', '시설물관리':'manage_r', '예약':'reservation_r', '와이파이':'wifi_r',
                                                        '위치':'location_r', '입장':'enter_r', '주차':'parking_r', '편의/부대시설':'conv_facility_r', '혼잡도':'congestion_r' })

        comfort_camp = self.gocamp[['insrncAt', 'trsagntNo', 'mangeDivNm', 'manageNmpr', 'sitedStnc', 'glampInnerFclty', 'caravInnerFclty',
                                    'trlerAcmpnyAt', 'caravAcmpnyAt', 'toiletCo', 'swrmCo', 'wtrplCo', 'brazierCl', 'sbrsCl', 'sbrsEtc',
                                    'posblFcltyCl', 'extshrCo', 'frprvtWrppCo', 'frprvtSandCo', 'fireSensorCo']]
        comfort_camp[['insrncAt']] = comfort_camp[['insrncAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        comfort_camp[['trsagntNo']] = comfort_camp[['trsagntNo']].fillna(0)
        comfort_camp[['mangeDivNm']] = comfort_camp[['mangeDivNm']].replace('직영', 1).replace('위탁', 0).fillna(0).astype('int')
        comfort_camp[['trlerAcmpnyAt']] = comfort_camp[['trlerAcmpnyAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        comfort_camp[['caravAcmpnyAt']] = comfort_camp[['caravAcmpnyAt']].replace('Y', 1).replace('N', 0).fillna(0).astype('int')
        comfort_camp[['brazierCl']] = comfort_camp[['brazierCl']].replace('개별', 1).replace('공동취사장', 1).replace('불가', 0).fillna(0).astype('int')
        for i in comfort_camp.columns:
            comfort_camp.loc[(comfort_camp[f'{i}'] != 0), f'{i}'] = 1


        ## together review & tag & camp
        to_review = count.loc[['아이 만족도', '만족도', '부대/공용시설', '즐길거리', '편의/부대시설']]
        to_review = pd.DataFrame(to_review['sum'].values, columns=['count'], index=to_review.index)
        to_tag_r = [1416, 1036, 945]
        to_tag_v = ['가족', '커플', '아이들놀기좋은']
        to_tag = pd.DataFrame(to_tag_r, columns=['count'], index=to_tag_v)
        to_camp = self.gocamp[['animalCmgCl', 'sbrsEtc', 'posblFcltyCl']]
        to_camp[['animalCmgCl']] = to_camp[['animalCmgCl']].replace('가능', 1).replace('가능(소형견)', 1).replace('불가능',0).fillna(0).astype('int')
        for i in to_camp.columns:
            to_camp.loc[(to_camp[f'{i}'] != 0), f'{i}'] = 1
        to_review = to_review.rename(index={'아이 만족도':'childlike_r', '만족도':'satisfied_r', '부대/공용시설':'facility_r', '즐길거리':'exciting_r', '편의/부대시설':'conv_facility_r' })
        to_tag = to_tag.rename(index={'가족':'with_family_s', '커플':'with_couple_s', '아이들놀기좋은':'with_child_s'})



        ## FUN review & tag & camp
        fun_review = count.loc[['수영장', '즐길거리', '아이 만족도', '만족도']]
        fun_review = pd.DataFrame(fun_review['sum'].values, columns=['count'], index=fun_review.index)
        fun_tag_r = [551, 400, 318, 459, 304, 598, 6, 728]
        fun_tag_v = ['생태교육', '둘레길', '축제', '문화유적', '자전거타기좋은', '수영장있는', '익스트림', '물놀이하기좋은']
        fun_tag = pd.DataFrame(fun_tag_r, columns=['count'], index=fun_tag_v)
        fun_camp = self.gocamp[['sbrsEtc', 'posblFcltyCl']]
        for i in fun_camp.columns:
            fun_camp.loc[(fun_camp[f'{i}'] != 0), f'{i}'] = 1
        fun_review = fun_review.rename(index={'수영장':'pool_r', '즐길거리':'exciting_r', '아이 만족도':'childlike_r', '만족도':'satisfied_r'})
        fun_tag = fun_tag.rename(index={'생태교육':'ecological_s', '둘레길':'trail_s', '축제':'festival_s', '문화유적':'cultural_s', '자전거타기좋은':'bicycle_s',
                                        '수영장있는':'pool_s', '익스트림':'extreme_s', '물놀이하기좋은':'waterplay_s'})

        ## HEARLING review & tag & camp
        healing_review = count.loc[['음식/조식', '전망', '분위기']]
        healing_review = pd.DataFrame(healing_review['sum'].values, columns=['count'], index=healing_review.index)

        heal_tag_r = [658, 388, 706, 1152, 502, 181]
        heal_tag_v = ['계곡옆', '물맑은', '별보기좋은', '힐링', '그늘이많은', '바다가보이는']
        healing_tag = pd.DataFrame(heal_tag_r, columns=['count'], index=heal_tag_v)

        healing_camp = self.gocamp[['brazierCl']]
        for i in healing_camp.columns:
            healing_camp.loc[(healing_camp[f'{i}'] != 0), f'{i}'] = 1

        healing_review = healing_review.rename(index={'음식/조식':'food_r', '전망':'view_r', '분위기':'atmos_r'})
        healing_tag = healing_tag.rename(index={'계곡옆':'valley_s', '물맑은':'pure_water_s', '별보기좋은':'star_s', '힐링':'healing_s', '그늘이많은':'shade_s', '바다가보이는':'ocean_s'})


    def count_weights(self, data, total_r):
        mm = MinMaxScaler()
        x = np.log(data)
        mm_fit = mm.fit_transform(x)
        data['log_count'] = x
        data['log_mm'] = mm_fit
        x = total_r / data.log_count.sum()
        y = data.log_count * x
        data['weights'] = y
        return round(data, 1)

    def camp_weights(self, data, total_r):
        x = data.sum() / len(data)
        y = total_r / x.sum()
        w_df = pd.DataFrame(x * y, columns=['weights'])
        w_df = w_df.astype('float')
        result = w_df.weights
        return round(result, 1)


    def weights_calc(self):

        comfort_w = self.count_weights(comfort_review, (100/35) * 15)
        comfort_w2 = pd.DataFrame(self.camp_weights(comfort_camp, (100/35) * 20))
        # comfort_weights_sum = comfort_w.weights.sum() + comfort_w2.sum()
        comfort_weights = pd.DataFrame(pd.concat([comfort_w.weights, comfort_w2.weights], 0)).reset_index().rename(columns={'index':'colname'})
        comfort_weights['category'] = 'comfort'

        together_w = self.count_weights(to_review, (100/11) * 5)
        together_w2 = self.count_weights(to_tag, (100/11) * 3)
        together_w3 = self.camp_weights(to_camp, (100/11) * 3)
        # together_weights_sum = together_w.weights.sum() + together_w2.weights.sum() + together_w3.sum()
        together_weights = pd.DataFrame(pd.concat([together_w.weights, together_w2.weights, together_w3], 0)).reset_index().rename(columns={'index':'colname'})
        together_weights['category'] = 'together'

        fun_w = self.count_weights(fun_review, (100/14)*4)
        fun_w2 = self.count_weights(fun_tag, (100/14)*8)
        fun_w3 = self.camp_weights(fun_camp, (100/14)*2)
        fun_weights_sum = fun_w.weights.sum() + fun_w2.weights.sum() + fun_w3.sum()
        fun_weights = pd.DataFrame(pd.concat([fun_w.weights, fun_w2.weights, fun_w3], 0)).reset_index().rename(columns={'index':'colname'})
        fun_weights['category'] = 'fun'

        healing_w = self.count_weights(healing_review, (100/10)*3)
        healing_w2 = self.count_weights(healing_tag, (100/10)*6)
        healing_w3 = self.camp_weights(healing_camp, (100/10)*1)
        # healing_weights_sum = healing_w.weights.sum() + healing_w2.weights.sum() + healing_w3.sum()
        healing_weights = pd.DataFrame(pd.concat([healing_w.weights, healing_w2.weights, healing_w3], 0)).reset_index().rename(columns={'index':'colname'})
        healing_weights['category'] = 'healing'

        clean_weights = pd.DataFrame({'category':['clean','clean'], 'colname':['clean_r','clean_s'], 'weights':[50,50]})

        df = pd.concat([comfort_weights, together_weights, fun_weights, healing_weights, clean_weights], 0)
        df = df[['category', 'colname', 'weights']].reset_index(drop=True)


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
        algo_result = pd.concat([result2,result1],1)
        algo_reg_df = algo_result.rename(columns={'아이 만족도':'아이만족도'})

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

    def remove_iqr(self, data, column):
        column_data = data[column]
        q1 = np.percentile(column_data.values, 25)
        q3 = np.percentile(column_data.values, 75)

        iqr = q3 - q1
        iqr = iqr * 1.5
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

        ## comfort
        comfort = data_df[['메인시설', '서비스', '위치', '목적', '만족도', '와이파이', '혼잡도',
                           '편의/부대시설', 'insrncAt', 'trsagntNo', 'sitedStnc', 'caravAcmpnyAt', 'manageNmpr',
                           'sbrsEtc', 'extshrCo', 'sbrsCl', 'glampInnerFclty', 'caravInnerFclty',
                           'fireSensorCo', 'frprvtSandCo', 'mangeDivNm', 'brazierCl', '부대/공용시설', '가격',
                           '예약', '비품', 'frprvtWrppCo', 'toiletCo', 'posblFcltyCl', 'trlerAcmpnyAt', 'avg_point']]
        comfort = comfort.reset_index(drop=True)
        comfort = comfort.fillna(0)
        comfort = self.remove_iqr(comfort, 'extshrCo')
        comfort = self.outlier_record(comfort, '서비스')

        comfort_reg = self.reg_weights(comfort)

        comfort_reg.loc[31] = ['시설물관리', comfort_reg.loc[7].lr_coef]
        comfort_reg.loc[32] = ['주차', comfort_reg.loc[7].lr_coef]
        comfort_reg.loc[33] = ['입장', comfort_reg.loc[7].lr_coef]
        comfort_reg.loc[34] = ['swrmCo', comfort_reg.loc[27].lr_coef]
        comfort_reg.loc[35] = ['wtrplCo', comfort_reg.loc[27].lr_coef]

        x = 100 / comfort_reg.lr_coef.sum()
        y = comfort_reg.lr_coef * x
        comfort_reg['weights'] = round(y, 2)
        comfort_reg['category'] = 'comfort'

        ## together
        together = data_df[['아이만족도', '만족도', '부대/공용시설', '편의/부대시설', '즐길거리', '가족', '커플', 'posblFcltyCl', '아이들 놀기 좋은',
                            'animalCmgCl', 'sbrsEtc', 'avg_point']]
        together = together.reset_index(drop=True)
        together = together.fillna(0)
        together = self.remove_iqr(together, 'posblFcltyCl')
        together = self.remove_iqr(together, 'animalCmgCl')
        together = self.remove_iqr(together, 'sbrsEtc')
        together = self.outlier_record(together, '만족도')
        together = self.outlier_record(together, '부대/공용시설')

        together_reg = self.weights(together)
        together_reg['category'] = 'together'


        ## fun
        fun = data_df[['수영장', '즐길거리', '아이만족도', '만족도', '생태교육', '둘레길', '축제', '문화유적', '자전거 타기 좋은', '수영장 있는',
                       '익스트림', '물놀이 하기 좋은', 'sbrsEtc', 'posblFcltyCl', 'avg_point']]
        fun = fun.reset_index(drop=True)
        fun = fun.fillna(0)
        fun = self.remove_iqr(fun, '수영장')
        fun = self.remove_iqr(fun, '즐길거리')
        fun = self.remove_iqr(fun, '수영장 있는')
        fun = self.outlier_record(fun, '수영장')

        fun_reg = self.weights(fun)
        fun_reg['category'] = 'fun'


        ## healing
        healing = data_df[['음식/조식', '전망', '분위기', '계곡옆', '물맑은', '별 보기 좋은', '힐링', '그늘이 많은', '바다가 보이는', 'brazierCl', 'avg_point']]
        healing = healing.reset_index(drop=True)
        healing = healing.fillna(0)
        healing = self.remove_iqr(healing, 'brazierCl')
        healing = self.remove_iqr(healing, '바다가 보이는')
        healing = self.remove_iqr(healing, '그늘이 많은')
        healing = self.remove_iqr(healing, '물맑은')
        healing = self.outlier_record(healing, '전망')
        healing = self.outlier_record(healing, '분위기')

        healing_reg = self.weights(healing)
        healing_reg['category'] = 'healing'


        ## clean
        clean = data_df[['청결도', '깨끗한', 'avg_point']]
        clean = clean.reset_index(drop=True)
        clean = clean.fillna(0)
        clean = self.outlier_record(clean, '청결도')

        clean_reg = self.weights(clean)
        clean_reg['category'] = 'clean'

        reg_df = pd.concat([comfort_reg, together_reg, fun_reg, healing_reg, clean_reg],0)
        reg_df = reg_df.drop('lr_coef', 1)
        reg_df = reg_df.rename(columns = {'index':'colname'})
        reg_df = reg_df.set_index('colname')
        reg_df = reg_df.rename(index = {'가격':'price_r', '만족도':'satisfied_r', '메인시설':'main_r', '목적':'object_r', '부대/공용시설':'facility_r',
                                                        '비품':'equipment_r', '서비스':'service_r', '시설물관리':'manage_r', '예약':'reservation_r', '와이파이':'wifi_r',
                                                        '위치':'location_r', '입장':'enter_r', '주차':'parking_r', '편의/부대시설':'conv_facility_r', '혼잡도':'congestion_r',
                                        '아이만족도':'childlike_r', '만족도':'satisfied_r', '부대/공용시설':'facility_r', '즐길거리':'exciting_r', '편의/부대시설':'conv_facility_r',
                                        '가족':'with_family_s', '커플':'with_couple_s', '아이들 놀기 좋은':'with_child_s','수영장':'pool_r', '즐길거리':'exciting_r', '아이 만족도':'childlike_r', '만족도':'satisfied_r',
                                        '생태교육': 'ecological_s', '둘레길': 'trail_s', '축제': 'festival_s', '문화유적': 'cultural_s', '자전거 타기 좋은': 'bicycle_s', '수영장 있는': 'pool_s', '익스트림': 'extreme_s',
                                        '물놀이 하기 좋은': 'waterplay_s', '음식/조식':'food_r', '전망':'view_r', '분위기':'atmos_r','계곡옆': 'valley_s', '물맑은': 'pure_water_s', '별 보기 좋은': 'star_s',
                                        '힐링': 'healing_s', '그늘이 많은': 'shade_s', '바다가 보이는': 'ocean_s', '청결도':'clean_r', '깨끗한':'clean_s' })
        reg_df = reg_df.reset_index(drop=False)
        reg_df = reg_df[['category', 'colname', 'weights']]

        return reg_df

class FinalWeights:

    def final_weights(self):

        weights_freq = WeightsCalc()
        weights_freq.data_preprocessing()
        weights_reg = RegDef()

        df = (weights_freq.weights_calc().weights + weights_reg.polar_linear_reg().weights)/2
        print(df)