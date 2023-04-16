"""
    Movimentos da arena e coordenadas.

    ...

    IMPORTs
    ----------
    import os

    import random

    from kivy.graphics.vertex_instructions import Quad
    
    from kivy.graphics.context_instructions import Color
"""

import os
import random

# ====================== KIVY
try:
    from kivy.graphics.vertex_instructions import Quad
    from kivy.graphics.context_instructions import Color

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY
class CollisionsApp:
    """
        Colisões da nave.
        
        ...

        FUNCTIONS
        ----------
        update : (dt)
                Animação das linhas
    """

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]

            if ti_y > self.current_y_loop + 1:
                return False
            
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True

        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinates(ti_x+1, ti_y+1)

        for i in range(0, 3):
            px, py = self.ship_coordinates[i]

            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
            
        return False
            
class CoordinatesApp:
    """
        Classe de coordenadas do campo.
        
        ...

        FUNCTIONS
        ----------
        get_line_x_from_index : (index)
            Coordenadas horizontal.

        get_line_y_from_index : (index)
            Coordenadas vertical.

        get_tile_coordinates : (ti_x, ti_y)
            Pegar as coordenadas das fitas X e Y

        init_tiles : any
            Criar uma fita e iniciar o processo de desenvolvimento.

        update_tiles : any
            Atualizar coordenadas das fitas para preencher o campo.

        generate_tiles_coordinates : any
            Gerar novas coordenadas para a movimentação do campo.

        pre_fill_tiles_coordinates : any
            Gerar linhas retas (qtd: 10).

        ...
    
        VARIABLES
        ----------
        NB_TILES : int
            Números de fitas.

        tiles : list[]
            Lista com quantidades de fitas.

        tiles_coordinates : list[]
            Coordenadas das fitas.
    """

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
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)

        return x, y
    
    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def update_tiles(self):
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]

            tile_coordinates = self.tiles_coordinates[i]

            xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])

            xmax, ymax = self.get_tile_coordinates(tile_coordinates[0]+1, tile_coordinates[1]+1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [
                x1, y1,
                x2, y2,
                x3, y3,
                x4, y4
            ]

    def generate_tiles_coordinates(self):
        last_x = 0
        last_y = 0

        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1
    
        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            # 0 -> straight
            # 1 -> right
            # 2 -> left

            start_index = -int(self.V_NB_LINES/2) + 1
            end_index = start_index + self.V_NB_LINES - 1
            
            if last_x <= start_index:
                r = 1

            if last_x >= end_index:
                r = 2
             
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))

                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))

                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))

            last_y += 1

    def pre_fill_tiles_coordinates(self):
        """
            10 fitas em uma linha reta.
        """

        for i in range(0, 10+self.delay):
            self.tiles_coordinates.append((0, i))

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
        
    def update(self, dt):
        """
            Atualização para efeito de animação.
        """

        # print('update')
        # print(f"dt: {str(dt*60)}")
        time_factor = dt * 60
        
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_LINES_SPACING * self.height

            while self.current_offset_y >= spacing_y:
                # GERANDO LINHAS INFINITAS (looping)
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.points_game = f"SCORE: {str(self.current_y_loop)}"
                self.generate_tiles_coordinates()

            speed_x = self.current_speed_x * self.width / 100

            # controle do teclado [ativação]
            self.current_offset_x += speed_x * time_factor

        # verificar colisão e GAME OVER
        if not self.check_ship_collision() and not self.state_game_over:
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            self.sound_gameover_voice.play()
            self.state_game_over = True
            self.menu_widget.opacity = 1

            self.menu_title = "GAME OVER !"
            self.menu_button_title = "RESTART"