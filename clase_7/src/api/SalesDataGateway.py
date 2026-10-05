import pandas as pd
import io
from app_collections.SalesCollection import SalesCollection


class SalesDataGateway:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def get_data(self) -> SalesCollection:
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        header_line = lines[0].strip() + lines[1].strip()
        data_lines = lines[2:]
        
        full_content = header_line + '\n' + ''.join(data_lines)
        df = pd.read_csv(io.StringIO(full_content))
        df = df.dropna(subset=['fecha'])
        return SalesCollection.from_dataframe(df)