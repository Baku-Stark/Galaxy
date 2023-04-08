import os

# IMPORT [message.py]
from msg import message

# ====================== KIVY
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.properties import NumericProperty
    from kivy.graphics.vertex_instructions import Line
    from kivy.graphics.context_instructions import Color

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY

class MainWidget(Widget):
    """
        Classe dos widgets.

        ...

        VARIABLES
        ----------
        perspective_point_x : any
        perspective_point_y : any

        line   : NoneType

        V_LINES_SPACING : percentage in screen width
    """

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 7
    V_LINES_SPACING = .1
    vertical_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f'INIT\nW: {self.width}\nH: {self.height}')
        self.init_vertical_lines()

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

        self.update_vertical_lines()

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
        with self.canvas:
            Color(1, 1, 1)
            
            # self.line = Line(
            #     points=[100, 0, 100, 100]
            # )

            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        # self.line.points = [center_x, 0, center_x, 100]

        center_line_x = int(self.width / 2)
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2)

        for i in range(0, self.V_NB_LINES):
                line_x = int(center_line_x + offset * spacing)
                self.vertical_lines[i].points = [line_x, 0, line_x, self.height]
                offset += 1

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