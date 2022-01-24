import sys

import pygame as pg

import settings
import ui
from menu_state import MenuState
from mouse_manager import MouseManager
from state_mechine import StateMechine

# initialization --------------------------------------------------------------------
pg.init()

gdata = lambda: None
gdata.fonts = dict()
gdata.fonts["Large"] = pg.font.SysFont("roboto", 42)
gdata.fonts["small"] = pg.font.SysFont("roboto", 32)
gdata.fonts["tiny"] = pg.font.SysFont("roboto", 12)
gdata.mmanager = MouseManager()
gdata.player = None  # Player(gdata)
gdata.bullets = None  # []
gdata.enemies = None  # []
gdata.enemygen = None  # EnemyGenerator(gdata)
gdata.shop = None  # Shop(gdata)
gdata.time = 0
gdata.quit = False
gdata.score = ui.Score()
gdata.smechine = StateMechine(MenuState(gdata))

screen = pg.display.set_mode(settings.WIN_SIZE)
pg.display.set_caption(settings.WIN_TITLE)

clock = pg.time.Clock()

# main game loop --------------------------------------------------------------------
while True:
    gdata.smechine.update(clock.tick(100))
    gdata.smechine.draw(screen)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        else:
            gdata.smechine.handle_event(event)
    pg.display.update()
