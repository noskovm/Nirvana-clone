from model import Model
from view import View


class Controller:
    """
    Контроллер. Отслеживает нажатие кнопок на представлении
    """

    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def print_layer(self, name_layer):
        """
        Только отрисовка слоя с именем
        """

        self.view.network_view.print_new_layer(name_layer)

    def add_layer(self, layer_meta_view):
        """
        Добавляет экзепляр представления слоя
        """

        self.model.add_layer(layer_meta_view)

    def main(self):
        self.view.main()  # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()
    controller.main()
