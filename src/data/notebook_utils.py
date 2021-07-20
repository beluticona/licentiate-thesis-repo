from src.config import training_dataset_path, data_types_path, chemical_inventory_path
import src.data.utils as data_utils 
import pandas as pd
import json
import yaml as yl


def read_data(data_path=training_dataset_path):
    with open(data_types_path) as json_file:

        dtypes = json.load(json_file)
        
        df = pd.read_csv(data_path, header=0, dtype=dtypes)

        if(data_path != training_dataset_path):
            data_utils.select_experiment_version_and_used_solvent(df)

        df = df.fillna(0)

        return df


def read_chemical_info():
    """Read information about chemical compounds used as organoammonium."""
    with open(chemical_inventory_path) as file:
        chemical_inventory = pd.read_csv(file, header=0)
        return chemical_inventory


def filter_columns_by_prefix(columns, prefixes):
    """Filter columns by prefix."""
    filtered_columns = {column for column in columns 
                        if True in (column.startswith(prefix) 
                        for prefix in prefixes)}
    return filtered_columns


def get_columns(total_columns):
    """Get all used columns: Reaction condition and physicochemical features."""
    prefixs = ['_rxn_', '_feat_']
    columns_by_prefix = {}
    for prefix in prefixs:
        columns_by_prefix[prefix] = set(filter(lambda column_name: 
                                        column_name.startswith(prefix), 
                                        total_columns))
    return columns_by_prefix

