#dbcamp.py
def gocamp(file):
    
    crawling = file

    crawling.rename(columns={'img_url' : 'detailimage', 'view' : 'readcount'}, inplace=True)
    crawling['left'], crawling['name'] = crawling['title'].str.split('] ', 1).str
    crawling['name'] = crawling['name'].replace(" ","").str.strip()
    crawling['address'] = crawling['address'].str.strip()

    crawling_df = crawling[['name', 'tags', 'address', 'readcount', 'detailimage']]

    data = pd.merge(api, crawling_df, how='left', left_on='placeName', right_on='name')
    final_data = data.drop_duplicates(['addr'])

    return final_data

def naver(file):

    naver = file
    naver['user_info'] = naver['user_info'].str.replace("\n","")
    naver['user_info'] = naver['user_info'].str.replace(" ","")

    naver["user_review"] = naver['user_info'].str.split("리뷰",expand=True)[1].str.split("평균별점",expand=True)[0].str.split("사진",expand=True)[0]
    naver["user_picture"] = naver['user_info'].str.split("사진",expand=True)[1].str.split("평균별점",expand=True)[0]
    naver["user_star"] = naver['user_info'].str.split("평균별점",expand=True)[1]
    naver['date'], naver['visit'] = naver["visit_info"].str.split(" ",1).str

    naver['visit_date'] = naver['date'].str[:10]
    naver['visit_count'] = naver['date'].str[10:] + naver['visit'].str[:2]
    naver['visit_reservation'] = naver['visit'].str[2:]

    naver.drop(['user_info', 'visit_info', 'date', 'visit'],1, inplace=True)
    return naver
