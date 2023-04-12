import os

# ====================== KIVY
try:
    from kivy.config import Config
    # Tamanho da tela da aplicação
    Config.set('graphics', 'width', '900')
    Config.set('graphics', 'height', '400')

    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy import platform
    from kivy.properties import NumericProperty
    from kivy.graphics.vertex_instructions import Line
    from kivy.graphics.context_instructions import Color

    from kivy.core.window import Window
    # ATALHOS DO TECLADO NA APLICAÇÃO

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY

# IMPORT [message.py]
from msg import message

# IMPORT [GalaxyFunctions]
from GalaxyFunctions.Movement import MovementApp
from GalaxyFunctions.Movement import CoordinatesApp
# ====================== END OF IMPORTs
class PlatformCheck:
    """
        Checagem de plataforma da aplicação.

        ...

        FUNCTIONS
        ----------
        is_desktop : boolean
                return True ('linux', 'win', 'macosx') or False
    """
    def is_desktop(self):
        """
            Confirmar checagem com True ou False.
        """
        
        return True if platform in ('linux', 'win', 'macosx') else False

class MainWidget(Widget, MovementApp, CoordinatesApp, PlatformCheck):
    """
        Classe dos widgets.

        ...

        VARIABLES
        ----------
        perspective_point_x : any
        perspective_point_y : any

        line   : NoneType

        [LINHA VERTICAL]
        V_NB_LINES      : quantidade de linhas
        V_LINES_SPACING : espaço entre as linhas

        [LINHA HORIZONTAL]
        H_NB_LINES      : quantidade de linhas
        H_LINES_SPACING : espaço entre as linhas
    """

    # Transform.py
    from GalaxyFunctions.Transform import transform, transform_2D, transform_perspective

    # Keyboard.py
    from GalaxyFunctions.Keyboard import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 4
    V_LINES_SPACING = .1
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = .1
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f'INIT\nW: {self.width}\nH: {self.height}')
        self.init_vertical_lines()
        self.init_horizontal_lines()

        # class CoordinatesApp
        self.init_tiles()
        self.generate_tiles_coordinates()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def init_vertical_lines(self):
        """
            Gerar linhas na vertical.
        """

        with self.canvas:
            Color(1, 1, 1)
            
            # self.line = Line(
            #     points=[100, 0, 100, 100]
            # )

            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        """
            Gerar linhas na horizontal.
        """

        with self.canvas:
            Color(1, 1, 1)

            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_vertical_lines(self):
        """
            Atualizar a posição para manter as linhas verticais centralizadas.
        """
        # self.line.points = [center_x, 0, center_x, 100]
        start_index = -int(self.V_NB_LINES/2) + 1

        for i in range(start_index, start_index+self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        """
            Atualizar a posição para manter as linhas horizontais centralizadas.
        """

        start_index = -int(self.V_NB_LINES/2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

class Galaxy(App):
    """
        GALAXY application main class
    """

    pass

if __name__ == '__main__':
    try:
        os.system('cls')
        message.message()
        message.success()

        # ====================== KIVY
        Galaxy().run()

    except (AttributeError) as error:
        message.error(error)