from model import Model
from view import MainFrame


class Controller:
    """
    Контроллер
    """

    def __init__(self):
        self.model = Model()
        self.view = MainFrame(self)

    def main(self):
        self.view.start()    # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()
    controller.main()
