import ROOT
import sys, os, argparse
import uproot
import awkward as ak
import json
import numpy as np
import matplotlib.pyplot as plt
from particle import literals as lp
import pandas as pd
import glob
from sklearn.model_selection import train_test_split
#Local code
#from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut
from config.common_defaults import deffccdicts

def run(modes, n_folds, stage):
  #xsec, from http://fcc-physics-events.web.cern.ch/fcc-physics-events/Delphesevents_spring2021_IDEA.php
  xsec = {}
  xsec["mumuH"]   = 0.0067643
  xsec["WWmumu"]  = 0.25792
  xsec["ZZ"]      = 1.35899
  xsec["Zll"]     = 5.288
  xsec["eeZ"]     = 0.10368
  xsec["gaga_mumu"] = 1.5523  
  sig = "mumuH"

  if (stage=="training"):
    data_path=loc.TRAIN
    pkl_path=loc.PKL
  elif (stage=="validation"):
    data_path=loc.ANALYSIS
    pkl_path=loc.PKL_Val
  else:
    print("Stage doesn't exist")
    exit(0)
  print(data_path)
  files = {}
  df = {}
  N_events = {}
  eff = {}
  N_BDT_inputs = {}
  vars_list = train_vars.copy()
  df0 = {}
  df1 = {} 
  frac = {}
  frac["mumuH"]  = 1.0
  frac["WWmumu"] = 1.0
  frac["ZZ"]     = 1.0
  frac["Zll"]    = 1.0
  frac["eeZ"]    = 1.0
  frac["gaga_mumu"] = 1.0
  print(f"--->Working on variables: {vars_list}")
  for cur_mode in modes:
    print(f"--->Working on {cur_mode}")
    
    if (cur_mode=="eeZ"):
      path_egamma = f"{data_path}/{mode_names['egamma']}"
      path_gammae = f"{data_path}/{mode_names['gammae']}"
      files[cur_mode] = glob.glob(f"{path_egamma}/*.root") + glob.glob(f"{path_gammae}/*.root")
    else:
      path = f"{data_path}/{mode_names[cur_mode]}"  
      files[cur_mode] = glob.glob(f"{path}/*.root")
   
    N_events[cur_mode] = sum([uproot.open(f)["eventsProcessed"].value for f in files[cur_mode]])
    print(f"------>Produced {N_events[cur_mode]} of {cur_mode} MC samples")
    df[cur_mode] = pd.concat((ut.get_df(f, vars_list) for f in files[cur_mode]), ignore_index=True)
    print(f"------>After selection: {len(df[cur_mode])} {cur_mode} MC samples")
    eff[cur_mode] = len(df[cur_mode])/N_events[cur_mode]
    print(f"------>Cut Efficiency: {eff[cur_mode]*100} %")
    df[cur_mode]['sample'] = cur_mode
    df[cur_mode]['isSignal'] = (1 if(cur_mode == sig) else 0)
    print(cur_mode)
  #set the BDT input numbers of each process
  xsec_tot_bkg = eff["ZZ"]*xsec["ZZ"] + eff["WWmumu"]*xsec["WWmumu"] + eff["Zll"]*xsec["Zll"] + eff["eeZ"]*xsec["eeZ"] + eff["gaga_mumu"]*xsec["gaga_mumu"]
  for cur_mode in modes:
    N_BDT_inputs[cur_mode] = (int(frac[cur_mode]*len(df[cur_mode])) if cur_mode == sig else int(frac[cur_mode]*len(df[sig])*(eff[cur_mode]*xsec[cur_mode]/xsec_tot_bkg)))
    print(f"--------->BDT inputs of {cur_mode}: {N_BDT_inputs[cur_mode]}")
    print(f"--------->Total number of {cur_mode}: {len(df[cur_mode])}")
    if (N_BDT_inputs[cur_mode]-len(df[cur_mode]) > 0):
      print(f"--------->(Total number - BDT inputs) of {cur_mode}: {len(df[cur_mode]) - N_BDT_inputs[cur_mode]}")
      print(f"--------->{cur_mode} needs {(N_BDT_inputs[cur_mode]-len(df[cur_mode]))/eff[cur_mode]} more events before selection")
      exit(1)
    #df_train[cur_mode], df_test[cur_mode] = train_test_split(df[cur_mode], test_size=0.5, random_state=7)
    df[cur_mode] = df[cur_mode].sample(n = N_BDT_inputs[cur_mode], random_state=1)
    df0[cur_mode], df1[cur_mode] = train_test_split(df[cur_mode], test_size=0.5, random_state=7)
    df[cur_mode].loc[df0[cur_mode].index, "test"] = False
    df[cur_mode].loc[df1[cur_mode].index, "test"] = True
    df[cur_mode].loc[df[cur_mode].index, "norm_weight"] = xsec[cur_mode]/N_events[cur_mode] 
  
  dfsum = pd.concat([df[cur_mode] for cur_mode in modes])
  #df1sum = pd.concat([df1[cur_mode] for cur_mode in modes])
    
  #Save to pickle
  print("Writing output to pickle file")
  ut.create_dir(pkl_path)
  print(f"--->Preprocessed saved {pkl_path}/preprocessed.pkl")
  dfsum.to_pickle(f"{pkl_path}/preprocessed.pkl")
  #df0sum.to_pickle(f"{pkl_path}/BDT_0.pkl")
  #df1sum.to_pickle(f"{pkl_path}/BDT_1.pkl")

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process mumuH, WWmumu, ZZ, Zll,eeZ MC to make reduced files for xgboost training')
  parser.add_argument("--Mode", action = "store", dest = "modes", default = ["mumuH","ZZ","WWmumu","Zll","eeZ","gaga_mumu"], help="Decay cur_mode")
  parser.add_argument("--Folds", action = "store", dest = "n_folds", default = 2, help="Number of Folds")
  parser.add_argument("--Stage", action = "store", dest = "stage", default = "training", choices=["training","validation"], help="training or validation")
  args = vars(parser.parse_args())

  run(**args)

