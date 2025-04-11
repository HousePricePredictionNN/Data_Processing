import os
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class NumbersApartmentPrices(DataProcessor):
    def __init__(self):
        super().__init__('numbers_apartment_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'numbers_apartment_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'numbers_apartment_prices', 'final')

        self.output_paths['lodz'] = get_dataset_path(base_dir, 'numbers_apartment_prices', 'final', 'data_lodz.csv')

        return input_path, output_path

    def _read_data(self):
        """Read data from input path"""
        data_path = os.path.join(self.input_path, 'OTODOM_DATA_TRANSFORMED.csv')
        df = pd.read_csv(data_path, sep=';', encoding='utf-8', low_memory=False)

        return df
    
    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        df.drop('DESCRIPTION', axis=1, errors='ignore', inplace=True)
        return df
    
    def _transform_data(self, df):
        df['listing_year'] = df['TIMESTAMP'].apply(lambda x: int(str(x).split('-')[0]))
        df['listing_month'] = df['TIMESTAMP'].apply(lambda x: int(str(x).split('-')[1]))

        df.drop('TIMESTAMP', axis=1, inplace=True)
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)

        df_lodz = df[df['CITY'] == 'Łódź']
        df_lodz.to_csv(self.output_paths['lodz'], sep=';', encoding='utf-8', index=False)

