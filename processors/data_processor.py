from abc import ABC, abstractmethod
import logging

class DataProcessor(ABC):
    """Base class for all data processors using template method pattern."""

    def __init__(self, name):
        self.name = name
        self.logger = self.__setup_logger()
    
    def __setup_logger(self):
        logger = logging.getLogger(f"{self.name}_processor")
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def process(self, base_dir):
        """Template methot defining the processing workflow"""
        self.logger.info(f"Starting processing for {self.name}")

        try:
            # Step 1: Identify input/output paths
            input_path, output_path = self._get_paths(base_dir)
            self.logger.info(f"Input path: {input_path}")
            self.logger.info(f"Output path: {output_path}")

            # Step 2: Read data
            df = self._read_data(input_path)
            self.logger.info(f"Data read with shape: {df.shape}")

            # Step 3: Clean data
            df = self._clean_data(df)
            self.logger.info(f"Data cleaned with shape: {df.shape}")

            # Step 4: Transform data
            df = self._transform_data(df)
            self.logger.info(f"Data transformed with columns: {df.columns.tolist()}")

            # Step 5: Save data
            self._save_data(df, output_path)
            self.logger.info(f"Data saved to {output_path}")

            return df
        
        except Exception as e:
            self.logger.error(f"Error processing {self.name}: {e}")
            raise e

    @abstractmethod
    def _get_paths(self, base_dir):
        """Define input/output paths"""
        pass
    @abstractmethod
    def _read_data(self, input_path):
        """Read data from input path"""
        pass

    @abstractmethod
    def _clean_data(self, df):
        """Clean the data"""
        pass

    @abstractmethod
    def _transform_data(self, df):
        """Transform the data"""
        pass

    @abstractmethod
    def _save_data(self, df, output_path):
        """Save the data to output path"""
        pass