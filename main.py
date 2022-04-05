import pygame

from Engine import Game
from Engine.Base import BaseObject
from GameObjects import Car, TrafficLights, TurnTrigger, CarSpawn, Road, RoadLine, Bus

win = pygame.display.set_mode((1280, 1050))
game = Game(win, 60, "seagreen")


def road(game):
    game.add_object(Road(position=(950, 570), size=(90, 400), color="Black"))
    game.add_object(Road(position=(640, 815), size=(1280, 135), color="Black"))
    game.add_object(Road(position=(940, 325), size=(680, 90), color="Black"))
    game.add_object(Road(position=(645, 525), size=(135, 1050), color="Black"))
    game.add_object(Road(position=(120, 885), size=(45, 45), rotate=45, color="Black"))
    game.add_object(Road(position=(200, 894), size=(160, 45), color="Black"))
    game.add_object(Road(position=(280, 885), size=(45, 45), rotate=-45, color="Black"))

    game.add_object(RoadLine(position=(576, 370), size=(2, 750), color="White", trigger=True))
    game.add_object(RoadLine(position=(620, 560), size=(2, 375), color="White", trigger=True))
    game.add_object(RoadLine(position=(620, 130), size=(2, 300), color="White", trigger=True))
    game.add_object(RoadLine(position=(665, 560), size=(2, 375), color="White", trigger=True))
    game.add_object(RoadLine(position=(665, 130), size=(2, 300), color="White", trigger=True))
    game.add_object(RoadLine(position=(714, 560), size=(2, 375), color="White", trigger=True))
    game.add_object(RoadLine(position=(714, 130), size=(2, 300), color="White", trigger=True))

    game.add_object(RoadLine(position=(1000, 280), size=(570, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1000, 325), size=(570, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(808, 372), size=(190, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1140, 372), size=(287, 2), color="White", trigger=True))

    game.add_object(RoadLine(position=(905, 560), size=(2, 375), color="White", trigger=True))
    game.add_object(RoadLine(position=(950, 560), size=(2, 375), color="White", trigger=True))
    game.add_object(RoadLine(position=(995, 560), size=(2, 375), color="White", trigger=True))

    game.add_object(RoadLine(position=(285, 748), size=(585, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(285, 795), size=(585, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(285, 840), size=(585, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(285, 885), size=(585, 2), color="White", trigger=True))

    game.add_object(RoadLine(position=(810, 748), size=(190, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(810, 795), size=(190, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1140, 748), size=(287, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1140, 795), size=(287, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1000, 840), size=(570, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(1000, 885), size=(570, 2), color="White", trigger=True))

    game.add_object(RoadLine(position=(576, 970), size=(2, 170), color="White", trigger=True))
    game.add_object(RoadLine(position=(620, 970), size=(2, 170), color="White", trigger=True))
    game.add_object(RoadLine(position=(665, 970), size=(2, 170), color="White", trigger=True))
    game.add_object(RoadLine(position=(714, 970), size=(2, 170), color="White", trigger=True))

    game.add_object(RoadLine(position=(103, 903), size=(2, 45), rotate=-45, color="White", trigger=True))
    game.add_object(RoadLine(position=(200, 918), size=(164, 2), color="White", trigger=True))
    game.add_object(RoadLine(position=(297, 903), size=(2, 45), rotate=45, color="White", trigger=True))


def triggers(game, color="Black"):
    #975 770
    game.add_object(TurnTrigger(position=(875, 770), size=(1, 30), color=color, routes=(-150, )))
    game.add_object(TurnTrigger(position=(875, 820), size=(1, 30), color=color, routes=(-60,)))
    game.add_object(TurnTrigger(position=(1025, 770), size=(1, 30), color=color, routes=(150, )))
    game.add_object(TurnTrigger(position=(1025, 820), size=(1, 30), color=color, routes=(60,)))
    game.add_object(TurnTrigger(position=(925, 720), size=(30, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(975, 720), size=(30, 1), color=color, routes=(0,)))

    game.add_object(TurnTrigger(position=(925, 405), size=(30, 1), color=color, routes=(-130,)))
    game.add_object(TurnTrigger(position=(975, 405), size=(30, 1), color=color, routes=(130,)))
    game.add_object(TurnTrigger(position=(1030, 350), size=(1, 30), color=color, routes=(0, )))
    game.add_object(TurnTrigger(position=(870, 350), size=(1, 30), color=color, routes=(0,)))

    game.add_object(TurnTrigger(position=(770, 350), size=(1, 30), color=color, routes=(70, 10)))
    game.add_object(TurnTrigger(position=(745, 300), size=(1, 30), color=color, routes=(150,)))
    game.add_object(TurnTrigger(position=(665, 350), size=(1, 30), color=color, routes=(-120, )))

    game.add_object(TurnTrigger(position=(690, 250), size=(30, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(640, 250), size=(30, 1), color=color, routes=(1,)))
    game.add_object(TurnTrigger(position=(595, 250), size=(30, 1), color=color, routes=(1,)))
    game.add_object(TurnTrigger(position=(640, 375), size=(30, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(600, 390), size=(30, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(690, 390), size=(30, 1), color=color, routes=(1,)))
    game.add_object(TurnTrigger(position=(600, 720), size=(30, 1), color=color, routes=(140,)))
    game.add_object(TurnTrigger(position=(640, 710), size=(30, 1), color=color, routes=(-105, 0)))
    game.add_object(TurnTrigger(position=(685, 710), size=(30, 1), color=color, routes=(0,)))

    game.add_object(TurnTrigger(position=(545, 770), size=(1, 30), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(545, 815), size=(1, 30), color=color, routes=(0, -23)))
    game.add_object(TurnTrigger(position=(545, 860), size=(1, 30), color=color, routes=(0, 150)))

    game.add_object(TurnTrigger(position=(667, 795), size=(4, 4), color=color, routes=(30,)))

    game.add_object(TurnTrigger(position=(715, 770), size=(1, 30), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(715, 815), size=(1, 30), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(740, 860), size=(1, 30), color=color, routes=(0,)))

    game.add_object(TurnTrigger(position=(590, 910), size=(15, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(645, 942), size=(30, 1), color=color, routes=(0,)))
    game.add_object(TurnTrigger(position=(690, 910), size=(30, 1), color=color, routes=(150, 1, 1)))

    game.add_object(TurnTrigger(position=(10, 865), size=(1, 30), color=color, routes=(-1, )))
    game.add_object(TurnTrigger(position=(15, 880), size=(3, 3), color=color, routes=(30,)))
    game.add_object(TurnTrigger(position=(93, 880), size=(3, 3), color=color, routes=(-30,)))
    game.add_object(TurnTrigger(position=(280, 865), size=(1, 30), color=color, routes=(0, )))


def traffic_lights(game):
    game.add_object(TrafficLights(position=(550, 840), size=(5, 90), on_time=6000, off_time=10000))
    game.add_object(TrafficLights(position=(550, 775), size=(5, 45), on_time=6000, off_time=10000, fake=True))

    game.add_object(TrafficLights(position=(620, 720), size=(90, 5), on_time=10000, off_time=6000, color="Green"))
    game.add_object(TrafficLights(position=(689, 720), size=(45, 5), on_time=10000, off_time=6000, color="Green", fake=True))
    game.add_object(TrafficLights(position=(630, 910), size=(110, 5), on_time=10000, off_time=6000, color="Green", fake=True))
    game.add_object(TrafficLights(position=(699, 910), size=(25, 5), on_time=10000, off_time=6000, color="Green"))

    game.add_object(TrafficLights(position=(745, 325), size=(5, 90), on_time=6000, off_time=10000, color="Green"))

    game.add_object(TrafficLights(position=(620, 255), size=(90, 5), on_time=10000, off_time=6000))
    game.add_object(TrafficLights(position=(689, 255), size=(45, 5), on_time=10000, off_time=6000, fake=True))
    game.add_object(TrafficLights(position=(620, 400), size=(90, 5), on_time=10000, off_time=6000, fake=True))
    game.add_object(TrafficLights(position=(689, 400), size=(45, 5), on_time=10000, off_time=6000))

    bus_light = TrafficLights(position=(255, 905), size=(5, 10), on_time=1600, off_time=5200)
    bus_light.set_layer(-1)
    game.add_object(bus_light)


def cars(game):
    game.add_object(CarSpawn(positions=((-40, 820, 0), (690, 1050, -90), (1300, 305, 180), (-95, 865, 0),
                                        (1300, 770, 180), (1300, 820, 180), (600, -40, 90), (645, -40, 90))))
    game.add_object(Bus(position=(0, 865), size=(110, 30), color="White"))


road(game)
triggers(game, "Black")
cars(game)
traffic_lights(game)

game.start()
game.run_forever()
