import os

# IMPORT [message.py]
from msg import message

# IMPORT [GalaxyFunctions]
from GalaxyFunctions.Movement import MovementApp

# ====================== KIVY
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.properties import NumericProperty
    from kivy.graphics.vertex_instructions import Line
    from kivy.graphics.context_instructions import Color

    from kivy.config import Config
    # Tamanho da tela da aplicação
    Config.set('graphics', 'width', '900')
    Config.set('graphics', 'height', '400')

    from kivy.core.window import Window
    # ATALHOS DO TECLADO NA APLICAÇÃO

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY

class MainWidget(Widget, MovementApp):
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

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10
    V_LINES_SPACING = .25
    vertical_lines = []

    H_NB_LINES = 15
    H_LINES_SPACING = .1
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f'INIT\nW: {self.width}\nH: {self.height}')
        self.init_vertical_lines()
        self.init_horizontal_lines()

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X

        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        """
            Atalhos de botões (mouse) ESQUERDA e DIREITA
        """
        if touch.x < self.width/2:
            self.current_speed_x = self.SPEED_X

        else:
            self.current_speed_x = -self.SPEED_X

    def on_touch_up(self, touch):
        """
            Atalhos de botões (mouse) CIMA e BAIXO
        """
        self.current_speed_x = 0

    def on_parent(self, widget, parent):
        # print(f'ON PARENT\nW: {self.width}\nH: {self.height}')
        pass

    def on_size(self, *args):
        """
            Mostra os valores de LARGURA e ALTURA da janela quando alterada.
        """

        print(f'=====>  ] [ON SIZE     ]\nW: {self.width}\nH: {self.height}\n======')
        print('')

        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height * 0.75

    def on_perspective_point_x(self, widget, value):
        """
            Mostra apenas o valor de LARGURA(X)

            Args:

                self   : class
                widget : Janela da aplicação
                value  : valor de LARGURA
        """

        print(f'PX: {str(value)}')

    def on_perspective_point_y(self, widget, value):
        """
            Mostra apenas o valor de ALTURA(Y)

            Args:

                self   : class
                widget : Janela da aplicação
                value  : valor de LARGURA
        """

        print(f'PY: {str(value)}')

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

        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2) + 0.5

        for i in range(0, self.V_NB_LINES):
            line_x = center_line_x + offset * spacing + self.current_offset_x

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

            offset += 1

    def update_horizontal_lines(self):
        """
            Atualizar a posição para manter as linhas horizontais centralizadas.
        """

        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = int(self.V_NB_LINES/2) - 0.5

        xmin = center_line_x - offset * spacing + self.current_offset_x
        xmax = center_line_x + offset * spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height


        for i in range(0, self.H_NB_LINES):
            line_y = i * spacing_y - self.current_offset_y

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        """
            Transformar as linhas para a perspectiva 2D/3D.
        """

        #return self.transform_2D(x, y)
        return self.transform_perspective(x, y)
    
    def transform_2D(self, x:int, y:int):
        """
            Transformar para 2D.
        """

        return x, y
    
    def transform_perspective(self, x:int, y:int):
        """
            Criar a perspetiva do cenário.
        """

        lin_y = y * self.perspective_point_y / self.height

        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 2) #número de vezes que será multiplicado

        # TRANSFORM [X]
        tr_x = self.perspective_point_x + diff_x * factor_y

        # TRANSFORM [Y]
        tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

        return tr_x, tr_y

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