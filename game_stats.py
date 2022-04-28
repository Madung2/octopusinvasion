class GameStats:
    """게임의 기록을 저장"""

    def __init__(self, ai_settings):
        """기록을 초기화"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 게임을 비활성 상태로 시작
        self.game_active = False

        #high_score은 리셋하지 않는다
        self.high_score = 0

    def reset_stats(self):
        """게임 도중에 바뀔수 있는 기록을 초기화"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1