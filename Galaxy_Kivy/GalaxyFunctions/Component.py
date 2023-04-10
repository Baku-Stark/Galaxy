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