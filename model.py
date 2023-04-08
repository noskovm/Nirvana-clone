from layers import *


class Model:
    """
    Модель. Отвечает за данные и исполнение вычислительных процессов
    """

    def __init__(self):
        pass

    def create_layer(self):
        new_layer = LayerReLU()
        return new_layer
