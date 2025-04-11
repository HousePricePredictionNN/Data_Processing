import os
from config.config import DATASET_CONFIG

# Path utility funciton
def get_dataset_path(base_dir, dataset_name, path_type='final', file_name=None):
    """
    Get the path for a specific dataset and path type.
    :param base_dir: Base directory of the project.
    :param dataset_name: Name of the dataset.
    :param path_type: Type of path ('raw', 'processed', 'final').
    :param file_name: Optional file name to append to the path.
    :return: Full path to the dataset.
    """
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(f"Dataset {dataset_name} not found in configuration.")
    
    dataset_config = DATASET_CONFIG[dataset_name]

    if path_type not in dataset_config:
        raise ValueError(f"Path type {path_type} not found for dataset {dataset_name}.")
    
    dir_path = os.path.join(base_dir, dataset_config[path_type])

    os.makedirs(dir_path, exist_ok=True)

    if file_name:
        return os.path.join(dir_path, file_name)
    
    return dir_path