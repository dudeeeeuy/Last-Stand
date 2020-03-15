import pygame as pg

class MouseManager:

    def __init__(self):
        self.mhandlers = []
        self.adding = []
        self.removing = []
        self.pmon = None
        self.md = None

    def get_mon(self, mpos):
        mon = None
        for handler in self.mhandlers:
            if handler.contains(mpos):
                mon = handler
        return mon

    def add(self, nhandler):
        self.adding.append(nhandler)

    def remove(self, mhandler):
        if self.md and self.md.id == mhandler.id:
            mhandler.on_mouse_up((0, 0))
        if self.pmon and self.pmon.id == mhandler.id:
            mhandler.on_mouse_exit((0, 0))
        self.removing.append(mhandler.id)

    def update(self):
        # update handler manager (self)
        if self.removing or self.adding:
            for id2rmv in self.removing:
                for handler in self.mhandlers:
                    if handler.id == id2rmv:
                        if self.md and self.md.id == id2rmv:
                            self.md = None
                        if self.pmon and self.pmon.id == id2rmv:
                            self.pmon = None
                        self.mhandlers.remove(handler)
            self.mhandlers += self.adding
            self.removing.clear()
            self.adding.clear()
        # notify handler of mouse exit & enter events appropriately 
        mpos = pg.mouse.get_pos()
        mon = self.get_mon(mpos)
        if self.pmon != mon:
            if self.pmon:
                self.pmon.on_mouse_exit(mpos)
            if mon:
                mon.on_mouse_enter(mpos)
        self.pmon = mon

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            self.on_mouse_up()
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.on_mouse_down()

    def on_mouse_up(self):
        mpos = pg.mouse.get_pos()
        mon = self.get_mon(mpos)
        if self.md:
            self.md.on_mouse_up(mpos)
            if self.md == mon:
                self.md.on_click(mpos)
        self.md = None

    def on_mouse_down(self):
        mpos = pg.mouse.get_pos()
        mon = self.get_mon(mpos)
        self.pmon = mon
        self.md = mon
        if mon:
            mon.on_mouse_down(mpos)