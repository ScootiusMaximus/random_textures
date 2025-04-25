import asyncio
import math
import pygame
import random
import sys
from datetime import datetime

from other_files.menu import *

class Program:
    pygame.init()
    scrw = 1280
    scrh = 720
    FPS = 60
    target_w = 160
    target_h = 160
    screen = pygame.display.set_mode((scrw,scrh))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Random gradients")
    def __init__(self):
        self.interval = 10000
        self.lastchange = -self.interval
        self.image = pygame.Surface((self.target_w,self.target_h))
        self.tuning = 1
        self.method = 2

        self.colours = []
        n = 20
        for i in range(n):
            c = i * (255//n)
            self.colours.append((c,c,c))

        method1box.move_to(self.scrw*0.85,self.scrh*0.4)
        method2box.move_to(self.scrw*0.85,self.scrh*0.5)
        method3box.move_to(self.scrw*0.85,self.scrh*0.6)
        weightslider.move_to(self.scrw*0.8,self.scrh*0.7)
        method1box.screen = self.screen
        method2box.screen = self.screen
        method3box.screen = self.screen
        weightslider.screen = self.screen
        weightslider.set(0.4)

    def draw(self):
        self.screen.blit(self.image,((self.scrw-self.image.get_width())//2,(self.scrh-self.image.get_height())//2))
        angle = 360 - (((self.now() - self.lastchange) / self.interval) * 360)
        pygame.draw.arc(self.screen, (200,200,200),
                        (self.scrw * 0.85, self.scrh * 0.1, self.scrw * 0.1, self.scrw * 0.1), 0, math.radians(angle),
                        width=20)

        for button in buttons:
            button.draw()

        weightslider.draw()

        pygame.draw.rect(self.screen,(100,0,0),
            ((self.scrw*0.85)+10,self.scrh*0.4 + (self.scrh*0.1*self.method) + 10,30,30))

    def create_method_a(self):
        m = len(self.colours)-1
        states = []
        state = random.randint(0,m)
        states.append((0,0,state))
        for x in range(self.target_w-1):
            for y in range(self.target_h-1):
                state = self.make_change(state)
                states.append((x+1,y+1,state))

        self.make_surface(states)

    def create_method_b(self):
        m = len(self.colours) - 1
        states = []
        state = random.randint(0, m)
        initial_state = state
        states.append((0, 0, state))
        for y in range(self.target_h):
            state = self.make_change(state)
            states.append((0, y, state))
        state = initial_state
        for x in range(self.target_w):
            state = self.make_change(state)
            states.append((x, 0, state))

        idx = self.target_h +1
        for x in range(self.target_w):
            for y in range(self.target_h):
                c = random.randint(0,1)
                if c == 0:
                    state = self.make_change(states[-1][2])
                else:
                    state = self.make_change(states[idx - self.target_w][2])

                state = self.make_change(state)
                states.append((x, y, state))
                idx += 1

        self.make_surface(states)

    def create_method_c(self):
        m = len(self.colours) - 1
        states = []
        state = random.randint(0, m)
        initial_state = state
        for x in range(self.target_w):
            state = self.make_change(state)
            states.append((x,0,state))

        idx = self.target_w
        for y in range(self.target_h):
            for x in range(self.target_w):
                c = random.randint(0,1)
                if c == 0 and idx % self.target_w != 0:
                    state = self.make_change(states[-1][2])
                else:
                    state = self.make_change(states[idx-self.target_w][2])
                states.append((x, y, state))
                idx += 1

        self.make_surface(states)

    def make_surface(self,states):
        blank = pygame.Surface((self.target_w, self.target_h))
        blank.fill((0, 0, 0))
        for p in states:
            blank.set_at((p[0],p[1]),self.colours[p[2]])

        scale = min(self.scrw//self.target_w,self.scrh//self.target_h)
        self.image = pygame.transform.scale_by(blank,scale)

    def make_change(self, state):
        m = len(self.colours) - 1
        if abs(random.normalvariate(0, 1)) > self.tuning:
            c = random.randint(1, 2)
            if c == 1 and state < m:
                state += 1
            elif c == 2 and state > 0:
                state -= 1
        return state

    def handle_user(self):
        if method1box.pressed():
            self.method = 0
        if method2box.pressed():
            self.method = 1
        if method3box.pressed():
            self.method = 2
        weightslider.update()
        self.tuning = 4 * weightslider.get()

    def now(self):
        return pygame.time.get_ticks()

    def quit(self):
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_SPACE:
                    name = f"images/texture-{datetime.now()}.png"
                    name = name.replace(":","-")
                    pygame.image.save(self.image,name)

    async def start(self):
        while True:
            await asyncio.sleep(0)
            pygame.display.flip()
            self.clock.tick(self.FPS)
            self.screen.fill((0,0,0))

            self.handle_events()
            self.handle_user()
            self.draw()

            if self.now() - self.lastchange > self.interval:
                if self.method == 0:self.create_method_a()
                if self.method == 1:self.create_method_b()
                if self.method == 2:self.create_method_c()
                self.lastchange = self.now()

the_program = Program()
asyncio.run(the_program.start())