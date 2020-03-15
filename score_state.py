import pygame as pg
import settings
import ui

from game_state import GameState

class ScoreState:
    
    def __init__(self, gdata):
        self.gdata = gdata
        btn_size = 200, 75
        back_tl = settings.WIN_SIZE[0] - btn_size[0] - 20,\
            settings.WIN_SIZE[1] -btn_size[1] - 20
        self.back_btn = ui.Button(back_tl, btn_size, self.on_back, "Back",\
            self.gdata.fonts["Large"])

        self.item_height = (settings.WIN_SIZE[1] - 200) // 10

        self.time_text = self.gdata.fonts["Large"].render("Time", True, settings.WHITE)
        self.date_text = self.gdata.fonts["Large"].render("Date", True, settings.WHITE)
        self.score_text = self.gdata.fonts["Large"].render("Score", True, settings.WHITE)

        self.time_tl = settings.WIN_SIZE[0] - btn_size[0] - 40 - self.time_text.get_width(), 20
        self.date_tl = settings.WIN_CENTER[0] - self.date_text.get_width() // 2, 20
        self.score_tl = settings.WIN_SIZE[0] - self.time_tl[0] - self.score_text.get_width(), 20

        self.time_cx = self.time_tl[0] + self.time_text.get_width() // 2
        self.date_cx = self.date_tl[0] + self.date_text.get_width() // 2
        self.score_cx = self.score_tl[0] + self.score_text.get_width() // 2

        self.hs_text = self.gdata.fonts["Large"].render("High Score", True, settings.WHITE)
        self.hs_tl = settings.WIN_CENTER[0] - self.hs_text.get_width() // 2, self.item_height + 20

        self.recents_text =self.gdata.fonts["Large"].render("Recents", True, settings.WHITE)
        self.recents_tl = settings.WIN_CENTER[0] - self.recents_text.get_width() // 2, 3 * (self.item_height + 20)

    def on_back(self, mpos):
        self.gdata.smechine.remove()

    def start_up(self):
        self.gdata.mmanager.add(self.back_btn)

    def update(self, dt):
        self.gdata.mmanager.update()

    def handle_event(self, event):
        self.gdata.mmanager.handle_event(event)

    def draw_score(self, screen, score, top):
        if score:
            stxt, dtxt, ttxt = score
            stxt = str(stxt)
        else:
            stxt, dtxt, ttxt = "---", "---", "---"
        stxt = self.gdata.fonts["Large"].render(stxt, True, settings.WHITE)
        dtxt = self.gdata.fonts["Large"].render(dtxt, True, settings.WHITE)
        ttxt = self.gdata.fonts["Large"].render(ttxt, True, settings.WHITE)
        screen.blit(stxt, (self.score_cx - stxt.get_width() // 2, top))
        screen.blit(dtxt, (self.date_cx - dtxt.get_width() // 2, top))
        screen.blit(ttxt, (self.time_cx- ttxt.get_width() // 2, top))

    def draw(self, screen):
        screen.fill(settings.BLACK)
        screen.blit(self.time_text, self.time_tl)
        screen.blit(self.date_text, self.date_tl)
        screen.blit(self.score_text, self.score_tl)
        screen.blit(self.hs_text, self.hs_tl)
        self.draw_score(screen, self.gdata.score.hs, 2 * (self.item_height + 20))
        screen.blit(self.recents_text, self.recents_tl)
        self.draw_score(screen, self.gdata.score.scores[0], 4 * (self.item_height + 20))
        self.draw_score(screen, self.gdata.score.scores[1], 5 * (self.item_height + 20))
        self.draw_score(screen, self.gdata.score.scores[2], 6 * (self.item_height + 20))
        self.draw_score(screen, self.gdata.score.scores[3], 7 * (self.item_height + 20))
        self.draw_score(screen, self.gdata.score.scores[4], 8 * (self.item_height + 20))
        self.back_btn.draw(screen)
        

    def clean_up(self):
        self.gdata.mmanager.remove(self.back_btn)