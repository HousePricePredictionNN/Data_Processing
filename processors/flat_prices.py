import os
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class FlatPricesProcessor(DataProcessor):
    def __init__(self):
        super().__init__('flat_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'flat_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'flat_prices', 'final')

        self.output_paths['lodz'] = get_dataset_path(base_dir, 'flat_prices', 'final', 'data_lodz.csv')

        return input_path, output_path
    
    def _read_data(self):
        """Read data from input path"""
        kaggle_3_data_path = os.path.join(self.input_path, 'Otodom_Flat_Listings.csv')
        df_kaggle3 = pd.read_csv(kaggle_3_data_path, sep=',', encoding='utf-8', low_memory=False)
        return df_kaggle3
    
    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        return df
    
    def _transform_data(self, df):
        df['year'] = 2023
        df['month'] = 11
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Saved combined data to {output_file_path}")

        df_lodz = df[df['City'] == 'Łódź']
        df_lodz.to_csv(self.output_paths['lodz'], sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Saved Lodz data with {df_lodz.shape[0]} rows")


