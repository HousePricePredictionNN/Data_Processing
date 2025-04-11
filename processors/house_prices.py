import os
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class HousePricesProcessor(DataProcessor):
    def __init__(self):
        super().__init__('house_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'house_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'house_prices', 'final')

        return input_path, output_path
        
    def _read_data(self):
        """Read data from input path"""
        kaggle_2_data_path = os.path.join(self.input_path, 'Houses.csv')
        df_kaggle2 = pd.read_csv(kaggle_2_data_path, sep=',', encoding='latin-1', low_memory=False)
        return df_kaggle2
    
    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        df = df.drop('Column1', axis=1, errors='ignore')
        return df
    
    def _transform_data(self, df):
        """Transform data"""
        # Map from corrupted character sequences to correct Polish characters
        polish_char_corrections = {
            # Original mappings
            'ï¿½': 'ą',
            'ï¿½': 'ć',
            'ï¿½': 'ę',
            'ï¿½': 'ł',
            'ï¿½': 'ń',
            'ï¿½': 'ó',
            'ï¿½': 'ś',
            'ï¿½': 'ź',
            'ï¿½': 'ż',
            'żw': 'ów',
            'żud': 'łud',
            'żawi': 'ławi',
            'żka': 'łęka',
            'Biażo': 'Biało',
            'żowicka': 'Łowicka',
            'żę': 'łę',
            'Poznaż': 'Poznań',
            'Krakżw': 'Kraków',
            'Mokotżw': 'Mokotów',
            'Pożudnie': 'Południe',
            'Podgżrze': 'Podgórze',
            'Zabżocie': 'Zabłocie',
            'Stanisżawa': 'Stanisława',
            'Praga-Pożudnie': 'Praga-Południe',
            'Podgżrze Zabżocie': 'Podgórze Zabłocie'
        }

        for wrong, correct in polish_char_corrections.items():
            df['address'] = df['address'].str.replace(wrong, correct, regex=False)
            df['city'] = df['city'].str.replace(wrong, correct, regex=False)

        year_extracted = df['year'].astype(str).str.extract(r'(\d{4})')[0]
        # Convert to nullable integer type
        df['year'] = pd.to_numeric(year_extracted, errors='coerce').astype('Int64')
        df.rename(columns={'year': 'build_year'}, inplace=True)
        df = df[(df['build_year'] > 1800) & (df['build_year'] < 2022)]
        df['month'] = 2
        df['year'] = 2021
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file_path = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Saved combined data to {output_file_path}")