import os
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class WarsawFlatPrices(DataProcessor):
    def __init__(self):
        super().__init__('warsaw_flat_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'warsaw_flat_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'warsaw_flat_prices', 'final')

        return input_path, output_path
    
    def _read_data(self):
        """Read data from input path"""
        kaggle_3_data_path = os.path.join(self.input_path, 'Warsaw_flat_prices_25_Sep_22.csv')
        df_kaggle3 = pd.read_csv(kaggle_3_data_path, sep=',', encoding='utf-8', low_memory=False)
        return df_kaggle3
    
    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        return df
    
    def _transform_data(self, df):
        if 'Price' in df.columns and df['Price'].dtype == 'object':
            df['Price'] = df['Price'].str.replace(' ', '').str.replace('zł', '').str.replace('€', '').str.replace(',', '').str.replace('$', '').astype(float)
            
        # Clean price_per_sqm column
        if 'Price per m2' in df.columns and df['Price per m2'].dtype == 'object':
            df['Price per m2'] = df['Price per m2'] \
                                    .str.replace(' ', '') \
                                    .str.replace(',', '') \
                                    .str.replace('zł/m²', '') \
                                    .str.replace('€/m²', '') \
                                    .str.replace('$', '') \
                                    .str.replace('/m²', '') \
                                    .str.strip().astype(float) \
                                    
        # Clean area column
        if 'Size M2' in df.columns and df['Size M2'].dtype == 'object':
            df['Size M2'] = df['Size M2'].str.replace(' ', '').str.replace('m²', '').str.strip().astype(float)
            
        # Clean rooms column
        if 'Rooms' in df.columns and df['Rooms'].dtype == 'object':
            df['Rooms'] = df['Rooms'].str.extract(r'(\d+)').astype(int)
    
        # Add standard year and month columns for consistency with other datasets
        df['year'] = 2022
        df['month'] = 9
        df['city'] = 'Warszawa'

        return df
    
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)