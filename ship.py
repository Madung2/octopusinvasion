import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 인어 이미지 로드
        self.image = pygame.image.load("C:/Users/tulip/OneDrive/바탕 화면/pythonProject/인어1.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 스크린 바닥 가운데서 시작
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 인어 이미지 가운데 값 저장
        self.center = float(self.rect.centerx)

        # 기본은 움직임=False로 둔다
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def update(self):
        """움직임 계산하는 범"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom <self.screen_rect.bottom:
            self.rect.centery += self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top>0:
            self.rect.centery -= self.ai_settings.ship_speed_factor


        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)