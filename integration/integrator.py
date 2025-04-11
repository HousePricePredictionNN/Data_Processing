import logging
import pandas as pd
from utils.standardization import standardize_dataframe, ensure_standard_columns, standardize_data_types
from config.config import REQUIRED_COLUMNS, OPTIONAL_COLUMNS
from utils.path_utils import get_dataset_path
from utils.feature_engineering import add_engineered_features
from utils.validation import validate_dataset

class DatasetIntegrator:
    def __init__(self, column_mappings):
        self.column_mappings = column_mappings
        self.logger = logging.getLogger(__name__)

    def integrate_datasets(self, base_dir):
        self.logger.info("Starting dataset ingeration")

        processed_dfs = {}

        for dataset_name in self.column_mappings.keys():
            try:
                df = self._load_processed_data(base_dir, dataset_name)

                if df.empty:
                    self.logger.warning(f"No data found for {dataset_name}. Skipping integration.")
                    continue
                
                # Transofrm data to standard schema
                standardized_df = standardize_dataframe(df, dataset_name, self.column_mappings)

                # Ensure all required columns exist
                standardized_df = ensure_standard_columns(standardized_df, REQUIRED_COLUMNS, OPTIONAL_COLUMNS)

                # Standardize data types
                standardized_df = standardize_data_types(standardized_df)

                # Store in directory
                processed_dfs[dataset_name] = standardized_df
                self.logger.info(f"Successfully processed {dataset_name} with {len(standardized_df)} ")
            except Exception as e:
                self.logger.error(f"Error processing {dataset_name}: {e}")
                continue

        if processed_dfs:
            combined_df = pd.concat(processed_dfs.values(), ignore_index=True)
            self.logger.info(f"Combined dataset has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns")

            # Apply post processing
            combined_df = self._post_process(combined_df)

            final_columns = [
                # Core identification and source
                'source_url',
                
                # Basic property details
                'price',
                'area_sqm',
                'rooms',
                'property_type',
                
                # Location information
                'address',
                'city',
                'district',
                'voivodeship',
                'latitude',
                'longitude',
                'distance_to_center',
                'city_population',
                
                # Property characteristics
                'floor',
                'floor_count',
                'build_year',
                'condition',
                'market_type',
                'building_type',
                'building_material',
                'heating_type',
                'ownership_type',
                
                # Amenities (boolean features)
                'has_elevator',
                'has_parking',
                'has_balcony',
                'has_storage',
                'has_security',
                
                # Additional features
                'furnishing',
                'additional_info',
                'utilities',
                'window_type',
                'energy_certificate',
                
                # Financial aspects
                'price_per_sqm',
                'maintenance_fee',
                'offer_type',
                
                # Temporal data
                'listing_year',
                'listing_month',
                'available_from'
            ]

            available_columns = [col for col in final_columns if col in combined_df.columns]
            combined_df = combined_df[available_columns]

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
        
    def _post_process(self, df):
        # Apply post processing 
        df = add_engineered_features(df)

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
    