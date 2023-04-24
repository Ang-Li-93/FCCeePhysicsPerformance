import numbers
from re import I
import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
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
from tqdm import tqdm

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
#from userConfig import loc, mode, train_vars, train_vars_vtx, mode_names
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

def run():

    modes = ["mumuH","ZZ","WWmumu","Zll","eeZ","gaga_mumu"]
    vars_list = train_vars
    print("TRAINING VARS")
    print(vars_list)
    path = f"{loc.PKL}"
    df = pd.read_pickle(f"{path}/preprocessed.pkl")
    print(f"__________________________________________________________")
    print(f"Input number of events:")
    for cur_mode in modes:
      print(f"Number of training {cur_mode}: {int(len(df[(df['sample'] == cur_mode) & (df['test'] == False)]))}")
      print(f"Number of testing {cur_mode}: {int(len(df[(df['sample'] == cur_mode) & (df['test'] == True)]))}")
    print(f"__________________________________________________________")
    
    X = df[vars_list]
    y = df['isSignal']
    #X_test  = df.loc[df['test'] == True, vars_list]
    #y_test  = df.loc[df['test'] == True, ['isSignal']]
    
    # Load trained model
    print(f"--->Loading BDT model {loc.BDT}/xgb_bdt.joblib")
    bdt = joblib.load(f"{loc.BDT}/xgb_bdt.joblib")
    # Add new column for the BDT output
    print(f"--->Evaluating BDT model")
    df["BDTscore"] = bdt.predict_proba(X).tolist()
    df["BDTscore"] = df["BDTscore"].apply(lambda x: x[1])
    
    # retrieve performance metrics
    print("------>Retrieving performance metrics")
    results = bdt.evals_result()
    epochs = len(results['validation_0']['error'])
    x_axis = range(0, epochs)
    best_iteration = bdt.best_iteration + 1

    ut.create_dir(f"{loc.PLOTS}")
    # plot log loss
    print("------>Plotting log loss")
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['logloss'], label='Train')
    ax.plot(x_axis, results['validation_1']['logloss'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('Log Loss')
    plt.title('XGBoost Log Loss')
    print(f"------>Saving {loc.PLOTS}/logloss.pdf")
    fig.savefig(f"{loc.PLOTS}/logloss.pdf")
    
    # plot classification error
    print("------>Plotting classification error")
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['error'], label='Train')
    ax.plot(x_axis, results['validation_1']['error'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('Classification Error')
    plt.title('XGBoost Classification Error')
    print(f"------>Saving {loc.PLOTS}/error.pdf")
    fig.savefig(f"{loc.PLOTS}/error.pdf")

    # plot auc
    print("------>Plotting auc")
    fig, ax = plt.subplots()
    ax.plot(x_axis, results['validation_0']['auc'], label='Train')
    ax.plot(x_axis, results['validation_1']['auc'], label='Test')
    plt.axvline(best_iteration, color="gray", label="Optimal tree number")
    ax.legend()
    plt.xlabel("Number of trees")
    plt.ylabel('auc')
    plt.title('XGBoost auc')
    print(f"------>Saving {loc.PLOTS}/auc.pdf")
    fig.savefig(f"{loc.PLOTS}/auc.pdf")

    # plot ROC 1
    print("------>Plotting ROC")
    fig, axes = plt.subplots(1, 1, figsize=(5,5))
    #df_train = df_tot.query('test==False')
    #df_valid =  df_tot.query("test==True")
    eps=0.
    ax=axes
    ax.set_xlabel("$\epsilon_B$")
    ax.set_ylabel("$\epsilon_S$")
    ut.plot_roc_curve(df[df['test']==True],  "BDTscore", ax=ax, label="test sample", tpr_threshold=eps)
    ut.plot_roc_curve(df[df['test']==False], "BDTscore", ax=ax, color="#ff7f02", tpr_threshold=eps,linestyle='--', label="train sample")
    plt.plot([eps, 1], [eps, 1], color='navy', lw=2, linestyle='--')
    ax.set_title('ROC')
    ax.legend()
    fig.savefig(f"{loc.PLOTS}/ROC1.pdf")
    print(f"------>Saved {loc.PLOTS}/ROC1.pdf")
    
    #plot score with trained, test, signal, backgrounds
    print("------>Plotting BDT score (overtraining check)")
    fig, axes = plt.subplots(1, 1, figsize=(5,5))
    Bins = 20
    htype="step"
    #plt.figure()
    tag=['signal_train', 'signal_test', 'bkg_train', 'bkg_test']
    line=['solid', 'dashed', 'solid', 'dashed']
    color=['red', 'red', 'blue', 'blue']
    cut=['test==False & isSignal==1', 'test==True & isSignal==1', 'test==False & isSignal!=1', 'test==True & isSignal!=1']
    for (x,y,z,w) in zip(tag, line, color, cut):
        df_instance = df.query(w)
        print('--------->', x, len(df_instance), "Ratio: %.2f%%" % ((len(df_instance)/float(len(df)))* 100.0))
        # better to recover the negative weights when evaluating the performance
        #print(df_instance['score'])
        #print(df_instance.index) 
        plt.hist(df_instance['BDTscore'], density=True, bins=Bins, range=[0.0, 1.0], histtype=htype, label=x, linestyle=y, color=z)
    ax = axes
    plt.yscale('log')
    ax.legend(loc=2, ncol=2)
    fig.savefig(f"{loc.PLOTS}/SB.pdf")
    print(f"------>Saved {loc.PLOTS}/SB.pdf")

    ## visualize the three
    #plt.figure(figsize = (50,200))
    #ax = plt.subplot(111) 
    #xgb.plot_tree(bdt,num_trees=1,ax=ax,rankdir='LR')
    #plt.savefig(f"{loc.PLOTS}/Tree_{vars}.pdf")

    # plot importance
    print("------>Plotting inportance")
    #plt.figure(figsize = (30,30))
    #ax = plt.subplot(111)
    fig, ax = plt.subplots(figsize=(12, 6))
    xgb.plot_importance(bdt,ax=ax)
    #xgb.plot_importance(bdt).set_yticklabels(vars_list)
    plt.savefig(f"{loc.PLOTS}/Importance.pdf")
    print(f"------>Saved {loc.PLOTS}/Importance.pdf")

   
    print("------>Plotting Significance scan")
    #compute the significance
    df_Z = ut.Significance(df[(df['isSignal'] == 1) & (df['test'] == True)], df[(df['isSignal'] == 0) & (df['test'] == True)], score_column = 'BDTscore', func=ut.Z, nbins=100)
    max_index=df_Z["Z"].idxmax()
    print('max-Z: {:.2f}'.format(df_Z.loc[max_index,"Z"]), 'cut threshold: [', max_index, ']')
    fig, ax = plt.subplots(figsize=(12,8))
    plt.scatter(df_Z.index, df_Z["Z"])
    ax.scatter(x=max_index, y=df_Z.loc[max_index,"Z"], c='r', marker="*")
    plt.xlabel("BDT Score ")
    plt.ylabel("Significance")
    txt1 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    txt2 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
    plt.legend([txt1, txt2], ('max-Z: {:.2f} cut threshold: [{:.2f}]'.format(df_Z.loc[max_index,"Z"],max_index), "$Z = S/\\sqrt{S+B}$"))
    fig.savefig(f"{loc.PLOTS}/Significance_Z_scan.pdf")
    print(f"------>Saved {loc.PLOTS}/Significance_Z_scan.pdf")  
   

    #Plot efficiency as a function of BDT cut in each sample
    print("------>Plotting Efficiency")
    BDT_cuts = np.linspace(0,99,99)
    cut_vals = []
    eff = {}

    for cur_mode in modes:
      eff[cur_mode] = []

    for x in tqdm(BDT_cuts):
      cut_val = float(x)/100
      cut_vals.append(cut_val)
      for cur_mode in modes:
        eff[cur_mode].append(float(len(df[(df['sample'] == cur_mode) & (df['test'] == True) & (df['BDTscore'] > cut_val)]))/float(len(df[(df['sample'] == cur_mode) & (df['test'] == True)])))
    
    fig, ax = plt.subplots(figsize=(12,8))
    
    for cur_mode in modes:
      plt.plot(cut_vals, eff[cur_mode], label=cur_mode)
         
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(0,1)
    plt.xlabel("BDT score",fontsize=30)
    plt.ylabel("Efficiency",fontsize=30)
    #plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,1.3)
    plt.legend(fontsize=20, loc="best")
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/BDT_eff_nolog.pdf")
    print(f"------>Saved {loc.PLOTS}/BDT_eff_nolog.pdf") 
    
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

def main():
    parser = argparse.ArgumentParser(description='Train xgb model for ZH recoil study')
    #parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    #args = parser.parse_args()

    run()

if __name__ == '__main__':
    main()
