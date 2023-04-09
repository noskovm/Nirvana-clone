from model import Model
from view import View


class Controller:
    """
    Контроллер. Отслеживает нажатие кнопок на представлении
    """

    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def on_add_layer_button_click(self):
        res = self.model.create_layer()
        self.view.network_view.print_new_layer(res)

    def main(self):
        self.view.main()  # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()
    controller.main()
