import logging
import pandas as pd
import warnings
from utils.standardization import standardize_dataframe, ensure_standard_columns, standardize_data_types
from config.config import REQUIRED_COLUMNS, OPTIONAL_COLUMNS
from utils.path_utils import get_dataset_path
from utils.feature_engineering import add_engineered_features
from utils.validation import validate_dataset
from config.city_mappings import get_complete_city_mapping
import os

# Suppress FutureWarning about DataFrame concatenation
warnings.filterwarnings('ignore', message='.*concatenation with empty or all-NA entries.*', category=FutureWarning)

class DatasetIntegrator:
    def __init__(self, column_mappings, base_dir=None):
        self.column_mappings = column_mappings
        self.logger = logging.getLogger(__name__)
        self.base_dir = base_dir

    def integrate_datasets(self, base_dir):
        self.logger.info("Starting dataset integration")

        processed_dfs = {}

        for dataset_name in self.column_mappings.keys():
            try:
                df = self._load_processed_data(base_dir, dataset_name)

                if df.empty:
                    self.logger.warning(f"No data found for {dataset_name}. Skipping integration.")
                    continue
                
                # Transform data to standard schema
                standardized_df = standardize_dataframe(df, dataset_name, self.column_mappings)

                # Ensure all required columns exist
                standardized_df = ensure_standard_columns(standardized_df, REQUIRED_COLUMNS, OPTIONAL_COLUMNS)

                # Standardize data types
                standardized_df = standardize_data_types(standardized_df)
                
                # Store in directory
                processed_dfs[dataset_name] = standardized_df
                self.logger.info(f"Successfully processed {dataset_name} with {len(standardized_df)} records")
            except Exception as e:
                self.logger.error(f"Error processing {dataset_name}: {e}")
                continue

        if processed_dfs:
            combined_df = pd.concat(processed_dfs.values(), ignore_index=True)
            self.logger.info(f"Combined dataset has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns")

            # Apply post processing
            combined_df = self._post_process(combined_df, base_dir)

            # final_columns = [
            #     # Core identification and source
            #     'source_url',
                
            #     # Basic property details
            #     'price',
            #     'area_sqm',
            #     'rooms',
            #     'property_type',
                
            #     # Location information
            #     'address',
            #     'city',
            #     'district',
            #     'voivodeship',
            #     'latitude',
            #     'longitude',
            #     'distance_to_center',
            #     'city_population',
                
            #     # Property characteristics
            #     'floor',
            #     'floor_count',
            #     'build_year',
            #     'condition',
            #     'market_type',
            #     'building_type',
            #     'building_material',
            #     'heating_type',
            #     'ownership_type',
                
            #     # Amenities (boolean features)
            #     'has_elevator',
            #     'has_parking',
            #     'has_balcony',
            #     'has_storage',
            #     'has_security',
                
            #     # Additional features
            #     'furnishing',
            #     'additional_info',
            #     'utilities',
            #     'window_type',
            #     'energy_certificate',
                
            #     # Financial aspects
            #     'price_per_sqm',
            #     'maintenance_fee',
            #     'offer_type',
                
            #     # Temporal data
            #     'listing_year',
            #     'listing_month',
            #     'available_from'
            # ]

            # available_columns = [col for col in final_columns if col in combined_df.columns]
            # combined_df = combined_df[available_columns]

            self.logger.info(f"Final dataset has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns")

            self._save_combined_data(combined_df, base_dir)

            return combined_df
        else:
            self.logger.warning("No datasets were processed successfully.")
            return pd.DataFrame()

    def _load_processed_data(self, base_dir, dataset_name):
        # Determine the path based on dataset name
        data_path = get_dataset_path(base_dir, dataset_name, 'final', 'data.csv')

        try:
            df = pd.read_csv(data_path, sep=';', encoding='utf-8', low_memory=False)
            self.logger.info(f"Loaded {dataset_name} data with shape {df.shape}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading {dataset_name} data: {e}")
            return pd.DataFrame() 
        
    def _post_process(self, df, base_dir):
        # Apply post processing 
        df = add_engineered_features(df)

        # Save all distinct city names before processing
        self._save_distinct_cities(df, base_dir)

        # Add macroeconomic indicators
        df = self._add_macroeconomic_data(df, base_dir)

        df, validation_report = validate_dataset(df)

        for issue in validation_report:
            self.logger.warning(f"Validation issue: {issue['rule_name']} - {issue['issue_count']} issues found ({issue['percentage']}%)")

        # Example post-processing: Remove duplicates
        df.drop_duplicates(inplace=True)

        self.logger.info("Post-processing completed")
        return df

    def _save_combined_data(self, df, base_dir):
        output_file_path = get_dataset_path(base_dir, 'integrated_data', 'path', 'combined_data.csv')
        output_file_path_lodz = get_dataset_path(base_dir, 'integrated_data', 'path', 'combined_data_lodz.csv')

        df.to_csv(output_file_path, sep=';', encoding='utf-8', index=False)
        df_lodz = df[df['city'].str.lower().isin(['łódź', 'lodz'])]
        df_lodz.to_csv(output_file_path_lodz, sep=';', encoding='utf-8', index=False)
        self.logger.info(f"Combined data saved to {output_file_path}")

    def _add_macroeconomic_data(self, df, base_dir):
        """Add macroeconomic data based on city, year and month"""
        # Get complete city to voivodeship mapping from the dedicated module
        city_to_voivodeship = get_complete_city_mapping()
        
        # Add voivodeship column based on city
        df['voivodeship'] = df['city'].str.lower().map(city_to_voivodeship)
          # Log missing mappings
        missing_regions = df[df['voivodeship'].isna()]['city'].unique()
        if len(missing_regions) > 0:
            self.logger.warning(f"Could not map these cities to voivodeships ({len(missing_regions)} total):")
            # Print all missing cities for debugging
            for i, city in enumerate(missing_regions):
                self.logger.warning(f"  {i+1:3d}. '{city}'")
            # Use default region for missing mappings
            df['voivodeship'] = df['voivodeship'].fillna('POLSKA')
        
        # Convert month to quarter
        month_to_quarter = {
            1: '1 kwartał', 2: '1 kwartał', 3: '1 kwartał',
            4: '2 kwartał', 5: '2 kwartał', 6: '2 kwartał',
            7: '3 kwartał', 8: '3 kwartał', 9: '3 kwartał',
            10: '4 kwartał', 11: '4 kwartał', 12: '4 kwartał'
        }
        df['quarter'] = df['listing_month'].map(month_to_quarter)
          # Load macroeconomic data
        macro_path = os.path.join(base_dir, 'data', 'marcoeconomic_factors', 'final', 'czynniki_makroekonomiczne.csv')
        try:
            macro_df = pd.read_csv(macro_path, sep=';', encoding='utf-8')
            self.logger.info(f"Loaded macroeconomic data with shape {macro_df.shape}")
            
            # Only use original macroeconomic data (no estimated data for 2024-2025)
            # Properties from 2024-2025 will have null macroeconomic values
            self.logger.info(f"Using original macroeconomic data only. Shape: {macro_df.shape}")
            
        except Exception as e:
            self.logger.error(f"Error loading macroeconomic data: {e}")
            return df
        
        # Perform the merge
        result_df = pd.merge(
            df,
            macro_df,
            how='left',
            left_on=['voivodeship', 'listing_year', 'quarter'],
            right_on=['region', 'year', 'quarter']
        )
        
        # Remove redundant columns
        result_df.drop(['region', 'year'], axis=1, inplace=True, errors='ignore')
          # Log merge statistics
        matched_count = result_df[~result_df['primary_price'].isna()].shape[0]
        total_before_merge = len(df)
        
        self.logger.info(f"Merge statistics:")
        self.logger.info(f"  - Total properties before merge: {total_before_merge}")
        self.logger.info(f"  - Properties with macroeconomic data: {matched_count}")
        self.logger.info(f"  - Merge rate: {matched_count/total_before_merge*100:.1f}%")
        
        # Check for properties missing macroeconomic data
        missing_macro = result_df[result_df['primary_price'].isna()]
        if len(missing_macro) > 0:
            missing_years = missing_macro['listing_year'].value_counts()
            missing_regions = missing_macro['voivodeship'].value_counts()
            self.logger.info(f"Properties without macroeconomic data breakdown:")
            self.logger.info(f"  - By year: {dict(missing_years.head())}")
            self.logger.info(f"  - By region: {dict(missing_regions.head())}")
            self.logger.info(f"Note: Properties from 2024-2025 will not have macroeconomic data as it's not available yet")
        
        return result_df
    
    def _save_distinct_cities(self, df, base_dir):
        """Save all distinct city names to a file for manual mapping review."""
        if 'city' not in df.columns:
            self.logger.warning("No 'city' column found in data")
            return
        
        # Get all distinct city names (non-null)
        distinct_cities = df['city'].dropna().unique()
        distinct_cities = sorted([city for city in distinct_cities if city and str(city).strip()])
        
        # Save to file
        output_path = os.path.join(base_dir, 'data', 'integrated_data', 'distinct_cities.txt')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Distinct Cities Found ({len(distinct_cities)} total)\n")
            f.write("=" * 50 + "\n\n")
            for i, city in enumerate(distinct_cities, 1):
                f.write(f"{i:4d}. {city}\n")
        
        self.logger.info(f"Saved {len(distinct_cities)} distinct cities to {output_path}")
