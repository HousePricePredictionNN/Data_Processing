import pandas as pd
import os

class AverageApartmentPricesProcessor:
    """
    Class to process average apartment prices data from Kaggle.
    """
    def __init__(self, data_path):
        self.data_path = data_path

    def process(self, current_dir):

        kaggle_6_data_path = os.path.join(current_dir, 'data', '6kaggle', 'poland_real_estate_prices_2006_2017.csv')

        df_kaggle6 = pd.read_csv(kaggle_6_data_path, sep=',', encoding='utf-8')
        print(df_kaggle6.head())
        print(df_kaggle6.shape)
        print(df_kaggle6.columns)

        df_kaggle6_lodz = df_kaggle6[df_kaggle6['City'] == 'Lodz']
        print(df_kaggle6_lodz.head())
        print(df_kaggle6_lodz.shape)
