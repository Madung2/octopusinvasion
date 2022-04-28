import pygame

class Settings:
    """게임 설정 정보"""

    def __init__(self):
        """게임 초기 상태 정보"""
        # 스크린 설정
        self.screen_width = 1200
        self.screen_height = 800
        self.background = pygame.image.load("C:/Users/tulip/OneDrive/바탕 화면/pythonProject/background.png")

        # 우주선 설정
        self.ship_limit = 3

        # 탄환 설정
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 외계인 설정
        self.fleet_drop_speed = 30

        # 게임 속도
        self.speedup_scale = 1.2
        # 점수 상승 폭
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """바꿀 수 있는 세팅 정보 """
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 28
        self.alien_speed_factor = 3

        # 기본 점수
        self.alien_points = 50

        # 오른쪽으로 가면 +1 왼쪽으로 가면 -1
        self.fleet_direction = 1

    def increase_speed(self):
        """스피드 상승폭"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)