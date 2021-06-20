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

# c = CampMerge()
# c.camp_api_data_merge()