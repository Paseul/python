from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import struct
import pygame

class Signal(QObject):
    js_signal = pyqtSignal(int, int)

class Joystick:

    def __init__(self, parent):
        self.parent = parent

        self.js_signal = Signal()
        self.js_signal.js_signal.connect(self.parent.jsUpdate)

        self.t = Thread(target=self.js_run)
        self.t.daemon = True
        self.t.start()

    def js_run(self):
        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.joystick.init()
        azimuth = 0
        elivation = 0

        while not done:
            for event in pygame.event.get():  # User did something.
                if event.type == pygame.QUIT:  # If user clicked close.
                    done = True  # Flag that we are done so we exit this loop.

            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            axes = joystick.get_numaxes()

            azimuth = (int)(joystick.get_axis(0) * 10000)
            elivation = (int)(joystick.get_axis(1) * 10000)

            self.js_signal.js_signal.emit(azimuth, elivation)

            # for i in range(axes):
            #     axis = joystick.get_axis(i)
            #     if axis != 0:
            #         print(i, axis)

            buttons = joystick.get_numbuttons()

            # for i in range(buttons):
            #     button = joystick.get_button(i)
            #     self.js_signal.js_signal.emit(button)

            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)
                # print(hat[0])

            clock.tick(20)