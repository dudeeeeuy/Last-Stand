
class StateMechine():

    def __init__(self, starting_state):
        self.states = [ starting_state ]
        self.adding = False
        self.removing = False
        self.new_state = None
        starting_state.start_up()

    def add(self, state, replacing = True):
        if not self.adding:
            self.adding = True
            self.removing = replacing
            self.new_state = state
        else:
            raise Exception("Something went wrong, sry cant help :(")

    def remove(self):
        self.removing = True

    def update(self, dt):
        if self.removing or self.adding:
            self.states[-1].clean_up()
            if self.removing:
                self.states.pop()
                self.removing = False
            if self.adding:
                self.states.append(self.new_state)
                self.adding = False
            self.states[-1].start_up()

        self.states[-1].update(dt)

    def draw(self, screen):
        self.states[-1].draw(screen)

    def handle_event(self, event):
        self.states[-1].handle_event(event)