import numpy as np
from sklearn.preprocessing import OneHotEncoder


class SaleMLDTO:
    def __init__(self, X: np.ndarray, y: np.ndarray, feature_names: list, 
                 categoria_encoder: OneHotEncoder, metodo_pago_encoder: OneHotEncoder):
        self.X = X
        self.y = y
        self.feature_names = feature_names
        self.categoria_encoder = categoria_encoder
        self.metodo_pago_encoder = metodo_pago_encoder