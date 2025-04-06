import os
import pandas as pd
from processors.data_processor import DataProcessor

class FlatPricesProcessor(DataProcessor):
    def __init__(self):
        super().__init__('flat_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = os.path.join(base_dir, 'data', '3_flat_prices', 'raw')
        output_path = os.path.join(base_dir, 'data', '3_flat_prices', 'final')
        os.makedirs(output_path, exist_ok=True)
        return input_path, output_path
    
    def _read_data(self, input_path):
        """Read data from input path"""
        kaggle_3_data_path = os.path.join(input_path, 'Otodom_Flat_Listings.csv')
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
    
    def _save_data(self, df, output_path):
        """Save data to output path"""
        output_file_path = os.path.join(output_path, 'data_combined.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)

        df_lodz = df[df['City'] == 'Łódź']
        output_file_path_lodz = os.path.join(output_path, 'data_combined_lodz.csv')
        df_lodz.to_csv(output_file_path_lodz, sep=';', encoding='utf-8', index=False)


