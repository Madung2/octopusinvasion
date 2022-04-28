import pygame
from pygame.sprite import Sprite #스프라이트를 사용하면 관련 요소를 그룹으로 묶어 한번에 사용 가능


class Bullet(Sprite):
    """우주선의 현재 위치에 탄환 객체를 만듬"""

    def __init__(self, ai_settings, screen, ship):
        """탄환을 우주선 위치에 만듬"""
        super(Bullet, self).__init__()
        self.screen = screen

        # (0,0) 좌표에 탄환을 만든 다음 정확한 위치를 지정
        # 탄환은 이미지를 사용하지 않으므로 pygame.rect 클래스만 가지고 만들어야함.
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx #(탄환은 우주선 앞에서 시작하므로) centerx값이 같음
        self.rect.top = ship.rect.top #(우주선 위랑 탄환 시작 위치가 같아야 발사되는 느낌)

        # 탄환의 위치를 부동소수점 숫자로 저장//탄환속도를 더 미세하게 조정할 수 있음
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """화면 위를 향해 탄환을 움직임"""

        self.y -= self.speed_factor
        #rect의 위치를 업데이트
        self.rect.y = self.y

    def draw_bullet(self):
        """#화면에 탄막을 그린다"""
        pygame.draw.rect(self.screen, self.color, self.rect)