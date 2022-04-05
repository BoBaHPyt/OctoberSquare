import random
import math

from Engine.Base import BaseObject


class Road(BaseObject):
    pass

class RoadLine(BaseObject):
    pass

class CarSpawn(BaseObject):
    colors = ["olivedrab1", "orange", "orchid", "paleturquoise1", "palevioletred", "purple", "red3"]

    def _start(self, positions, limit=20):
        self._limit = limit
        self._positions = positions
        self._count = 0
        self._pos_generator = self._position_generator()
        self._time = 0

    def _create_car(self):
        if self._limit:
            x, y, angle = self._pos_generator.__next__()
            car = Car(size=(40, 20), position=(x, y), rotate=angle, color=random.choice(self.colors))
            self._game.add_object(car)
            self._limit -= 1

    def on_delete(self):
        self._limit += 1

    def update(self, deltatime):
        self._time += deltatime
        if self._time > 1000:
            self._create_car()
            self._time = 0
        if not self._limit:
            self.destroy()

    def _position_generator(self):
        i = 0
        while True:
            yield self._positions[i]
            i += 1
            i %= len(self._positions)


class Car(BaseObject):
    def _start(self):
        self._layer = 1
        self.__start_position = self.position
        self.__start_rotate = self.rotate

        self._physical = True
        self._speed = 80
        self._route = 0
        self._stop_trigger = False

    def restart(self):
        self._position = self.__start_position
        self._rotate = self.__start_rotate
        self._angle_speed = 0
        self._route = 0

    def _on_collision_up(self, obj):
        self.restart()

    def _on_collision_down(self, obj):
        self.restart()

    def _on_trigger_down(self, trigger):
        if type(trigger) is TurnTrigger:
            self._route = trigger.route
        elif type(trigger) is TrafficLights:
            self._stop_trigger = False

    def _on_trigger_up(self, trigger):
        if type(trigger) is TrafficLights and trigger.state:
            self._stop_trigger = True
        elif type(trigger) is TurnTrigger:
            self._route = 0

    def forward_ray(self, triggers=False):
        length = self.size[0] / 2 + 3
        return self._game.ray(*self.position, self.rotate, space=length, triggers=triggers)

        # dx, dy = self._game.vector(self.rotate, self.size[0] / 5)
        # x3 = math.cos(math.radians(self.rotate + 40)) * self.size[0] / 2 + dx
        # y3 = math.sin(math.radians(self.rotate + 40)) * self.size[1] / 2 + dy
        # x4 = math.cos(math.radians(self.rotate - 40)) * self.size[0] / 2 + dx
        # y4 = math.sin(math.radians(self.rotate - 40)) * self.size[1] / 2 + dy
        # return min(self._game.ray(*self.position, self.rotate, space=length, triggers=triggers),
        #            self._game.ray(self.position[0] + x3, self.position[1] + y3, self.rotate, triggers=triggers),
        #            self._game.ray(self.position[0] + x4, self.position[1] + y4, self.rotate, triggers=triggers),
        #            key=lambda x: x[0])

    def left_ray(self, triggers=False):
        x, y = self._game.vector(self.rotate, self.size[0] / 2 + 1)
        return self._game.ray(self.position[0] + x, self.position[1] + y, self.rotate - 90, triggers=triggers, length=50)

    def right_ray(self, triggers=False):
        x, y = self._game.vector(self.rotate, self.size[0] / 2 + 1)
        return self._game.ray(self.position[0] + x, self.position[1] + y, self.rotate + 90, triggers=triggers, length=50)

    def _go_ahead(self):
        distance, obj = self.forward_ray()
        if distance < 5:
            self._speed = -10
        elif distance < 10 and self._speed >= 0:
            self._speed = 0
        elif distance < 20 and self._speed < 0:
            self._speed = 0
        elif distance < 20:
            self._speed = 30
        else:
            self._speed = 80

        left, _ = self.left_ray(True)
        right, _ = self.right_ray(True)
        if right - left > 8:
            self._angle_speed = 0.2 * self._speed
        elif left - right > 8:
            self._angle_speed = -0.2 * self._speed
        else:
            self._angle_speed = 0

    def _turn(self):
        distance, obj = self.forward_ray()
        if distance < 15:
            self._speed = -10
            self._angle_speed = self._route * self._speed / 80 / 8
        elif distance < 20:
            self._angle_speed = 0
            self._speed = 0
        else:
            self._angle_speed = self._route * self._speed / 80
            self._speed = 80

    def _update(self, deltatime):
        if not self._stop_trigger:
            if self.position[0] < -100 or self.position[1] < -100\
                    or self.position[0] - 100 > self._game.screen_size[0]\
                    or self.position[1] - 100 > self._game.screen_size[1]:
                self.restart()
            if not self._route:
                self._go_ahead()
            else:
                self._turn()
        else:
            self._angle_speed = 0
            self._speed = 0


class Bus(Car):
    pass


class TurnTrigger(BaseObject):
    def _start(self, routes=(0, -70, 160)):
        self._trigger = True

        self._routes = routes
        if not self._routes:
            self._routes = (0,)
        elif type(self._routes) == int:
            self._routes = (self._routes,)
        else:
            self._routes = []
            for i, v in enumerate(routes, start=1):
                self._routes += [v] * i
            self._routes = tuple(self._routes)

    @property
    def route(self):
        if len(self._routes) == 1:
            return self._routes[0]
        elif len(self._routes) > 1:
            return random.choice(self._routes)


class TrafficLights(BaseObject):
    _colors = {"Red": "Green", "Green": "Red"}

    def _start(self, on_time, off_time, fake=False):
        self._layer = 2
        self._alias = "TrafficLight"
        self._fake = fake
        if not self._color in self._colors:
            self._color = "Red"

        self._on_time = on_time
        self._off_time = off_time

        self._trigger = self.state
        self._reload_cycle_time()

    @property
    def state(self):
        if not self._fake:
            return self._color == "Red"
        return False

    def _change_light(self):
        self._color = self._colors[self._color]
        self._trigger = self.state
        self._reload_cycle_time()

    def _reload_cycle_time(self):
        self._cycle_time = self._on_time if self._colors[self._color] == "Red" else self._off_time

    def _update(self, deltatime):
        self._cycle_time -= deltatime
        if self._cycle_time < 0:
            self._change_light()
