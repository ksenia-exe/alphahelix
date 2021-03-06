training_labels_path = "/home/local/CORNELL/public/final_files/Training_Labels.txt"
testing_labels_path = "/home/local/CORNELL/public/final_files/Testing_Labels.txt"
expasy_aa_scales_path = "/home/local/CORNELL/public/final_files/Expasy_AA_Scales.txt"
training_labels_path_short = "Training_Labels_short.txt"

import pandas as pd
import numpy as np

import urllib.request
from joblib import dump, load

def select_columns(df, select):
    return df.loc[:,select]
# FUNCTION END

#Creates a triple of set X, set Y, and set X again but with UniProt column still included
#Features: blurring with a window of 9 for avg and max window values
def get_x_y(path, df = False):
    if df:
        train_df = path
    else:
        train_df = pd.read_csv(path, sep="\t")
    #reading in the file with labels and Expasy AA scales
    aa_df = pd.read_csv(expasy_aa_scales_path, sep="\t")
    aa_df = aa_df.rename(columns={"Amino Acid": "AA"})
    #Merging the df's on 'Amino Acid'
    train_df_m = pd.merge(train_df, aa_df, how='left', on=['AA'])
    #Keeping the Label for Y set
    train_y = pd.DataFrame(data=train_df_m["Label"], columns=["Label"])
    
    #Removing columns that include Position, Label, UniProt
    cols = list(train_df_m)[4:]
    #Feature blurring with a window of 9 based on average value of the window
    train_x_win_avg = train_df_m.groupby("UniProt")[cols].rolling(9, center=True, min_periods=1).mean()
    train_x_win_avg = train_x_win_avg.add_suffix('_avg')
    #Feature blurring with a window of 9 based on maximum value of the window
    train_x_win_max = train_df_m.groupby("UniProt")[cols].rolling(9, center=True, min_periods=1).max()
    train_x_win_max = train_x_win_max.add_suffix('_max')
    #Concatenating the two types of features
    train_x_win_avg=pd.concat([train_x_win_avg, train_x_win_max], axis=1)
    train_x = train_x_win_avg.reset_index().drop(["UniProt","level_1"], axis=1)
    uniprot_df = train_x_win_avg.reset_index().drop(["level_1"], axis=1)
#     min_max_scaler = preprocessing.MinMaxScaler()
#     train_x = pd.DataFrame(min_max_scaler.fit_transform(train_x), columns = train_x.columns)
#     uniprot_df = pd.DataFrame(min_max_scaler.fit_transform(uniprot_df), columns = train_x.columns[1:])
    return train_x,train_y,uniprot_df
# FUNCTION END

selected = ['beta_turn__Deleage_&_Roux_max','%_accessible_residues_avg','AA_composition_max','beta_sheet__Deleage_&_Roux_avg','AA_composition_avg','Refractivity_avg','Bulkiness_avg','beta_turn__Deleage_&_Roux_avg','Hphob__Wolfenden_et_al_avg','Coil__Deleage_&_Roux_avg','Ratio_hetero_endside_avg','Coil__Deleage_&_Roux_max','Hphob__Black_max','beta_sheet__Deleage_&_Roux_max','Hphob__Welling_&_al_avg','Average_flexibility_avg','Recognition_factors_avg','Relative_mutability_avg','beta_turn__Chou_&_Fasman_max','HPLC__retention_pH_74_avg']


# Get the amino acid sequence for the given UniProt
# Throws an exception if the ID is invalid
# Ex: retrieve_aa_seq('P30615') returns 'MSQLEHN.....RLIYLP'
def retrieve_aa_seq(UniProt):
    url='https://www.uniprot.org/uniprot/' + UniProt + '.fasta'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
    content = ''.join(content.split('\n')[1:])
    return content
# FUNCTION END

# Creates a df with UniProt, Position, AA, Label
# The label is a dummy label (-1) and is discarded
def create_x_df(aa_seq, uniprot):
    len_prot = len(aa_seq)
    position = list(range(1,len_prot+1))
    aa = list(aa_seq)
    uniprot_lst =  [uniprot for _ in range(len_prot)] 
    label =  [-1 for _ in range(len_prot)] 
    data = {'UniProt':uniprot_lst, 'Position':position, 'AA':aa, 'Label':label}
    return pd.DataFrame(data)
# FUNCTION END

# Create Function for obtianing features
def get_features(UniProt):
    # Get features saved from both the test and train sets
    features = pd.read_csv("../../final/features.csv")
    # If UniProt is in the original dataset, find the UniProt group and return the features
    if UniProt in features.UniProt.values:
        features_x = features.groupby("UniProt").get_group(UniProt).iloc[:,1:] #.drop(["level_1"], axis=1)
        return  select_columns(features_x,selected)
        #return features_x
    
    # If UniProt is not in the dataset, retrieve the AA sequence from uniprot.org
    aa_seq = retrieve_aa_seq(UniProt)
    # Calculate the features 
    features,_,_ = get_x_y(create_x_df(aa_seq, UniProt), df=True)
    return select_columns(features,selected)  
    #return features_x
# FUNCTION END

# Create Function for obtaining predicitons
def predict_uniprot(self, UniProt):
    # Get features
    X = self.get_features(UniProt)

    # Make / return predictions
    return self.predict(X)
# FUNCTION END

def predict_uniprot_proba(self, UniProt):
    # Get features
    X = self.get_features(UniProt)

    # Make / return prediction probabilities
    return self.predict_proba(X)
# FUNCTION END





























