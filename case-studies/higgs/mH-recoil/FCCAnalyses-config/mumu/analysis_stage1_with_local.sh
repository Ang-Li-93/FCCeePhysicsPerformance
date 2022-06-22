#!/bin/bash
echo ${MH_RECOIL_DIR} 
echo 'working directory is ${MH_RECOIL_DIR}'
training_samples='/eos/user/l/lia/FCCee/MVA/training_samples/'
outputDir='/eos/user/l/lia/FCCee/MVA/flatNtuples/'

processes=('wzp6_ee_mumuH_ecm240'
           'p8_ee_WW_mumu_ecm240'
           'wzp6_egamma_eZ_Zmumu_ecm240'
           'wzp6_gammae_eZ_Zmumu_ecm240'
           'wzp6_ee_mumu_ecm240'
           'p8_ee_ZZ_ecm240')

 
for process in "${processes[@]}"
do
  python ${MH_RECOIL_DIR}/analysis/APC/FCCAnalysisRun.py ${MH_RECOIL_DIR}/FCCAnalyses-config/mumu/analysis_stage1_batch.py --files-list ${training_samples}${process}/*.root --output ${outputDir}/${process}/chunk0.root
done
