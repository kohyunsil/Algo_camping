import pandas as pd
import camping_server.config as config
from datetime import datetime

class Sigungucode:
    def __init__(self):
        self.path = config.Config.PATH
        self.do_list = config.Config.DO_LIST
        self.five_code = pd.read_csv(self.path + "/sigungucode.csv")


    def read_file(self, df):
        df.drop(df[df['addr1'].isnull()].index, axis=0, inplace=True) # 빈 row 삭제
        return df


    def do_sigungu(self, df):
        # 파일 읽어오기
        df = self.read_file(df)

        # 예외처리 1: 페스티발 온라인개최 삭제
        try:
            df.drop(df[df['addr1'] == '온라인개최'].index, axis=0, inplace=True)
        except:
            pass

        # 도, 시군구명 컬럼 생성
        if not 'doNm' in df.columns.tolist():
            df['doNm'] = [a.split(" ")[0] for a in df['addr1']]
            df['doNm'] = [as_is.replace(as_is, self.do_list[as_is]) if len(as_is) < 3 else as_is for as_is in df['doNm']]
        if not 'sigunguNm' in df.columns.tolist():
            df['sigunguNm'] = [b.split(" ")[1:2] for b in df['addr1']]
            df['sigunguNm'] = [b[0] if len(b) > 0 else "" for b in df['sigunguNm']]

        df['sigunguNm2'] = [c.split(" ")[1:3] for c in df['addr1']]
        df['sigunguNm2'] = [c[0] + " " + c[1] if len(c) > 1 else "" for c in df['sigunguNm2']]
        df['sigunguNm3'] = [c.split(" ")[0:2] for c in df['addr1']]
        df['sigunguNm3'] = [c[0] + " " + c[1] if len(c) > 1 else "" for c in df['sigunguNm3']]

        # 예외처리 2: sigunguNm null값 처리
        sigunguNm = []
        for i in range(len(df)):
            a = df['sigunguNm'].iloc[i]
            b = df['sigunguNm2'].iloc[i]
            if type(a) == float:  # sigunguNm null값 예외처리
                result = b.split(" ")[0]
            else:
                result = a
            sigunguNm.append(result)
        df['sigunguNm'] = sigunguNm

        return df


    def make_sigungucode(self, df):
        df = self.do_sigungu(df)
        # 조건에 맞게 시군구코드 생성
        signguNm_ls = self.five_code['signguNm'].unique().tolist()
        sigungucode = []

        for i in range(len(df)):
            a = df['sigunguNm'].iloc[i]
            b = df['sigunguNm2'].iloc[i]
            c = df['sigunguNm3'].iloc[i]
            d = df['doNm'].iloc[i]
            if a in signguNm_ls:
                result = self.five_code['signguCode'][self.five_code['signguNm'] == a].iloc[0]
            elif b in signguNm_ls:
                result = self.five_code['signguCode'][self.five_code['signguNm'] == b].iloc[0]
            elif c in signguNm_ls:
                result = self.five_code['signguCode'][self.five_code['signguNm'] == c].iloc[0]
            elif d in ['세종시', '세종특별자치시']:
                result = self.five_code['signguCode'][self.five_code['signguNm'] == '세종특별자치시'].iloc[0]
            else:
                result = '확인필요'
            sigungucode.append(result)

        # 시군구코드 컬럼 생성
        df['sigungucode'] = sigungucode

        # DB 저장시 필요없는 컬럼 삭제
        df.drop(['doNm', 'sigunguNm', 'sigunguNm2', 'sigunguNm3'], axis=1, inplace=True)

        return df


    def final_check_save(self, filename, df):
        """
        filename에 저장하고자 하는 파일명 기입
        'filename_작업일.csv'로 저장
        """
        filedate = datetime.today().strftime("%y%m%d")

        # 오류있는 row 조회 수 drop
        if df['sigungucode'].isnull().sum() > 0 or len(df[df['sigungucode']=='확인필요']) > 0:
            drop_df = pd.DataFrame(df[df['sigungucode']=='확인필요'][['addr1']])
            print("plz check errored rows")
            print(drop_df)
            df.drop(drop_df.index, axis=0, inplace=True)

        # 최종 처리된 파일 저장
        df.to_csv(self.path + f"/{filename}_{filedate}.csv", encoding="utf-8-sig")
        print("------")
        print("File save completed!")