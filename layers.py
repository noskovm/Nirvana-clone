import torch


class LayerLinear:

    def __init__(self, color, consumption, tank_volume, mileage=0):
        self.layer = torch.nn.Linear()

    def choto(self):
        print('Я слой')


class LayerReLU:

    def __init__(self, color, consumption, tank_volume, mileage=0):
        self.layer = torch.nn.ReLU()
        self.consumption = consumption
        self.tank_volume = tank_volume
        self.reserve = tank_volume
        self.mileage = mileage
        self.engine_on = False

    def choto(self):
        pass
