import pandas as pd
import numpy as np
import random
from datetime import datetime


class CopyWriting:
    def __init__(self):
        pass
    
    def read_answer(self):
        """DB.user 테이블에서 유저가 등록한 응답 불러오기"""
        pass

    def copy_a100(self, answer):
        if answer == 5:
            return "어서와요, 캠핑은 처음이죠? 캠린이도 쉽게 즐기는 글램핑!"
        else:
            pass

    def copy_a200(self, answer):
        with_whom_dict = {1: '가족', 2: '연인', 3: '친구들', 4: '혼자'}
        if answer == 4:
            copy = '혼자라서 오롯이 그 행복을 느낄 수 있는 캠핑'
        else:
            copy = f"{with_whom_dict[answer]}과 함께 즐길 수 있는 캠핑장은 어떠세요?"
        return copy

    def copy_a210(self, answer):
        if answer == 1:
            copy1 = "댕댕이와 함께 즐길 수 있는 이런 캠핑장은 어떠세요?"
            copy2 = "반려동물과 함께하면 캠핑의 행복이 두 배!"
            return random.choice([copy1, copy2])
        else:
            pass

    def copy_a300(self, answer):
        camp_dict = {1: '오토캠핑', 2: '카라반', 3: '글램핑'}
        copy = f"인기 있는 {camp_dict[answer]} 스팟도 둘러보세요!"
        return copy

    def copy_a410(self, answer, now=True):
        season_dict = {1: '봄', 2: '여름', 3: '가을', 4: '겨울'}
        if now:
            month = datetime.today().month

            if month in range(3, 5):
                season = '봄'
            elif month in range(6, 8):
                season = '여름'
            elif month in range(9, 11):
                season = '가을'
            else:
                season = '겨울'

        else:
            season = season_dict[answer]

        copy = f'{season}에 놀러가기 좋은 캠핑장을 둘러보세요!'
        return season, copy

    def copy_a420(self, answer):
        if answer == 1:
            copy1 = '시원한 바닷바람과 함께 즐기는 캠핑 어떠세요?'
            copy2 = '탁 트인 바닷가 근처에서 즐기는 캠핑 어떠세요?'

        elif answer == 2:
            copy1 = '맑은 공기로 마음까지 정화되는 힐링 캠핑 떠나봐요!'
            copy2 = '숲 속 캠핑으로 몸과 마음 모두 정화되는 힐링'

        elif answer == 3:
            copy1 = '내 마음 속 호수를 찾아, 나 만의 캠핑장을 찾아서'
            copy2 = '맑은 강물이 흐르는 곳에서 여유로운 캠핑을 즐겨봐요'

        elif answer == 4:
            copy1 = '바쁜 일상에서 벗어나 훌쩍 떠나보는 도심 속 캠핑장'
            copy2 = '도심 속 캠핑장에서 망중한을 즐겨보세요'

        else:
            copy1 = '좋아하실 만한 인기 캠핑장을 소개드려요'
            copy2 = '요즘 뜨는 인기 캠핑장을 소개드려요'
        return random.choice([copy1, copy2])

    def copy_a500(self, answer):
        if answer == 1:
            """가입자 성별에 따라 아빠, 엄마 구분 예정"""
            copy1 = '“이번 주말에 어디가?” 라는 물음에도 자신있는 엄마아빠의 비결은?'
            copy2 = '아이들이 즐길 거리가 가득한 캠핑장으로 떠나보세요'
            copy = random.choice([copy1, copy2])
        elif answer == 2:
            copy = '여유롭게 감성 캠핑을 즐겨봐요'
        elif answer == 3:
            copy = '생태교육까지 즐길 수 있는 재미있는 캠핑!'
        elif answer == 4:
            # copy = f'{festival}이 열리는 {region}캠핑장으로 떠나봐요'
            copy = '주변 투어 코스까지 갖춰진 캠핑장으로 완벽한 여행을 계획해보세요'
        else:
            copy = '좋아하실 만한 인기 캠핑장을 소개드려요'
        return copy

    def copy_a600(self, answer):
        region_dict = {1: '수도권', 2: '동해/강원권', 3: '남해/영남권',
                       4: '서해/충청권', 5: '광주/호남권', 6: '제주도'}
        return f"{region_dict[answer]} 에서 인기있는 캠핑장을 둘러보세요"

    def copy_mix_scene(self, s_no):
         scene_dict = {
                  101: "아빠어디가? 아이들과 함께 즐길 수 있는 캠핑장!",  # 롤링배너
                  102: "드넓은 동해바다로! 바다근처 캠핑장은 어떠세요?",  # 롤링배너
                  103: "계곡에서 즐기고, 산속에서 체험할 수 있는 캠핑장!",
                  104: "매력적인 남해로! 바다근처 캠핑장은 어떠세요?",
                  105: "요즘 관광 트렌드는 남해죠! 캠핑도 즐기고 주변 투어도 해요!",  # 롤링배너
                  106: "특별한 날엔 특별한 데이트, 연인과 휴양하는 감성캠핑 어떠세요?",
                  107: "가을 캠핑에 감성 한스푼",
                  108: "가을 단풍 여행가요! 가을단풍명소 근처 캠핑장",  # 롤링배너
                  109: "가족과 함께 즐길 수 있는 캠핑장",
                  110: "웨이크 액티비티도 체험하고 캠핑도 즐겨요!",
                  111: "반려동물과 산책가요! 둘레길이 있는 캠핑장",  # 롤링배너
                  112: "협재, 애월, 월정리 제주바다에서 캠핑해요",  # 롤링배너
                  113: "제주투어하고 저녁에는 낭만캠핑 즐겨요",
                  114: "액티비티와 캠핑을 한번에 ! 실패없는 제주 여행",
                  115: "가족과 함께 오토캠핑과 차박을 즐겨보세요!",  # 롤링배너
                  116: "친구와 함께 오토캠핑과 차박을 즐겨보세요!",
                  117: "가족과 함께하는 글램핑&카라반",
                  118: "친구와의 캠핑 어디로 갈 지 고민이라면 글램핑&카라반으로~",
                  119: "연인과의 캠핑을 어떻게 계획할지 고민이라면 글램핑&카라반으로~"}  # 롤링배너
         copy = scene_dict[s_no]
         return copy
