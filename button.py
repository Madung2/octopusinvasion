import pygame.font


class Button:
    def __init__(self, ai_settings, screen, msg):
        """버튼 속성 초기화"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 버튼 키기 및 기타 속성 설정
        self.width, self.height = 200, 50
        self.button_color = (255, 51, 153)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 버튼의 rect 객체 생성, 화면 중앙에 배치
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #버튼의 메시지는 한번만 준비
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """'msg를 이미지로 렌더링하고 버튼 중앙에 놓는다'''"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 빈 버튼을 그리고 그 위에 메시지를 그림
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)