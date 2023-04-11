from model import Model
from view import View


class Controller:
    """
    Контроллер. Отслеживает нажатие кнопок на представлении
    """

    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def on_add_linear_button_click(self):
        res = self.model.add_layer('linear')
        self.view.network_view.print_new_layer(res)

    def on_add_relu_button_click(self):
        res = self.model.add_layer('relu')
        self.view.network_view.print_new_layer(res)

    def main(self):
        self.view.main()  # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()
    controller.main()
