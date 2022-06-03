from src.config import full_chem_feat_path, data_types_path, chemical_inventory_path, raw_data_path
import src.data.utils as data_utils 
from src.constants import GBL_INCHI_KEY, DMSO_INCHI_KEY, DMF_INCHI_KEY, INCHI_TO_CHEMNAME, RXN_FEAT_NAME, TARGET_COL, ORGANOAMONIUM_INCHI_KEY_COL
import pandas as pd
import json
import yaml as yl
import itertools

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

organoammonium_info = [
    'Chemical Name', 
    'Chemical Abbreviation', 
    'Molecular Weight (g/mol)',
    'Density            (g/mL)', 
    'InChI=',
    'InChI Key (ID)',
    'Chemical Category',
    'Canonical SMILES String',
    'Molecular Formula'
]


def read_data(data_path, solvent=GBL_INCHI_KEY, organic_key=False, 
              binary_cristal_score=True, filter_rxn_feat=True):
    """ To Read different type of data."""
    #with open(data_types_path) as json_file:

     #   dtypes = json.load(json_file)

    df = pd.read_csv(data_path, header=0, low_memory=False)

    data_utils.select_experiment_version(df)
    
    if solvent:
        df.query('_raw_reagent_0_chemicals_0_InChIKey == @solvent', inplace=True)
    else:
        df = df[df['_raw_reagent_0_chemicals_0_InChIKey'].isin([GBL_INCHI_KEY, DMSO_INCHI_KEY, DMF_INCHI_KEY])]
    
    df = df.fillna(0)

    chemical_info = read_chemical_info()

    chemical_info[['Chemical Abbreviation', 'InChI Key (ID)']].dropna()
    df = df.set_index('_rxn_organic-inchikey').join(chemical_info.set_index('InChI Key (ID)'), 
                                                    how='inner').reset_index().rename({'index': '_rxn_organic-inchikey'}, 
                                                    axis='columns')
    #selected_columns = rings_feat+columns_arbitrary_decision+continous_feat+rxn_feat+target+['Chemical Abbreviation']
     
    selected_columns = get_deafult_model_columns() + ["_rxn_organic-inchikey"]

    if not organic_key: 
        df.drop(["_rxn_organic-inchikey"], axis=1, inplace=True)
        selected_columns.remove("_rxn_organic-inchikey")
        
    df = df.query("_out_crystalscore > 0")
    
    if binary_cristal_score:
        df = binarization(df)
        
    return df[selected_columns]

def get_organoamines():
    df_amines_feats = pd.read_csv("data/metadata/type_var_fq_bins.csv")
    
    df = read_data(raw_data_path, organic_key=True, solvent=None)[[ORGANOAMONIUM_INCHI_KEY_COL]].drop_duplicates()
    chemical_info = read_chemical_info()

    chemical_info[['Chemical Abbreviation', 'InChI Key (ID)']].dropna()
    df = df.set_index(ORGANOAMONIUM_INCHI_KEY_COL).join(chemical_info.set_index('InChI Key (ID)'), 
                                                    how='inner').reset_index().rename({'index': ORGANOAMONIUM_INCHI_KEY_COL}, 
                                                    axis='columns')
    return df
    

def read_multisolvent_data():
    
    solvents_inchies = [GBL_INCHI_KEY, DMSO_INCHI_KEY, DMF_INCHI_KEY]
    solvents = [INCHI_TO_CHEMNAME[inchie] for inchie in solvents_inchies]

    plot_solvents = {'Gamma-Butyrolactone': "GBL",
                     'Dimethyl sulfoxide':"DMSO",
                     'Dimethylformamide': "DMF"}

    solvents_data = {INCHI_TO_CHEMNAME[solvent_inchie]: utils.read_data(raw_data_path, organic_key=True,\
                                                                        solvent=solvent_inchie) \
                     for solvent_inchie in solvents_inchies}
    
    def add_column(df, solvent):
        df['solvent'] = solvent
        return df

    df_full_with_solvent = pd.concat([data.apply(add_column, axis=1, args=(solvent,)) \
                                 for solvent, data in solvents_data.items()], axis=0)\
                                .reset_index(drop=True)
    return df_full_with_solvent


def binarization(df, soft=False, col=TARGET_COL):
    if soft:
        df.loc[:,col] = (df[TARGET_COL] > 2).astype(int)
    else:
        df.loc[:,col] = (df[TARGET_COL] == 4).astype(int)
    return df


def read_chemical_info(filtered_cols=True):
    """Read information about chemical compounds used as organoammonium."""
    with open(chemical_inventory_path) as file:
        chemical_inventory = pd.read_csv(file, header=0)
        if filtered_cols:
            chemical_inventory = chemical_inventory[organoammonium_info]
        chemical_inventory = chemical_inventory.drop_duplicates().dropna()
        return chemical_inventory


def filter_columns_by_prefix(columns, prefixes):
    """Filter columns by prefix."""
    filtered_columns = {column for column in columns 
                        if True in (column.startswith(prefix) 
                        for prefix in prefixes)}
    return filtered_columns

def get_columns(total_columns, as_list=True):
    """Get all used columns: Reaction condition and physicochemical features."""
    prefixs = ['_rxn_', '_feat_']
    columns_by_prefix = {}
    for prefix in prefixs:
        columns_by_prefix[prefix] = set(filter(lambda column_name: 
                                        column_name.startswith(prefix), 
                                        total_columns))
    key_list = [list(key_val) for key_val in columns_by_prefix.values()]
    columns_list = list(itertools.chain(*key_list))

    return columns_list if as_list else columns_by_prefix


def concentration_feats():
    return list(RXN_FEAT_NAME.keys())  

def chem_feats():
    with open(full_chem_feat_path, 'r') as file:
        data = json.load(file)
        feat_ls = json.loads(data)
    return feat_ls
    
def get_deafult_model_columns():
    concentration_cols = concentration_feats()
    feats_cols = chem_feats()
    return feats_cols + concentration_cols +[TARGET_COL]
