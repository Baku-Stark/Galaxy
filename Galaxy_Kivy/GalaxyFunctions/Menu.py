"""
    Menu da aplicação (main e game over).

    ...

    IMPORTs
    ----------
    import os

    from kivy.uix.relativelayout import RelativeLayout
"""
import os

# ====================== KIVY
try:
    from kivy.uix.relativelayout import RelativeLayout

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY
class MenuWidget(RelativeLayout):
    """
        Menu da aplicação (main e game over).

        ...

        FUNCTIONS
        ----------
        on_menu_button_pressed : (self)
    """
    def on_touch_down(self, touch):
        """
            Atalhos de botões (mouse) ESQUERDA e DIREITA
        """

        if self.opacity == 0:

            return False

        return super(RelativeLayout, self).on_touch_down(touch)