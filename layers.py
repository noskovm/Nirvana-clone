import torch


class LayerLinear:

    def __init__(self):
        self.layer = torch.nn.Linear()
        # todo Линейный слой должен знать размер входных данных


class LayerReLU:

    def __init__(self):
        self.layer = torch.nn.ReLU()


class LayersSequence:

    def __init__(self):
        self.layer = torch.nn.Sequential()

