from src.config import training_dataset_path, data_types_path, chemical_inventory_path, raw_data_path
import src.data.utils as data_utils 
import pandas as pd
import json
import yaml as yl


rings_feat = ['_feat_CyclomaticNumber',
 '_feat_CarboaromaticRingCount',
 '_feat_CarboRingCount',
 '_feat_LargestRingSize',
 '_feat_RingAtomCount',
 '_feat_SmallestRingSize',
 '_feat_AromaticRingCount',
 '_feat_AromaticAtomCount']

 
columns_arbitrary_decision = ["_feat_BalabanIndex", "_feat_VanderWaalsSurfaceArea", "_feat_VanderWaalsVolume", "_feat_ASA", "_feat_WienerIndex", "_feat_maximalprojectionsize"]
continous_feat = ['_feat_molsurfaceareaVDWp', '_feat_maximalprojectionsize', '_feat_MinimalProjectionArea', '_feat_minimalprojectionsize', '_feat_MaximalProjectionArea', '_feat_MolPol', '_feat_ASA_P', '_feat_msareaVDWp', '_feat_ASA', '_feat_ASA-', '_feat_MinimalProjectionRadius', '_feat_molsurfaceareaASAp', '_feat_LengthPerpendicularToTheMinArea', '_feat_WienerIndex', '_feat_ASA+', '_feat_MaximalProjectionRadius', '_feat_VanderWaalsSurfaceArea', '_feat_LengthPerpendicularToTheMaxArea', '_feat_VanderWaalsVolume', '_feat_BalabanIndex', '_feat_ASA_H', '_feat_HyperWienerIndex', '_feat_msareaASAp', '_feat_Refractivity', '_feat_AvgPol']
rxn_feat = ["_rxn_M_acid", "_rxn_M_organic", "_rxn_M_inorganic"] 
target = ["_out_crystalscore"]


def read_data(data_path=training_dataset_path, organic_key=False):
    """To Read different type of data."""
    with open(data_types_path) as json_file:

        dtypes = json.load(json_file)

        df = pd.read_csv(data_path, header=0, dtype=dtypes)

        if(data_path == raw_data_path):
            data_utils.select_experiment_version_and_used_solvent(df)

        df = df.fillna(0)

        chemical_info = read_chemical_info()

        chemical_info[['Chemical Abbreviation', 'InChI Key (ID)']].dropna()
        df = df.set_index('_rxn_organic-inchikey').join(chemical_info.set_index('InChI Key (ID)'), 
                                                        how='inner').reset_index().rename({'index': '_rxn_organic-inchikey'}, 
                                                        axis='columns')
        selected_columns = rings_feat+columns_arbitrary_decision+continous_feat+rxn_feat+target+['Chemical Abbreviation']
        if(organic_key): 
            selected_columns += ["_rxn_organic-inchikey"]
        df = df[set(selected_columns)]
        df['_out_crystalscore'] = (df['_out_crystalscore'] == 4).astype(int)
        
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

