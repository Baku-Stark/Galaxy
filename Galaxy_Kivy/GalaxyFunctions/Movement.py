"""
    Movimentos da arena.
"""

import os

# ====================== KIVY
try:
    from kivy.properties import Clock

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY

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
    def __init__(self):
        # super(MainWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        

    def update(self, dt):
        # print('update')
        self.update_vertical_lines()
        self.update_horizontal_lines()

        self.current_offset_y += self.SPEED

        spacing_y = self.H_LINES_SPACING * self.height

        if self.current_offset_y >= spacing_y:
            # GERANDO LINHAS INFINITAS
            self.current_offset_y -= spacing_y