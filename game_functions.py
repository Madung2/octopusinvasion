import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:# or pygame.K_d :
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:# or pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_DOWN:#  or pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_UP:#  or pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):

    if event.key == pygame.K_RIGHT:#  or pygame.K_d :
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:#  or pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_DOWN:#  or pygame.K_s:
        ship.moving_down = False
    elif event.key == pygame.K_UP:#  or pygame.K_w:
        ship.moving_up = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """키보드와 마우스 이벤트에 응답"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y
):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """아젝 제한이 걸리지 않았다면 탄환 발싸"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """화면에 있는 이미지를 업데이트 하고 새 화면에 그린다 /루프를 실행할 때마다 화면을 다시 그림"""
    screen.blit(ai_settings.background, (0, 0))


    for bullet in bullets.sprites(): #배경 화면일수록 위에 둔다
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 점수 정보 그림
    sb.show_score()

    # 게임이 inactive일때 play 버튼 나타냄
    if not stats.game_active:
        play_button.draw_button()

    #가장 최근에 그린 화면을 표시
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """탄환 위치를 업데이트 하고 화면에서 사라진 탄환 제거"""
    bullets.update()

    # bullet이 화면 밖으로 나가면 지우기//for문 안에서는 그룹 항목을 제거해서 안됨 그래서 copy 메서드로 복사해서 사용
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets
):
    """외계인과 탄환이 충돌했을 때 반응을 설정"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 함대 전멸시 기존 탄환을 제거하고 새 함대를 만든다
        bullets.empty()
        ai_settings.increase_speed()

        # 레벨을 1올린다
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """화면 가장자리에 도달한 외계인이 있을 때 리액션'"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """함대 전체를 내리고 방향 바꾸기'"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """우주선이 외계인과 충동했을 때'"""
    if stats.ships_left > 0:
        # ship_left를 줄인다
        stats.ships_left -= 1

        # 스코어를 업데이트
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # 외계인과 탄환 리스트를 비운다
    aliens.empty()
    bullets.empty()

    # 외계인 함대를 새로 만들고 우주선을 중앙에 배치
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # 일시정지
    sleep(0.5) # 여기서 time>sleep 임포트 필요성


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """화면 맨 아래에 도달한 외계인이 있는지 확인하기
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 외계인과 우주선이 충돌했을때와 똑같은 반응 일어나게 함
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)


    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):

    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """함대생성####"""
    # 한 열에 함대
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 열x 열 함대
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)