import math
import pygame


class Angle(float):
    def __new__(cls, x: float):
        x %= 360
        return super().__new__(cls, x)

    def __add__(self, other):
        return Angle(float(self) + other)

    def __sub__(self, other):
        return Angle(float(self) - other)

    def __mul__(self, other):
        return Angle(float(self) * other)

    def __truediv__(self, other):
        return Angle(float(self) / other)


class Game:
    __singleton = None

    def __init__(self, win=None, fps=None, background="Black"):
        self._time = 0
        self._objects = []
        self._id = 0
        self._win = win
        self._fps = fps
        self._background = background
        self._deleted = 0

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = super().__new__(cls, *args, **kwargs)
        return cls.__singleton

    def set_background(self, color):
        self._background = color

    def gen_id(self):
        self._id += 1
        return self._id

    def add_object(self, object):
        if object not in self._objects:
            self._objects.append(object)
            self._objects.sort(key=lambda x: x.layer)

    def del_obj(self, object):
        if object in self._objects:
            self._objects.pop(self._objects.index(object))
            self._deleted += 1

    @staticmethod
    def intersection(x11, y11, x12, y12, x21, y21, x22, y22) -> (None, None) or (float, float):
        ua = (x22 - x21) * (y11 - y21) - (y22 - y21) * (x11 - x21)
        ub = (x12 - x11) * (y11 - y21) - (y12 - y11) * (x11 - x21)
        ud = (y22 - y21) * (x12 - x11) - (x22 - x21) * (y12 - y11)
        if ud == 0:
            return None, None
        if 0 <= ua / ud <= 1 and 0 <= ub / ud <= 1:
            x = x11 + ua / ud * (x12 - x11)
            y = y11 + ua / ud * (y12 - y11)
            return x, y
        return None, None

    @staticmethod
    def vector(angle, length):
        return math.cos(math.radians(angle)) * length, math.sin(math.radians(angle)) * length

    def ray(self, x0, y0, angle, length=100, space=0, triggers=False):
        space_vector = self.vector(angle, space)
        x0, y0 = x0 + space_vector[0], y0 + space_vector[1]
        x1, y1 = self.vector(angle, length)
        x1, y1 = x1 + x0, y1 + y0

        intersections = []
        for obj in self._objects:
            if obj.physical or (triggers and obj.trigger):
                for coordinates in obj:
                    intersection = self.intersection(x0, y0, x1, y1, *coordinates)
                    if not intersection[0] is None:
                        intersections.append((math.sqrt((intersection[0] - x0) ** 2 + (intersection[1] - y0) ** 2), obj))
        if intersections:
            distance, obj = min(intersections, key=lambda x: x[0])
        else:
            distance = length
            obj = None
        return distance, obj

    def collision(self, glade_obj):
        if glade_obj.physical or glade_obj.trigger:
            x0, y0 = glade_obj.position
            sx0, sy0 = glade_obj.size
            for obj in self._objects:
                if (obj.physical or obj.trigger) and glade_obj.id != obj.id:
                    x1, y1 = obj.position
                    sx1, sy1 = obj.size
                    if (x1 - x0) ** 2 + (y1 - y0) ** 2 < (sx0 + sx1) ** 2 + (sy0 + sy1) ** 2:
                        for line in glade_obj:
                            for line2 in obj:
                                if self.intersection(*line, *line2)[0]:
                                    yield obj

    def start(self):
        if self.time:
            raise Exception("Game.start runs 2 times")
        for obj in self._objects:
            obj.update(0)

    def update(self, deltatime):
        self._time += deltatime

        for obj in self._objects:
            obj.update(deltatime)

    def draw(self, win, deltatime=1000):
        for obj in self._objects:
            obj.draw(win)

        font = pygame.font.Font(None, 18)
        fps = font.render(f"FPS: {1000 // deltatime}", True, "Red")
        mouse = font.render(f"MOUSE: {pygame.mouse.get_pos()}", True, "Red")
        accidents = font.render(f"DELETED: {self._deleted}", True, "Yellow")

        win.blit(fps, (10, 10))
        win.blit(mouse, (10, 30))
        win.blit(accidents, (10, 50))

    @property
    def time(self):
        return self._time

    @property
    def screen_size(self):
        return self._win.get_size()

    def run_forever(self):
        pygame.font.init()
        if self._win:
            clock = pygame.time.Clock()
            self._win.fill(self._background)
            self.draw(self._win)
            pygame.display.update()
            deltatime = clock.tick(self._fps)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_KP_PLUS:
                            self._fps += 10
                        elif event.key == pygame.K_KP_MINUS:
                            self._fps -= 10
                        elif event.key == pygame.K_KP_MULTIPLY:
                            self._fps = 0
                        elif event.key == pygame.K_KP_DIVIDE:
                            self._fps = 60

                self.update(deltatime)

                self._win.fill(self._background)
                self.draw(self._win, deltatime)
                pygame.display.update()
                if self._fps:
                    deltatime = clock.tick(self._fps)
                else:
                    deltatime = 16
