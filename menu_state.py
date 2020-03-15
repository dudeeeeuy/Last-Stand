import pygame as pg
import settings
import ui

from game_state import GameState
from score_state import ScoreState

class MenuState:
    
    def __init__(self, gdata):
        self.gdata = gdata
        self.btn_size = 200, 75
        self.vgap = 20
        self.nbtn_top = settings.WIN_SIZE[1] // 2
        self.start_btn = self.btn("Start", self.on_start)
        self.score_btn = self.btn("Scores", self.on_score)

    def btn(self, text, on_click):
        topleft = (settings.WIN_SIZE[0] - self.btn_size[0]) // 2, self.nbtn_top
        self.nbtn_top += self.btn_size[1] + self.vgap
        return ui.Button(topleft, self.btn_size, on_click, text, \
            self.gdata.fonts["Large"])

    def on_start(self, mpos):
        self.gdata.smechine.add(GameState(self.gdata), False)

    def on_score(self, mpos):
        self.gdata.smechine.add(ScoreState(self.gdata), False)

    def start_up(self):
        self.gdata.mmanager.add(self.start_btn)
        self.gdata.mmanager.add(self.score_btn)

    def update(self, dt):
        self.gdata.mmanager.update()

    def handle_event(self, event):
        self.gdata.mmanager.handle_event(event)

    def draw(self, screen):
        screen.fill(settings.BLACK)
        self.start_btn.draw(screen)
        self.score_btn.draw(screen)

    def clean_up(self):
        self.gdata.mmanager.remove(self.start_btn)
        self.gdata.mmanager.remove(self.score_btn)