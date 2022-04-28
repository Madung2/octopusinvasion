import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """외계인 1개 함대"""

    def __init__(self, ai_settings, screen):
        """외계인 초기 위치에 둔다"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 외계인 이미지 부러오기
        self.image = pygame.image.load("C:/Users/tulip/OneDrive/바탕 화면/pythonProject/배경X-문어리사이즈.bmp")
        self.rect = self.image.get_rect()

        # 맨 왼쪽 위를 기준으로 외계인 배치
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 외계인 위치 담기
        self.x = float(self.rect.x)

    def check_edges(self):
        """외계인이 화면 밖에 있는지 확인하고 True 반환"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """외계인을 오른쪽으로 움직입니다'"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """외계인 그리기"""
        self.screen.blit(self.image, self.rect)