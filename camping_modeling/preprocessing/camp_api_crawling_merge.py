import re
import pandas as pd

class CampMerge:

    def camp_api_data_merge(self):
        camp_api = pd.read_csv("../datas/camp_api_info_210619.csv", encoding='utf-8-sig')
        camp_details = pd.read_csv("../datas/camp_details.csv", encoding='utf-8-sig')
        datas = camp_details['link']
        data =[ re.findall("\d+",data)[0] for data in datas]
        camp_details['url_num'] = data
        camp_details['url_num'] = camp_details['url_num'].astype('int')
        merge_inner1 = pd.merge(camp_api, camp_details, how='left', left_on='contentId',  right_on='url_num')
        merge_inner1 = merge_inner1.drop(['title', 'description', 'address', 'link', 'url_num'],1)
        merge_inner1.to_csv("../datas/camp_data_merge.csv", index=False, encoding='utf-8-sig')

    def camp_algo_merge(self):

        data1 = pd.read_csv('../datas/camp_data_merge.csv')
        data = data1.reset_index(drop=True)
        data['tags'] = data['tags'].str.replace(' ', '')
        data['tag'] = data.tags.str.replace('#', " ")
        data['tag'] = data['tag'].str.strip()
        data['tag'] = data['tag'].fillna('정보없음')

        out = []
        seen = set()
        for c in data['tag']:
            words = c.split()
            out.append(' '.join([w for w in words if w not in seen]))
            seen.update(words)
        data['unique_tag'] = out

        df = data[data['unique_tag'] != ""]
        df = df.reset_index(drop=True)

        df2 = df['unique_tag'].unique()
        df3 = " ".join(df2)
        df3 = df3.split(" ")

        def get_tag(i):
            dfs = data['tag'].str.contains(df3[i])
            data[df3[i]] = dfs.astype(int)

        for i in range(len(df3)):
            get_tag(i)

        tag_data = data.iloc[:, 90:]
        tag_data = tag_data.drop(['친절한', '재미있는', '여유있는'],1)
        camp_data1 = data[['facltNm', 'contentId', 'insrncAt', 'trsagntNo', 'mangeDivNm', 'manageNmpr', 'sitedStnc',
                           'glampInnerFclty',
                           'caravInnerFclty', 'trlerAcmpnyAt', 'caravAcmpnyAt', 'toiletCo', 'swrmCo', 'wtrplCo',
                           'brazierCl', 'sbrsCl',
                           'sbrsEtc', 'posblFcltyCl', 'extshrCo', 'frprvtWrppCo', 'frprvtSandCo', 'fireSensorCo',
                           'animalCmgCl']]

        camp_algo_merge = pd.concat([camp_data1, tag_data], 1)
        camp_algo_merge.to_csv('../datas/camp_algo_merge.csv', index=False, encoding='utf-8-sig')

        print(camp_algo_merge)

if __name__  == '__main__':
    c = CampMerge()
    # c.camp_api_data_merge()
    c.camp_algo_merge()