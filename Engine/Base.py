import math

import pygame

from .Engine import Game, Angle


class BaseObject(list):
    _game = Game()

    def __init__(self, size=(0, 0), position=(0, 0), rotate=0, color="White", layer=0, physical=False, trigger=False, alias=None, *args, **kwargs):
        self._size = size
        self._position = position
        self._rotate = Angle(rotate)
        self._physical = physical
        self._trigger = trigger
        self._color = color
        self._speed = 0
        self._angle_speed = 0
        self._time = 0
        self._layer = layer

        self.__triggers = []
        self.__collisions = []

        self.__id = self._game.gen_id()

        if not alias:
            self._alias = f"Object{self.id}"
        else:
            self._alias = alias

        self._start(*args, **kwargs)

        self.append((0, 0, 0, 0))
        self.append((0, 0, 0, 0))
        self.append((0, 0, 0, 0))
        self.append((0, 0, 0, 0))

    def _start(self, *args, **kwargs):
        pass

    def _update(self, deltatime):
        pass

    def _on_collision_up(self, obj):
        pass

    def _on_collision_down(self, obj):
        pass

    def _on_trigger_up(self, trigger):
        pass

    def _on_trigger_down(self, trigger):
        pass

    def update(self, deltatime):
        if self.physical:
            back = False
            rotate = self._rotate
            position = self._position

            self._rotate = self._rotate + self._angle_speed * deltatime / 1000
            self._position = (self._position[0] + self._speed * math.cos(math.radians(self._rotate)) * deltatime / 1000,
                              self._position[1] + self._speed * math.sin(math.radians(self._rotate)) * deltatime / 1000)
            if deltatime:
                self._update(deltatime)
            tmp_collisions, self.__collisions = self.__collisions, []
            tmp_triggers, self.__triggers = self.__triggers, []

            self.__glade_update()

            for collision in self._game.collision(self):
                if collision.physical:
                    if not back:
                        self._rotate = rotate
                        self._position = position
                        back = True

                    if collision not in self.__collisions:
                        self.__collisions.append(collision)
                        if collision not in tmp_collisions:
                            self._on_collision_up(collision)
                elif collision.trigger:
                    if collision not in self.__triggers:
                        self.__triggers.append(collision)
                        if collision not in tmp_triggers:
                            self._on_trigger_up(collision)

            for obj in tmp_collisions:
                if obj not in self.__collisions:
                    self._on_collision_down(obj)
            for obj in tmp_triggers:
                if obj not in self.__triggers:
                    self._on_trigger_down(obj)
        else:
            if deltatime:
                self._update(deltatime)
            else:
                self.__glade_update()

        self._time += deltatime

    def draw(self, win) -> None:
        polygon = [(self[0][0], self[0][1])]
        for x1, y1, x2, y2 in self:
            polygon.append((x2, y2))
        pygame.draw.polygon(win, self._color, polygon)

    @property
    def id(self):
        return self.__id

    @property
    def layer(self):
        return self._layer

    def set_layer(self, layer):
        if type(layer) is int:
            self._layer = layer
        else:
            raise TypeError

    @property
    def alias(self):
        return self._alias

    @property
    def rotate(self):
        if type(self._rotate) != Angle:
            self._rotate = Angle(self._rotate)
        return round(self._rotate)

    @property
    def trigger(self):
        return self._trigger

    @property
    def physical(self) -> bool:
        return self._physical

    @property
    def size(self) -> (float, float):
        return self._size

    @property
    def position(self) -> (float, float):
        return round(self._position[0]), round(self._position[1])

    def __glade_update(self):
        cos = math.cos(math.radians(self.rotate))
        cos2 = math.cos(math.radians(self.rotate + 90))
        sin = math.sin(math.radians(self.rotate))
        sin2 = math.sin(math.radians(self.rotate + 90))

        size_x = self._size[0] / 2
        size_y = self._size[1] / 2

        line = (self.position[0] + size_x * cos, self.position[1] + size_x * sin, self.position[0] - size_x * cos, self.position[1] - size_x * sin)

        self[0] = (line[0] + cos2 * size_y, line[1] + sin2 * size_y, line[2] + cos2 * size_y, line[3] + sin2 * size_y)
        self[1] = (line[2] + cos2 * size_y, line[3] + sin2 * size_y, line[2] - cos2 * size_y, line[3] - sin2 * size_y)
        self[2] = (line[2] - cos2 * size_y, line[3] - sin2 * size_y, line[0] - cos2 * size_y, line[1] - sin2 * size_y)
        self[3] = (line[0] - cos2 * size_y, line[1] - sin2 * size_y, line[0] + cos2 * size_y, line[1] + sin2 * size_y)

    def __eq__(self, other):
        if not isinstance(other, BaseObject):
            raise TypeError
        return self.id == other.id

    def __hash__(self):
        return self.id

    def destroy(self):
        self._game.del_obj(self)
