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