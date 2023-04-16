import os

# ====================== KIVY
try:
    from kivy.config import Config
    # Tamanho da tela da aplicação
    Config.set('graphics', 'width', '900')
    Config.set('graphics', 'height', '400')

    from kivy.app import App
    from kivy import platform
    from kivy.lang import Builder
    from kivy.properties import Clock
    from kivy.properties import ObjectProperty
    from kivy.properties import StringProperty
    from kivy.properties import NumericProperty
    from kivy.uix.relativelayout import RelativeLayout
    from kivy.graphics.vertex_instructions import Line
    from kivy.graphics.context_instructions import Color
    from kivy.graphics.vertex_instructions import Triangle

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
from GalaxyFunctions.Movement import CollisionsApp
# ====================== END OF IMPORTs
Builder.load_file("GalaxyFunctions/Menu.kv")
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

class MainWidget(RelativeLayout, MovementApp, CoordinatesApp, CollisionsApp, PlatformCheck):
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

    V_NB_LINES = 8
    V_LINES_SPACING = .4
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = .1
    horizontal_lines = []

    delay = 4
    NB_TILES = 8 + 4
    tiles = []
    tiles_coordinates = []

    SPEED = .8
    SPEED_X = 3.0

    current_offset_x = 0
    current_offset_y = 0

    current_speed_x = 0
    current_y_loop = 0

    state_game_over = False
    state_game_has_started = False
    points_game = StringProperty("---")

    menu_widget = ObjectProperty()

    SHIP_WIDTH = .09
    SHIP_HEIGHT = 0.050
    SHIP_BASE_Y = 0.04
    ship = None
    ship_coordinates = []

    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("START")

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f'INIT\nW: {self.width}\nH: {self.height}')

        self.init_vertical_lines()
        self.init_horizontal_lines()

        # class CoordinatesApp
        self.init_tiles()
        # main
        self.init_ship()

        self.reset_game()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width / 2
        ship_half_width = self.SHIP_WIDTH * self.width / 2
        
        base_y = self.SHIP_BASE_Y * self.height
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates = [
            (center_x - ship_half_width, base_y),
            (center_x, base_y + ship_height),
            (center_x + ship_half_width, base_y)
        ]

        x1, y1 = self.transform(*self.ship_coordinates[0])
        
        x2, y2 = self.transform(*self.ship_coordinates[1])

        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [
            x1, y1,
            x2, y2,
            x3, y3
        ]
    
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
    
    def on_menu_button_pressed(self):
        """
            Iniciar jogo.
        """

        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0

    def reset_game(self):
        """
            Reiniciar jogo.
        """

        self.current_offset_x = 0
        self.current_offset_y = 0

        self.current_speed_x = 0
        self.current_y_loop = 0

        self.tiles_coordinates = []
        
        # main
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False


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

    except KeyboardInterrupt:
        message.Interrupt()