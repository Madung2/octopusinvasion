import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from score_board import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # 파이게임이 제대로 동작하는데 필요한 기본 설정 초기화
    pygame.init()
    ai_settings = Settings()#세팅 클래스 불러오고
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )# 세팅창에 저장해둔 값으로 게임창 만들기(창 크기 정하는 튜플)
    pygame.display.set_caption("Octopus Invasion")
    #Play버튼을 그림
    play_button = Button(ai_settings, screen, "Play")

    # 게임을 저장할 인스턴스
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #
    bg_color = (230, 230, 230)

    #alien을 저장할 빈 그룹 만들고
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 외계인 함대 생성
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 메인루프 시작
    while True:
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )


run_game()