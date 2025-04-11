import pandas as pd
from config.column_mappings import COLUMN_MAPPINGS

def standardize_dataframe(df, dataset_name, column_mappings=COLUMN_MAPPINGS):
    mapper = column_mappings.get(dataset_name, {})

    standard_df = pd.DataFrame()

    # standard_df['source_dataset'] = dataset_name

    for source_col, target_col in mapper.items():
        if source_col in df.columns:
            standard_df[target_col] = df[source_col]

    return standard_df

def ensure_standard_columns(df, required_columns, optional_columns):
    missing_required = set(required_columns) - set(df.columns)

    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")

    for col in optional_columns:
        if col not in df.columns:
            df[col] = pd.NA  

    return df

def standardize_data_types(df):
    numeric_cols = ['price', 'area_sqm', 'rooms', 'floor', 'price_per_sqm']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')        

    bool_cols = ['has_parking', 'has_balcony', 'has_elevator', 'has_security']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].fillna(False).astype(bool)

    if 'listing_year' in df.columns:
        df['listing_year'] = df['listing_year'].astype('Int64')
    if 'listing_month' in df.columns:
        df['listing_month'] = df['listing_month'].astype('Int64')       

    return df

