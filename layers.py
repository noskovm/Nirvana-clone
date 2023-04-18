import torch


def make_linear_layer(parameters):
    in_f = parameters['in_features']
    out_f = parameters['out_features']

    layer = torch.nn.Linear(in_features=in_f, out_features=out_f)
    return layer


def make_relu_layer():
    layer = torch.nn.ReLU()
    return layer


class LayerReLU:

    def __init__(self):
        self.layer = torch.nn.ReLU()


class LayersSequence:

    def __init__(self):
        self.layer = torch.nn.Sequential()
