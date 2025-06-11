import os
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class AllegroPrices(DataProcessor):
    def __init__(self):
        super().__init__('allegro_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'allegro_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'allegro_prices', 'final')

        return input_path, output_path

    def _read_data(self):
        """Read data from input path"""
        data_path= os.path.join(self.input_path, 'data.csv')

        df = pd.read_csv(data_path, sep=',', encoding='utf-8', low_memory=False)

        return df
    
    def _clean_data(self, df):
        """Clean data"""
        # df = df.drop_duplicates()
        return df
    
    def _transform_data(self, df):
        # Extract date components safely
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)

