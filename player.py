import pygame as pg
import random as rnd
import math as m
import settings
from game_over_state import GameOverState

def distsq(pos):
    return (pos[0] - settings.WIN_CENTER[0]) ** 2 +\
        (pos[1] - settings.WIN_CENTER[1]) ** 2

def angle(base, pt):
    diff = pt[0] - base[0], pt[1] - base[1]
    arg = m.atan2(diff[1], diff[0])
    return -m.degrees(arg)

def rad_dist(ang1, ang2):
    dist = ang2 - ang1
    if dist > 180:
        dist = dist - 360
    elif dist < -180:
        dist = 360 + dist
    return dist

def norm_angle(ang):
    while ang > 180:
        ang -= 360
    while ang < -180:
        ang += 360
    return ang

def sign(x):
    return [-1, 1][x > 0]

class Player:

    def __init__(self, gdata):
        self.gdata = gdata
        self.avel = 5
        self.reload_time = 1000
        self.health = 100
        self.max_health = 100
        self.money = 0

        self.spread_shot = False

        self.angle = 0
        self.fire = False
        self.reload_timer = 0

        self.oimg = pg.Surface((100, 100), pg.SRCALPHA)
        self.img = None

        self.x, self.y = settings.WIN_CENTER
        self.radius = 25
        self.redraw(0)

    def redraw(self, percent):
        self.oimg.fill((0, 0, 0, 0))
        pg.draw.circle(self.oimg, settings.WHITE, (50, 50), 25)
        width = 40 - 15 * percent
        width = 40 if width > 40 else width
        rect = pg.Rect(50, 40, width, 20)
        pg.draw.rect(self.oimg, settings.WHITE, rect, 3)

    def update(self, dt):
        self.rotate2mouse()
        if self.reload_timer > 0:
            self.reload_timer -= dt
            self.redraw(self.reload_timer/self.reload_time)
        elif self.fire:
            self.on_fire()

    def rotate2mouse(self):
        mpos = pg.mouse.get_pos()
        ang = angle(settings.WIN_CENTER, mpos)
        dist = rad_dist(self.angle, ang)
        if abs(dist) > self.avel:
            dist = sign(dist) * self.avel
        self.rotate_ccw(dist)

    def rotate_ccw(self, ang):
        self.angle = norm_angle(self.angle + ang)

    def on_fire(self):
        self.gdata.bullets.add(Bullet(self.gdata, settings.WIN_CENTER, self.angle))
        if self.spread_shot:
            self.gdata.bullets.add(Bullet(self.gdata, settings.WIN_CENTER, \
                norm_angle(self.angle + 5)))
            self.gdata.bullets.add(Bullet(self.gdata, settings.WIN_CENTER, \
                norm_angle(self.angle - 5)))
        self.reload_timer = self.reload_time

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.gdata.smechine.add(GameOverState(self.gdata))
        if self.health >= self.max_health:
            self.health = self.max_health

    def set_reload_time(self, time):
        self.reload_time = time

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            self.fire = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.fire = True

    def draw(self, screen):
        self.img = pg.transform.rotate(self.oimg, self.angle)
        topleft = ((settings.WIN_SIZE[0] - self.img.get_width()) // 2, \
                (settings.WIN_SIZE[1] - self.img.get_height()) // 2)
        screen.blit(self.img, topleft)

class ObjectManager:

    def __init__(self):
        self.objects = []
        self.adding = []
        self.removing = []

    def add(self, object):
        self.adding.append(object)
    
    def remove(self, object):
        self.removing.append(object)

    def update(self, dt):
        
        for obj in self.removing:
            if obj in self.objects:
                self.objects.remove(obj)
        self.removing.clear()
    
        for obj in self.adding:
            self.objects.append(obj)
        self.adding.clear()

        for obj in self.objects:
            obj.update(dt)

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)

class Bullet:

    def __init__(self, gdata, pos, ang, rad=10, dmg=50, vel=0.5):
        self.gdata = gdata
        self.x, self.y = pos[0], pos[1]
        self.vx, self.vy = m.cos(m.radians(ang)) * vel, -m.sin(m.radians(ang)) * vel
        self.radius = rad
        self.damage = dmg
        self.piercing = Bullet.piercing
        
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if distsq((self.x, self.y)) > (settings.WIN_SIZE[0] // 2 + 25) ** 2:
            self.remove()

    def remove(self):
        self.gdata.bullets.remove(self)

    def draw(self, screen):
        pg.draw.circle(screen, settings.ORANGE, (int(self.x), int(self.y)), \
            self.radius)
    
    def collide(self, enemy):
        enemy.take_damage(self.damage)
        if enemy.health >= 0:
            self.gdata.player.money += enemy.worth
        if not self.piercing:
            self.remove()

Bullet.piercing = False

class ShockwaveBullet:

    def __init__(self, gdata, center, vel=0.3):
        self.gdata = gdata
        self.x, self.y = center[0], center[1]
        self.radius = 0
        self.vel = vel

    def update(self, dt):
        self.radius += self.vel * dt
        if self.radius ** 2 > distsq((0, 0)):
            self.remove()

    def remove(self):
        self.gdata.bullets.remove(self)

    def draw(self, screen):
        pg.draw.circle(screen, settings.ORANGE, (self.x, self.y), int(self.radius), 5)
    
    def collide(self, enemy):
        enemy.take_damage(enemy.health)
        if enemy.health >= 0:
            self.gdata.player.money += enemy.worth


class Enemy:
    
    def __init__(self, gdata, pos, ang, rad=30, dmg=25, vel=5):
        self.gdata = gdata
        self.x, self.y = pos[0], pos[1]
        self.vx, self.vy = -m.cos(m.radians(ang)) * vel, -m.sin(m.radians(ang)) * vel
        self.radius = rad
        self.damage = dmg
        self.health = 50
        self.worth = 25
        
    def update(self, dt):
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pg.draw.circle(screen, settings.RED, (int(self.x), int(self.y)), \
            self.radius)
    
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.gdata.enemies.remove(self)

    def collide_player(self):
        self.gdata.player.take_damage(self.damage)
        self.gdata.enemies.remove(self)

class EnemyGenerator:

    def __init__(self, gdata):
        rnd.seed()
        self.gdata = gdata
        self.timer = 2000
        self.spawn_count = 0
        self.spawn_limit = 10
        self.acc = 0
        self.total_time = 0

    def update(self, dt):
        self.acc += dt
        self.total_time += dt
        while self.acc > self.timer:
            self.spawn()
            self.acc -= self.timer
        if self.acc < 0:
            self.acc = 0
        if self.spawn_count >=  self.spawn_limit:
            self.timer = int(0.60 * self.timer)
            self.spawn_count = 0
            self.spawn_limit *= 2
    
    def spawn(self):
        ang = 360 * rnd.random() - 180
        spawn_dist = settings.WIN_SIZE[0] // 2 + 25
        x, y = m.cos(m.radians(ang)) * spawn_dist, m.sin(m.radians(ang)) * spawn_dist
        x += settings.WIN_SIZE[0] // 2
        y += settings.WIN_SIZE[1] // 2
        self.gdata.enemies.add(Enemy(self.gdata, (x, y), ang))
        self.spawn_count += 1

