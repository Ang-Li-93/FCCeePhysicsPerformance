#!/bin/bash
cd /afs/cern.ch/work/l/lia/private/FCC/MVA_Final/FCCAnalyses
source setup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/MVA_Final/FCCeePhysicsPerformance/case-studies/higgs/dataframe
source localSetup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/MVA_Final/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/FCCAnalyses-config/mumu

#python train_xgb_reproduce.py --Vars normal
python train_xgb.py --Vars normal
#python plot_xgb.py --Vars normal
