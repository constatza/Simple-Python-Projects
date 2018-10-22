# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:30:26 2017
@author: Κωνσταντίνος

Title:Graphics

"""
import tkinter as tk
import time
import random as rand
import numpy as np


WIDTH = 800
HEIGHT = 800
CENTER = np.array( [WIDTH/2, HEIGHT/2])
N = 100

class Ball:

    diam = 30

    def __init__(self, canvas, center, radius, vel0=[0, 0], acc0=[0, 0], color=None):
        self.rad = radius
        self.shape = canvas.create_oval(center[0] - radius, center[1] - radius,
                                        center[0] + radius, center[1] + radius,
                                        fill=color)
        self.canvas = canvas
        self.vel = np.array(vel0)
        self.acc = np.array(acc0)
        self.pos = np.array(center)
        self.mass = np.pi*self.rad**3

    def apply_force(self, force):
        self.acc = force/self.mass

    @property
    def pos(self):
        coords =  self.canvas.coords(self.shape)
        x = 0.5 * (coords[0] + coords[2])
        y = 0.5 * (coords[1] + coords[3])
        return np.array([x, y])

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, value):
        self._vel = value

    @pos.setter
    def pos(self, newpos):
        r = self.rad
        self.canvas.coords(newpos[0]-r, newpos[1]-r, newpos[0]+r, newpos[1]+r)

    def move(self):
        hit_edge = False
       # hit_edge = self.check_edges()
        if hit_edge==False:
            self.vel = self.vel + self.acc*DT
        self.canvas.move(self.shape, self.vel[0]*DT, self.vel[1]*DT)

    def check_edges(self):
        x = self.pos[0]
        y = self.pos[1]
        r = self.rad
        hit_edge = False
        if x - r < 0 or x + r > WIDTH:
            self.vel = self.vel  * np.array([-1, 1])
            hit_edge = True
        if y - r < 0 or y + r > HEIGHT:
            self.vel = self.vel  * np.array([1, -1])
            hit_edge = True
        return hit_edge

    def attracted(self, other):
        F = Central(self, other)
        self.apply_force(F)
        self.move()
        other.apply_force(-F)
        other.move()


    def check_collision(self, other):
        dist = np.linalg.norm(self.pos-other.pos)
        if dist!=0 and dist <+ self.rad + other.rad:
            M = self.mass + other.mass
            dP = 2* self.mass * other.mass/M * (self.vel-other.vel)
            self.vel = self.vel - dP/self.mass
            other.vel = other.vel +  dP/other.mass
            return True
        else:
            return False



def Central(body, center_body):
    r = body.pos-center_body.pos
    dist = np.linalg.norm(r)
    if dist!=0:
        F = -0.09*r*body.mass*center_body.mass/dist**2
    else:
        F = [0, 0]
    F = np.array(F)
    return F


def CircFlow(r, zero):
    dist = np.linalg.norm(r-zero)
    F = np.empty(2)
    q = r - zero
    if dist!=0:
        F[0], F[1] = -(q[1]/dist), (q[0]/dist)
    else:
        F = np.array([0, 0])
    return 2*F

root = tk.Tk()
root.title('Graphics')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

colors = ['orange','red', 'blue', 'green', 'yellow', 'black', 'purple', 'pink']
Sun = Ball(canvas, CENTER, 10, color='yellow')

balls = []
N = 2
for i in range(N):
    pos0 = np.random.randint(300, 500, size=2)
    r = pos0 - CENTER
    vel0 = np.array([-r[1], r[0]])
    balls.append(Ball(canvas,
                      pos0,
                      rand.randint(10, 15),
                      vel0 = vel0/50 ,
                      acc0=np.random.randint(-1, 1, size=2),
                      color=np.random.choice(colors, replace=False)
                      )
                )
global DT
DT = 0.01
while True:
    for i in range(len(balls)):
        ball = balls[i]
        for other_ball in balls+[Sun]:
            #ball.check_collision(other_ball)
            ball.attracted(other_ball)
        ball.move()
        Sun.pos = CENTER
        force2 = CircFlow(ball.pos, CENTER)
        force1 = Central(ball, Sun)
        SF = force1 #+ force2
        #ball.apply_force(SF)
    root.update()
    time.sleep(0.014)

tk.mainloop()

