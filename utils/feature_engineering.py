import pandas as pd
from datetime import datetime

def add_engineered_features(df):
    if 'price' in df.columns and 'area_sqm' in df.columns:
        df['price_per_sqm'] = df['price'] / df['area_sqm']
    if 'price_per_sqm' in df.columns and 'area_sqm' in df.columns:
        df['price'] = df['price_per_sqm'] * df['area_sqm']
        
    return df    