import os
import glob
import pandas as pd
from processors.data_processor import DataProcessor
from utils.path_utils import get_dataset_path

class ApartmentPricesProcessor(DataProcessor):
    def __init__(self):
        super().__init__('apartment_prices')

    def _get_paths(self, base_dir):
        """Define input/output paths"""
        input_path = get_dataset_path(base_dir, 'apartment_prices', 'raw')
        output_path = get_dataset_path(base_dir, 'apartment_prices', 'final')

        self.output_paths['lodz'] = get_dataset_path(base_dir, 'apartment_prices', 'final', 'data_lodz.csv')

        return input_path, output_path

    def _read_data(self):
        """Read data from input path"""
        pattern = os.path.join(self.input_path, 'apartments_pl_*.csv')
        csv_files = glob.glob(pattern)

        filtered_files = []
        for file in csv_files:
            basename = os.path.basename(file)
            if basename.startswith('apartments_pl_') and basename.endswith('.csv'):
                filtered_files.append(file)
        filtered_files.sort()

        dfs = []
        for file in filtered_files:
            df = pd.read_csv(file, sep=',', encoding='utf-8', low_memory=False)
            basename = os.path.basename(file)
            date_part = basename[14:-4]
            year, month = date_part.split('_')
            df['year'] = int(year)
            df['month'] = int(month)
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    def _clean_data(self, df):
        """Clean data"""
        df = df.drop_duplicates()
        df.drop('id', axis=1, inplace=True)
        df = df[df['price'] > 0]
        return df

    def _transform_data(self, df):
        return df
    
    def _save_data(self, df):
        """Save data to output path"""
        output_file = os.path.join(self.output_path, 'data.csv')
        df.to_csv(output_file, sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Saved combined data to {output_file}")

        df_lodz = df[df['city'] == 'lodz']
        df_lodz.to_csv(self.output_paths['lodz'], sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Saved Lodz data with {df_lodz.shape[0]} rows")