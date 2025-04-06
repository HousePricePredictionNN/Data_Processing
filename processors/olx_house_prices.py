import os
import pandas as pd
from processors.data_processor import DataProcessor

class OlxHousePricesProcessor(DataProcessor):
    """
    Class to process OLX house prices data from Kaggle.
    """
    def __init__(self):
        super().__init__('olx_house_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = os.path.join(base_dir, 'data', '4_olx_house_prices', 'raw')
        output_path = os.path.join(base_dir, 'data', '4_olx_house_prices', 'final')
        os.makedirs(output_path, exist_ok=True)
        return input_path, output_path

    def _read_data(self, input_path):
        """Read data from input path"""
        data_path = os.path.join(input_path, 'olx_house_price_Q122.csv')
        df = pd.read_csv(data_path, sep=',', encoding='utf-8-sig', low_memory=False)
        return df

    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        # df = df.drop('Column1', axis=1, errors='ignore')
        return df

    def _transform_data(self, df):
        """Transform data"""
        # Map from corrupted character sequences to correct Polish characters
        polish_char_corrections = {
            'Ĺ‚': 'ł',
            'Ĺ›': 'ś',
            'Ĺ„': 'ń', 
            'Ĺş': 'ź',
            'Ä…': 'ą',
            'Ĺ¼': 'ż',
            'Ä™': 'ę',
            'Ă³': 'ó',
            'Ĺ': 'Ł',
            'Ăł': 'ó',
            'Ł\x81': 'Ł',
            'Ł»': 'Ż',
            'Łš': 'Ś',
            'Ä‡': 'ć',
            'OŁĽ': 'Oż',
            'ŁĽ': 'ż',
            '\x81Ăł': 'łó',
            'Ł\x81Ăł': 'Łó',
            'ZamośÄ‡': 'Zamość',
            '\x81omŁĽ': 'Łomż',
            'Silesia': 'Śląska',
            'BrześÄ‡': 'Brześć',
            'SkarŁĽ': 'Skarż',
            'Ł\x81om': 'Łom'
        }

        month_map = {
            'January': 1, 'Jan': 1,
            'February': 2, 'Feb': 2,
            'March': 3, 'Mar': 3,
            'April': 4, 'Apr': 4,
            'May': 5,
            'June': 6, 'Jun': 6,
            'July': 7, 'Jul': 7,
            'August': 8, 'Aug': 8,
            'September': 9, 'Sep': 9, 'Sept': 9,
            'October': 10, 'Oct': 10,
            'November': 11, 'Nov': 11,
            'December': 12, 'Dec': 12
        }

        if 'month' in df.columns:
            # First standardize the month values (e.g., capitalize first letter)
            df['month'] = df['month'].str.strip().str.title()
            
            # Map the month names to their numeric values
            df['month'] = df['month'].map(month_map)
    
        for wrong, correct in polish_char_corrections.items():
            df['city_name'] = df['city_name'].str.replace(wrong, correct, regex=False)
            df['offer_title'] = df['offer_title'].str.replace(wrong, correct, regex=False)

        return df    
    
    def _save_data(self, df, output_path):
        """Save data to output path"""
        output_file_path = os.path.join(output_path, 'data_combined.csv')
        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)

        df_lodz = df[df['city_name'] == 'Łódź']
        output_file_path_lodz = os.path.join(output_path, 'data_combined_lodz.csv')
        df_lodz.to_csv(output_file_path_lodz, sep=';', encoding='utf-8', index=False)



