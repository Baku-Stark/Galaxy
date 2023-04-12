"""
    Movimentos da arena e coordenadas.
"""

import os

# ====================== KIVY
try:
    from kivy.properties import Clock
    from kivy.graphics.vertex_instructions import Quad
    from kivy.graphics.context_instructions import Color

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY
class CoordinatesApp:
    """
        Classe de coordenadas do campo.
        
        ...

        FUNCTIONS
        ----------
        get_line_x_from_index : (index)
                Coordenadas horizontal.
    """

    tile = None
    ti_x = 1
    ti_y = 2

    def get_line_x_from_index(self, index):
        center_line_x = self.perspective_point_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = center_line_x + offset * spacing + self.current_offset_x

        return line_x
    
    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y

        return line_y

    def get_tile_coordinates(self, ti_x, ti_y):
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)

        return x, y
    
    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            
            self.tile = Quad()

    def update_tiles(self):
        xmin, ymin = self.get_tile_coordinates(self.ti_x, self.ti_y)
        xmax, ymax = self.get_tile_coordinates(self.ti_x+1, self.ti_y+1)

        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        self.tile.points = [
            x1, y1,
            x2, y2,
            x3, y3,
            x4, y4
        ]


class MovementApp:
    """
        Classe do movimento das linhas.

        ...

        IMPORTs
        ----------
        from kivy.properties import Clock
        
        ...

        FUNCTIONS
        ----------
        update : (dt)
                Animação das linhas
    """

    SPEED = 4
    SPEED_X = 12

    current_offset_x = 0
    current_offset_y = 0

    current_speed_x = 0

    def __init__(self):
        # super(MainWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
    def update(self, dt):
        """
            Atualização para efeito de animação.
        """

        # print('update')
        # print(f"dt: {str(dt*60)}")
        time_factor = dt * 60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        CoordinatesApp.update_tiles(self)

        # self.current_offset_y += self.SPEED * time_factor

        spacing_y = self.H_LINES_SPACING * self.height

        if self.current_offset_y >= spacing_y:
            # GERANDO LINHAS INFINITAS
            self.current_offset_y -= spacing_y

        # self.current_offset_x += self.current_speed_x * time_factor