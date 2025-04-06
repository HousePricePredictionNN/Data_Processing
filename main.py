import os
import logging
from processors.apartment_prices import ApartmentPricesProcessor
from processors.house_prices import HousePricesProcessor
from processors.flat_prices import FlatPricesProcessor
from processors.olx_house_prices import OlxHousePricesProcessor
from processors.warsaw_flat_prices import WarsawFlatPrices

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

    processors = [
        ApartmentPricesProcessor(),
        HousePricesProcessor(),
        FlatPricesProcessor(),
        OlxHousePricesProcessor(),
        WarsawFlatPrices(),
    ]

    for processor in processors:
        try:
            logger.info(f"Processing data with {processor.name}")
            processor.process(base_dir)
        except Exception as e:
            logger.error(f"Error processing {processor.name}: {e}")
            continue
    
    logger.info("Data processing pipeline completed")

if __name__ == "__main__":
    main()

