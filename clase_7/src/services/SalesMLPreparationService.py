import numpy as np
import pandas as pd
from app_collections.SalesCollection import SalesCollection
from entities.Sale import Sale
from dto.SaleMLDTO import SaleMLDTO
from sklearn.preprocessing import OneHotEncoder
from typing import List


class SalesMLPreparationService:
    def __init__(self, sales_collection: SalesCollection):
        self.sales_collection = sales_collection
        self.categoria_encoder = None
        self.metodo_pago_encoder = None
        self.feature_names = None

    def fit_encoders(self):
        df = self.sales_collection.to_dataframe()
        
        self.categoria_encoder = OneHotEncoder(sparse_output=False)
        self.categoria_encoder.fit(df[['categoria']])
        
        self.metodo_pago_encoder = OneHotEncoder(sparse_output=False)
        self.metodo_pago_encoder.fit(df[['metodo_pago']])
        
        cat_features = self.categoria_encoder.get_feature_names_out(['categoria'])
        pago_features = self.metodo_pago_encoder.get_feature_names_out(['metodo_pago'])
        self.feature_names = ['precio_unitario', 'cantidad', 'cliente_edad'] + list(cat_features) + list(pago_features)

    def transform(self) -> SaleMLDTO:
        df = self.sales_collection.to_dataframe()
        
        df_clean = df.copy()
        median_age = df_clean['cliente_edad'].median()
        df_clean['cliente_edad'] = df_clean['cliente_edad'].fillna(median_age)
        df_clean['total_venta'] = df_clean['precio_unitario'] * df_clean['cantidad']
        
        cat_encoded = self.categoria_encoder.transform(df_clean[['categoria']])
        pago_encoded = self.metodo_pago_encoder.transform(df_clean[['metodo_pago']])
        
        cat_features = self.categoria_encoder.get_feature_names_out(['categoria'])
        pago_features = self.metodo_pago_encoder.get_feature_names_out(['metodo_pago'])
        
        X = np.hstack([
            df_clean[['precio_unitario', 'cantidad', 'cliente_edad']].values,
            cat_encoded,
            pago_encoded
        ])
        
        y = df_clean['total_venta'].values
        
        return SaleMLDTO(
            X=X,
            y=y,
            feature_names=['precio_unitario', 'cantidad', 'cliente_edad'] + list(cat_features) + list(pago_features),
            categoria_encoder=self.categoria_encoder,
            metodo_pago_encoder=self.metodo_pago_encoder
        )

    def prepare_and_save(self, output_path: str) -> SaleMLDTO:
        self.fit_encoders()
        ml_dto = self.transform()
        
        df_ml = pd.DataFrame(ml_dto.X, columns=ml_dto.feature_names)
        df_ml['total_venta'] = ml_dto.y
        
        df_ml.to_csv(output_path, index=False)
        print(f"\nDataset preparado guardado como '{output_path}'")
        
        return ml_dto