REQUIRED_COLUMNS = [
    'price', 'area_sqm', 'rooms', 'city', 'listing_year', 'listing_month'
]

OPTIONAL_COLUMNS = [
    'address', 'latitude', 'longitude', 'floor', 'property_type',
    'condition', 'has_parking', 'has_balcony', 'price_per_sqm', 'source_dataset'
]

DATASET_CONFIG = {
    'apartment_prices': {
        'raw': 'data\\apartment_prices\\raw',
        'processed': 'data\\apartment_prices\\processed',
        'final': 'data\\apartment_prices\\final',
        'file_name': 'data.csv',
    },
    'house_prices': {
        'raw': 'data\\house_prices\\raw',
        'processed': 'data\\house_prices\\processed',
        'final': 'data\\house_prices\\final',
        'file_name': 'data.csv',
    },
    'flat_prices': {
        'raw': 'data\\flat_prices\\raw',
        'processed': 'data\\flat_prices\\processed',
        'final': 'data\\flat_prices\\final',
        'file_name': 'data.csv',
    },
    'olx_house_prices': {
        'raw': 'data\\olx_house_prices\\raw',
        'processed': 'data\\olx_house_prices\\processed',
        'final': 'data\\olx_house_prices\\final',
        'file_name': 'data.csv',
    },
    'warsaw_flat_prices': {
        'raw': 'data\\warsaw_flat_prices\\raw',
        'processed': 'data\\warsaw_flat_prices\\processed',
        'final': 'data\\warsaw_flat_prices\\final',
        'file_name': 'data.csv',
    },
    'numbers_apartment_prices': {
        'raw': 'data\\numbers_apartment_prices\\raw',
        'processed': 'data\\numbers_apartment_prices\\processed',
        'final': 'data\\numbers_apartment_prices\\final',
        'file_name': 'data.csv',
    },
    'otodom_current_prices': {
        'raw': 'data\\otodom_current_prices\\raw',
        'processed': 'data\\otodom_current_prices\\processed',
        'final': 'data\\otodom_current_prices\\final',
        'file_name': 'data.csv',
    },
    'allegro_prices': {
        'raw': 'data\\allegro_prices\\raw',
        'processed': 'data\\allegro_prices\\processed',
        'final': 'data\\allegro_prices\\final',
        'file_name': 'data.csv',
    },
    'integrated_data': {
        'path': 'data\\integrated_data',
        'file_name': 'combined_data.csv',
    }
}