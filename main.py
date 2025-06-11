import os
import logging
from processors.apartment_prices import ApartmentPricesProcessor
from processors.house_prices import HousePricesProcessor
from processors.flat_prices import FlatPricesProcessor
from processors.olx_house_prices import OlxHousePricesProcessor
from processors.otodom_current_prices import OtodomCurrentPrices
from processors.allegro_prices import AllegroPrices
from integration.integrator import DatasetIntegrator
from config.column_mappings import COLUMN_MAPPINGS

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('processing.log'),
            logging.StreamHandler()
        ]
    )
def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the data processing pipeline")

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Phase 1: Process individual datasets
    logger.info("Phase 1: Processing individual datasets")

    processors = [
        ApartmentPricesProcessor(),
        HousePricesProcessor(),
        FlatPricesProcessor(),
        OlxHousePricesProcessor(),
        OtodomCurrentPrices(),
        AllegroPrices(),
    ]

    for processor in processors:
        try:
            logger.info(f"Processing data with {processor.name}")
            processor.process(base_dir)
        except Exception as e:
            logger.error(f"Error processing {processor.name}: {e}")
            continue
    
    # Phase 2: Integrate datasets
    logger.info("Phase 2: Integrating datasets")
    try:
        integrator = DatasetIntegrator(COLUMN_MAPPINGS)
        combined_df = integrator.integrate_datasets(base_dir)
        logger.info(f"Integration complete. Combined dataset has {combined_df.shape[0]} rows and {combined_df.shape[1]} columns")
    except Exception as e:
        logger.error(f"Error during dataset integration: {e}")

    logger.info("Data processing pipeline completed")
        
if __name__ == "__main__":
    main()

