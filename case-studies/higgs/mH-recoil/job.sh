#!/bin/bash
cd /afs/cern.ch/work/l/lia/private/FCC/NewWorkFlow/FCCAnalyses
source setup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/NewWorkFlow/FCCeePhysicsPerformance/case-studies/higgs/dataframe
source localSetup.sh
cd /afs/cern.ch/work/l/lia/private/FCC/NewWorkFlow/FCCeePhysicsPerformance/case-studies/higgs/mH-recoil/FCCAnalyses-config/ZH

#python train_xgb_reproduce.py --Vars normal
#python train_xgb.py --Vars normal
python plot_xgb.py --Vars normal --Stage validation
