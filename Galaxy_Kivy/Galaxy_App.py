import os
import message

# ====================== KIVY
try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.properties import NumericProperty

except ModuleNotFoundError:
    os.system('python -m pip install "kivy[base]" --pre --extra-index-url https://kivy.org/downloads/simple/')
# ====================== END OF KIVY

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print(f'INIT\nW: {self.width}\nH: {self.height}')

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

            Args
                :self   -> class
                :widget -> Janela da aplicação
                :value  -> valor de LARGURA
        """
        print(f'PX: {str(value)}')

    def on_perspective_point_y(self, widget, value):
        """
            Mostra apenas o valor de ALTURA(Y)

            Args
                :self   -> class
                :widget -> Janela da aplicação
                :value  -> valor de ALTURA
        """
        print(f'PY: {str(value)}')

class Galaxy(App):
    pass

if __name__ == '__main__':
    try:
        os.system('cls')
        message.message()
        message.sucess()

        # ====================== KIVY
        Galaxy().run()

    except Exception:
        message.error(Exception)