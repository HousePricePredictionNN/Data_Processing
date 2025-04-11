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
        data_path_new = os.path.join(self.input_path, 'properties_new.csv')
        data_path_old = os.path.join(self.input_path, 'properties_old.csv')

        df_new = pd.read_csv(data_path_new, sep=',', encoding='utf-8', low_memory=False) 
        df_new.rename(columns={
            'Cena za m2 (zł)': 'Cena za m²',
        })
        
        df_old = pd.read_csv(data_path_old, sep=',', encoding='utf-8', low_memory=False)   


        df = pd.concat([df_new, df_old], ignore_index=True)
        return df
    
    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        return df
    
    def _transform_data(self, df):
        # Extract date components safely
        if 'end_date' in df.columns:
            df['listing_year'] = df['end_date'].str.split(' ').str[0].str.split('.').str[2].astype(int)
            df['listing_month'] = df['end_date'].str.split(' ').str[0].str.split('.').str[1].astype(int)
        
        # Handle different price column names
        if 'Cena za m²' in df.columns:
            price_col = 'Cena za m²'
        elif 'Cena za m2 (zł)' in df.columns:
            price_col = 'Cena za m2 (zł)'
        else:
            # Create empty column if neither exists
            df['price'] = None
            price_col = None
        
        # Calculate price only if both columns exist
        if price_col and 'Powierzchnia' in df.columns:
            calculated_prices = df[price_col] * df['Powierzchnia']
            df['price'] = df['price'].fillna(calculated_prices)
        
        df['city'] = 'Łódź'
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)

