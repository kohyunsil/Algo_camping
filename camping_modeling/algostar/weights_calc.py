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
        self.naver = config.Config.NAVER
        self.gocamp = config.Config.ALGO_DF


    def data_preprocessing(self):
        global size, comfort_review, comfort_camp, to_review, to_tag, to_camp, fun_review, fun_tag, fun_camp, \
            healing_review, healing_tag, healing_camp

        kakao_groupby = self.kakao.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        kakao_groupby = kakao_groupby.set_index('category')
        naver_groupby = self.naver.groupby(by=['category'], as_index=False).size().reset_index().drop('index', 1)
        naver_groupby = naver_groupby.set_index('category')

        size = pd.concat([naver_groupby, kakao_groupby], 1)
        size.columns = ['size_x', 'size_y']
        size['size_y'] = size['size_y'].fillna(0)
        size['sum'] = size.size_x + size.size_y
        size = size.iloc[1:]

        ## comfort review & gocamp
        comfort_review = size.drop(index=['맛', '메뉴', '분위기', '수영장', '아이 만족도', '음식/조식', '음식양', '전망', '즐길거리', '청결도'])
        comfort_review = pd.DataFrame(comfort_review['sum'].values, columns=['count'], index=comfort_review.index)

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
        to_review = size.loc[['아이 만족도', '만족도', '부대/공용시설', '즐길거리', '편의/부대시설']]
        to_review = pd.DataFrame(to_review['sum'].values, columns=['count'], index=to_review.index)
        to_tag_r = [1416, 1036, 945]
        to_tag_v = ['가족', '커플', '아이들놀기좋은']
        to_tag = pd.DataFrame(to_tag_r, columns=['count'], index=to_tag_v)
        to_camp = self.gocamp[['animalCmgCl', 'sbrsEtc', 'posblFcltyCl']]
        to_camp[['animalCmgCl']] = to_camp[['animalCmgCl']].replace('가능', 1).replace('가능(소형견)', 1).replace('불가능',0).fillna(0).astype('int')
        for i in to_camp.columns:
            to_camp.loc[(to_camp[f'{i}'] != 0), f'{i}'] = 1

        ## FUN review & tag & camp
        fun_review = size.loc[['수영장', '즐길거리', '아이 만족도', '만족도']]
        fun_review = pd.DataFrame(fun_review['sum'].values, columns=['count'], index=fun_review.index)
        fun_tag_r = [551, 400, 318, 459, 304, 598, 6, 728]
        fun_tag_v = ['생태교육', '둘레길', '축제', '문화유적', '자전거타기좋은', '수영장있는', '익스트림', '물놀이하기좋은']
        fun_tag = pd.DataFrame(fun_tag_r, columns=['count'], index=fun_tag_v)
        fun_camp = self.gocamp[['sbrsEtc', 'posblFcltyCl']]
        for i in fun_camp.columns:
            fun_camp.loc[(fun_camp[f'{i}'] != 0), f'{i}'] = 1

        ## HEARLING review & tag & camp
        healing_review = size.loc[['음식/조식', '전망', '분위기']]
        healing_review = pd.DataFrame(healing_review['sum'].values, columns=['count'], index=healing_review.index)

        heal_tag_r = [658, 388, 706, 1152, 502, 181]
        heal_tag_v = ['계곡옆', '물맑은', '별보기좋은', '힐링', '그늘이많은', '바다가보이는']
        healing_tag = pd.DataFrame(heal_tag_r, columns=['count'], index=heal_tag_v)

        healing_camp = self.gocamp[['brazierCl']]
        for i in healing_camp.columns:
            healing_camp.loc[(healing_camp[f'{i}'] != 0), f'{i}'] = 1



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
        comfort_weights_sum = comfort_w.weights.sum() + comfort_w2.sum()
        comfort_result_weights = pd.DataFrame(pd.concat([comfort_w.weights, comfort_w2.weights], 0))

        together_w = self.count_weights(to_review, (100/11) * 5)
        together_w2 = self.count_weights(to_tag, (100/11) * 3)
        together_w3 = self.camp_weights(to_camp, (100/11) * 3)
        together_weights_sum = together_w.weights.sum() + together_w2.weights.sum() + together_w3.sum()
        together_result_weights = pd.DataFrame(pd.concat([together_w.weights, together_w2.weights, together_w3], 0))

        fun_w = self.count_weights(fun_review, (100/14)*4)
        fun_w2 = self.count_weights(fun_tag, (100/14)*8)
        fun_w3 = self.camp_weights(fun_camp, (100/14)*2)
        fun_weights_sum = fun_w.weights.sum() + fun_w2.weights.sum() + fun_w3.sum()
        fun_result_weights = pd.DataFrame(pd.concat([fun_w.weights, fun_w2.weights, fun_w3], 0))

        healing_w = self.count_weights(healing_review, (100/10)*3)
        healing_w2 = self.count_weights(healing_tag, (100/10)*6)
        healing_w3 = self.camp_weights(healing_camp, (100/10)*1)
        healing_weights_sum = healing_w.weights.sum() + healing_w2.weights.sum() + healing_w3.sum()
        healing_result_weights = pd.DataFrame(pd.concat([healing_w.weights, healing_w2.weights, healing_w3], 0))


        ## polar 별 가중치 점수 확인
        return print(healing_result_weights)


if __name__  == '__main__':
    w = WeightsCalc()
    w.data_preprocessing()
    w.weights_calc()






