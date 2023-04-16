"""
    Menu da aplicação (main e game over).

    ...

    IMPORTs
    ----------
    import os

    import random

    from kivy.graphics.vertex_instructions import Quad
    
    from kivy.graphics.context_instructions import Color
"""
import os

# ====================== KIVY
try:
    from kivy.uix.relativelayout import RelativeLayout

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY
class MenuWidget(RelativeLayout):
    pass