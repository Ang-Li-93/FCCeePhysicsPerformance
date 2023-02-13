import numbers
from re import I
import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
#from root_pandas import read_root
import uproot
import ROOT
import joblib
import glob
import seaborn as sns

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
#from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

#def run(vars):
def run():
    
    modes = ["mumuH","ZZ","WWmumu","Zll","eeZ"]
    vars_list = train_vars
    print("TRAINING VARS")
    print(vars_list)
    path = f"{loc.PKL}"
    #df0 = pd.read_pickle(f"{path}/BDT_0.pkl")
    #df1 = pd.read_pickle(f"{path}/BDT_1.pkl")
    df = pd.read_pickle(f"{path}/preprocessed.pkl")
    print(f"__________________________________________________________")
    print(f"Input number of events:")
    for cur_mode in modes:
      print(f"Number of training {cur_mode}: {int(len(df[(df['sample'] == cur_mode) & (df['test'] == False)]))}")
      print(f"Number of testing {cur_mode}: {int(len(df[(df['sample'] == cur_mode) & (df['test'] == True)]))}")
    print(f"__________________________________________________________")
   
    X_train = df.loc[df['test'] == False, vars_list]
    y_train = df.loc[df['test'] == False, ['isSignal']]
    X_test  = df.loc[df['test'] == True, vars_list]
    y_test  = df.loc[df['test'] == True, ['isSignal']]

    X_train =  X_train.to_numpy()   
    y_train =  y_train.to_numpy() 
    X_test  =  X_test.to_numpy() 
    y_test  =  y_test.to_numpy() 
    
    #BDT
    config_dict = {
            "n_estimators"      : 350,
            "learning_rate"     : 0.20,
            "max_depth"         : 3,
            'subsample'         : 0.5,
            'gamma'             : 3,
            'min_child_weight'  : 10,
            'max_delta_step'    : 0,
            'colsample_bytree'  : 0.5,
            }
    early_stopping_round = 25
    
    # Training
    bdt = xgb.XGBClassifier(n_estimators    =config_dict["n_estimators"],
                            max_depth       =config_dict["max_depth"],
                            learning_rate   =config_dict["learning_rate"],
                            subsample       =config_dict["subsample"],
                            gamma           =config_dict["gamma"],
                            min_child_weight=config_dict["min_child_weight"], 
                            max_delta_step  =config_dict["max_delta_step"],
                            colsample_bytree=config_dict["colsample_bytree"],
                            #feature_names=vars_list,
                            )

    eval_set = [(X_train, y_train), (X_test, y_test)]
    
    #Fit the model
    print("Training model")
    bdt.fit(X_train, y_train, eval_metric=["error", "logloss", "auc"], eval_set=eval_set, early_stopping_rounds=early_stopping_round, verbose=True)
    best_iteration = bdt.best_iteration + 1 
    #if best_iteration < config_dict["n_estimators"]:
    if True:
              print("early stopping after {0} boosting rounds".format(best_iteration))
              print("")
    feature_importances = pd.DataFrame(bdt.feature_importances_,
                                        index = vars_list,
                                       columns=['importance']).sort_values('importance',ascending=False)

    #Write the model to a ROOT file on EOS, for application elsewhere in FCCAnalyses
    out = f"{loc.BDT}"
    print("--->Writing xgboost model:")
    ut.create_dir(out)
    print(f"------>Saving {out}/xgb_bdt.root")
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, "ZH_Recoil_BDT", f"{out}/xgb_bdt.root", num_inputs=len(vars_list))
    
    #Write model to joblib file
    print(f"------>Saving {out}/xgb_bdt.joblib")
    joblib.dump(bdt, f"{out}/xgb_bdt.joblib")

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Train xgb model for ZH recoil study')
    #parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    #args = parser.parse_args()

    #run(args.Vars)
    run()
