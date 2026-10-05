from services.MovementDataPreparationService import MovementDataPreparationService
import pandas as pd


class MovementDataPreparationController:
    def __init__(self, preparation_service: MovementDataPreparationService = None):
        self.service = preparation_service or MovementDataPreparationService()

    def prepare_data(self) -> pd.DataFrame:
        df_prepared, _ = self.service.prepare_full_pipeline()
        return df_prepared

    def get_eda_findings(self) -> dict:
        if not self.service.eda_findings:
            self.service.perform_eda()
        return self.service.eda_findings

    def get_eda_summary(self) -> str:
        return self.service.get_eda_summary()

    def save_prepared_data(self, output_path: str = 'data_prepared.csv'):
        self.service.save_prepared_data(output_path)

    def get_raw_dataframe(self) -> pd.DataFrame:
        if self.service.df_raw is None:
            self.service.load_data()
        return self.service.df_raw

    def get_clean_dataframe(self) -> pd.DataFrame:
        if self.service.df_clean is None:
            self.service.clean_data()
        return self.service.df_clean

    def get_prepared_dataframe(self) -> pd.DataFrame:
        if self.service.df_prepared is None:
            self.prepare_data()
        return self.service.df_prepared